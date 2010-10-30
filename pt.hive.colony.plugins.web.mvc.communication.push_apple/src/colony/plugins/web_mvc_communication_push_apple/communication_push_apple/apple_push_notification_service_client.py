import ssl
import socket
import struct
import binascii

APNS_SSL_COMBINED_KEY_CERTIFICATE_FILE = "c:/apple_development_push_services_lmartinho.pem"
""" The path to the combined key/certificate file used to establish the secure channel with Apple's push server """

DEVICE_TOKEN = "EDDD43A237B610A3A669ACEF25A6477DDC52A268B3997BA4F5002289B25A7739"
""" The hex string value for the device token """

APNS_SERVER_HOSTNAME = "gateway.sandbox.push.apple.com"
APNS_SERVER_PORT = 2195
APNS_FEEDBACK_SERVER_HOSTNAME = "feedback.sandbox.push.apple.com"
APNS_FEEDBACK_SERVER_PORT = 2196

SIMPLE_NOTIFICATION_FORMAT_VALUE = "simple_notification_format"
ENHANCED_NOTIFICATION_FORMAT_VALUE = "enhanced_notification_format"
DEFAULT_NOTIFICATION_FORMAT_VALUE = ENHANCED_NOTIFICATION_FORMAT_VALUE

SIMPLE_NOTIFICATION_FORMAT_COMMAND = 0
ENHANCED_NOTIFICATION_FORMAT_COMMAND = 1
DEFAULT_NOTIFICATION_EXPIRY_TIME = 0

SIMPLE_NOTIFICATION_FORMAT_TEMPLATE = "!BH32sH%ds"
ENHANCED_NOTIFICATION_FORMAT_TEMPLATE = "!BiiH32sH%ds"
ERROR_RESPONSE_FORMAT_TEMPLATE = "!BBi"
FEEDBACK_FORMAT_TEMPLATE = "!IH32s"

NO_ERRORS_ENCOUNTERED_CODE = 0
""" The error code for no errors encountered """

PROCESSING_ERROR_CODE = 1
""" The error code for the processing error """

MISSING_DEVICE_TOKEN_CODE = 2
MISSING_TOPIC_CODE = 3
MISSING_PAYLOAD_CODE = 4
INVALID_TOKEN_SIZE_CODE = 5
INVALID_TOPIC_SIZE_CODE = 6
INVALID_PAYLOAD_SIZE_CODE = 7
INVALID_TOKEN_CODE = 8
UNKNOWN_ERROR_CODE = 255

SSL_ERROR_TIMEOUT_VALUE = "The read operation timed out"
DEFAULT_SSL_SOCKET_TIMEOUT = 1

class ApplePushNotificationServiceException(Exception):
    pass

class MissingFormatException(ApplePushNotificationServiceException):
    pass

class ProcessingErrorException(ApplePushNotificationServiceException):
    pass

class MissingDeviceTokenException(ApplePushNotificationServiceException):
    pass

class MissingTopicException(ApplePushNotificationServiceException):
    pass

class MissingPayloadException(ApplePushNotificationServiceException):
    pass

class InvalidTokenSizeException(ApplePushNotificationServiceException):
    pass

class InvalidTopicSizeException(ApplePushNotificationServiceException):
    pass

class InvalidPaylodSizeException(ApplePushNotificationServiceException):
    pass

class InvalidTokenException(ApplePushNotificationServiceException):
    pass

class UnknownError(ApplePushNotificationServiceException):
    pass

class ApplePushNotificationServiceClient:
    def send_message(self, ssl_socket, device_token_data, payload, format_type=DEFAULT_NOTIFICATION_FORMAT_VALUE):
        # in case the format is simple
        if format_type == SIMPLE_NOTIFICATION_FORMAT_VALUE:
            # sends the message using the simple notification format
            return self.send_simple_format_message(ssl_socket, device_token_data, payload)
        # in case the format is enhanced
        elif format_type == ENHANCED_NOTIFICATION_FORMAT_VALUE:
            # sends the message using the enhanced notification format
            return self.send_enhanced_format_message(ssl_socket, device_token_data, payload)
        # otherwise
        else:
            # missing format exception
            pass

    def send_simple_format_message(self, ssl_socket, device_token, payload):
        """
        Sends a message in the simple notification format.
        Notification messages are binary messages in network order, the simple format is as follows:
        <1 byte command> <2 bytes length><token> <2 bytes length><payload>.
        """

        # creates the format for the message using the payload simple format template
        simple_notification_format = SIMPLE_NOTIFICATION_FORMAT_TEMPLATE % len(payload)

        # retrieves the corresponding command
        command = SIMPLE_NOTIFICATION_FORMAT_COMMAND

        # creates the message
        simple_format_message = struct.pack(simple_notification_format, command, 32, device_token, len(payload), payload)

        print "Sending: " + repr(simple_format_message)

        # writes the message to the secure socket
        number_bytes_written = ssl_socket.write(simple_format_message)

        print "Wrote %d bytes " % number_bytes_written

    def send_enhanced_format_message(self, ssl_socket, device_token, payload):
        """
        Sends a message using the enhanced notification format.
        Notification messages are binary messages in network order, the simple format is as follows:
        <1 byte command> <4 bytes identifier> <4 bytes expiry> <2 bytes length><token> <2 bytes length><payload>.
        """

        # creates the format for the message using the payload enhanced format template
        enhanced_notification_format = ENHANCED_NOTIFICATION_FORMAT_TEMPLATE % len(payload)

        # retrieves the corresponding command
        command = ENHANCED_NOTIFICATION_FORMAT_COMMAND

        # initializes the notification identifier
        identifier = 3

        # initializes the expiry time for this notification
        expiry = DEFAULT_NOTIFICATION_EXPIRY_TIME

        # creates the message to send
        enhanced_format_message = struct.pack(enhanced_notification_format, command, identifier, expiry, 32, device_token, len(payload), payload)

        print "Sending: " + repr(enhanced_format_message)

        # writes the message to the socket
        number_bytes_written = ssl_socket.write(enhanced_format_message)

        print "Wrote %d bytes " % number_bytes_written

        try:
            # retrieves the response packet from the socket
            data = ssl_socket.read(6)
        except ssl.SSLError, error:
            # in case a timeout occur
            if error.args[0] == SSL_ERROR_TIMEOUT_VALUE:
                # signals write went ok
                return number_bytes_written

        # retrieves the error response format
        error_response_format = ERROR_RESPONSE_FORMAT_TEMPLATE

        # unpacks the information in the response packet
        command, status, identifier = struct.unpack(error_response_format, data)

        # no error encountered
        if status == NO_ERRORS_ENCOUNTERED_CODE:
            pass
        # processing error
        elif status == PROCESSING_ERROR_CODE:
            raise ProcessingErrorException
        # missing device token
        elif status == MISSING_TOPIC_CODE:
            raise MissingDeviceTokenException
        # missing topic exception
        elif status == MISSING_TOPIC_CODE:
            raise MissingTopicException
        # missing payload
        elif status == MISSING_PAYLOAD_CODE:
            raise MissingPayloadException
        # invalid token size
        elif status == INVALID_TOKEN_SIZE_CODE:
            raise InvalidTokenSizeException
        # invalid topic size
        elif status == INVALID_TOPIC_SIZE_CODE:
            raise InvalidTopicSizeException
        # invalid payload size
        elif status == INVALID_PAYLOAD_SIZE_CODE:
            raise InvalidPaylodSizeException
        # invalid token
        elif status == INVALID_TOKEN_CODE:
            raise InvalidTokenException
        # none (unknown)
        elif status == UNKNOWN_ERROR_CODE:
            raise UnknownError

        ssl_socket.close()

    def get_feedback(self):
        # creates the ssl for the feedback request
        feedback_ssl_socket = self.create_ssl_socket(APNS_FEEDBACK_SERVER_HOSTNAME, APNS_FEEDBACK_SERVER_PORT)

        # creates the feedback format
        feedback_format = FEEDBACK_FORMAT_TEMPLATE

        print "Retrieving feedback"

        # reading the feedback data from the socket
        # as described in the Apple documentation
        # transmission begins as soons as one is connected
        data = feedback_ssl_socket.read(38)

        print 'Got %d bytes: %s' % (len(data), repr(data))

        if len(data):
            # retrieves the feedback data
            timestamp, token_length, device_token = struct.unpack(feedback_format, data)

            # prints the retrieved values
            # packing the unpacked values just for the print
            print "timestamp: %d, token_length: %d, device_token: %s" % (timestamp, token_length, device_token)

    def create_ssl_socket(self, hostname, port):
        """
        Creates an ssl socket to be used with the provided hostname at the specified port.
        """

        # creats the plain socket
        plain_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # wraps the plain socket in an ssl context
        ssl_socket = ssl.wrap_socket(plain_socket, certfile=APNS_SSL_COMBINED_KEY_CERTIFICATE_FILE)

        # connects the socket to the provided target
        ssl_socket.connect((hostname, port))

        # sets the timeout on the socket
        ssl_socket.settimeout(DEFAULT_SSL_SOCKET_TIMEOUT)

        return ssl_socket

    def send_payload(self, device_token, payload):
        # creates a new ssl socket to send the notification
        notification_ssl_socket = self.create_ssl_socket(APNS_SERVER_HOSTNAME, APNS_SERVER_PORT)

        # converts the device token to a binary buffer
        binary_device_token = binascii.unhexlify(device_token)

        # sends the message using the default format
        self.send_message(notification_ssl_socket, binary_device_token, payload)
