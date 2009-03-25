#!/usr/bin/python
# -*- coding: Cp1252 -*-

# Hive Colony Framework
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 1509 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-02-17 13:44:20 +0000 (ter, 17 Fev 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import business_session_serializer_exceptions

SERVICE_ID = "business_session_serializer"
""" The service id """

SESSION_NAME_VALUE = "session_name"
""" The session name value """

GET_SESSION_METHODS_TYPE_VALUE = "get_session_methods"
""" The get session methods type value """

CALL_SESSION_METHOD_TYPE_VALUE = "call_session_method"
""" The call session method type value """

class BusinessSessionSerializer:
    """
    The business session serializer class.
    """

    business_session_serializer_plugin = None
    """ The business session serializer plugin """

    session_proxy_map = {}
    """ The session proxy used for session access """

    def __init__(self, business_session_serializer_plugin):
        """
        Constructor of the class
        
        @type business_session_serializer_plugin: BusinessSessionSerializerPlugin
        @param business_session_serializer_plugin: The business session serializer plugin.
        """

        self.business_session_serializer_plugin = business_session_serializer_plugin

        self.session_proxy_map = {}

    def add_session_proxy(self, session_proxy):
        # retrieves the session name
        session_name = session_proxy.get_session_name()

        if session_name in self.session_proxy_map:
            raise business_session_serializer_exceptions.SessionSerializerDuplicatedProxy("proxy " + session_name + " already exists")
        else:
            self.session_proxy_map[session_name] = session_proxy

    def remove_session_proxy(self, session_proxy):
        # retrieves the session name
        session_name = session_proxy.get_session_name()

        if session_name in self.session_proxy_map:
            del self.session_proxy_map[session_name]
        else:
            raise business_session_serializer_exceptions.SessionSerializerProxyNotFound("proxy " + session_name + " does not exists")

    def get_service_id(self):
        return SERVICE_ID

    def get_service_alias(self):
        return []

    def get_available_rpc_methods(self):
        return []

    def get_rpc_methods_alias(self):
        return {}

    def get_session_methods(self, session_information):
        # prints the debug message
        self.business_session_serializer_plugin.debug("Received session methods retrieval request")

        # retrieves the session name
        session_name = session_information[SESSION_NAME_VALUE]

        if session_name in self.session_proxy_map:
            session_proxy = self.session_proxy_map[session_name]
        else:
            raise business_session_serializer_exceptions.SessionSerializerProxyNotFound("proxy " + session_name + " does not exists")

        # creates the session information entity
        session_information_structure = SessionInformation()

        # populates the session information entity from the session information map
        session_information_structure.convert_from_map(session_information)

        # creates the session request entity
        session_request_structure = GetSessionMethodsSessionRequest()

        # send the session information and session request to the session proxy
        # for handling
        return session_proxy.handle_request(session_information_structure, session_request_structure)

    def call_session_method(self, session_information, session_entity, session_method, session_method_arguments, session_method_arguments_map):
        # prints the debug message
        self.business_session_serializer_plugin.debug("Received session method call request, session: %s, entity: %s, method: %s" % (str(session_information), session_entity, session_method))

        # retrieves the session name
        session_name = session_information[SESSION_NAME_VALUE]

        if session_name in self.session_proxy_map:
            session_proxy = self.session_proxy_map[session_name]
        else:
            raise business_session_serializer_exceptions.SessionSerializerProxyNotFound("proxy " + session_name + " does not exists")

        # creates the session information entity
        session_information_structure = SessionInformation()

        # populates the session information entity from the session information map
        session_information_structure.convert_from_map(session_information)

        # creates the session request entity
        session_request_structure = CallSessionMethodSessionRequest(session_entity, session_method, session_method_arguments, session_method_arguments_map)

        # send the session information and session request to the session proxy
        # for handling
        return session_proxy.handle_request(session_information_structure, session_request_structure)

class SessionInformation:
    """
    The session information class.
    """

    def __init__(self):
        """
        Constructor of the class
        """

        pass

    def convert_from_map(self, session_information_map):
        """
        Converts the elements of the given map into attributes of
        the session information instance.
        
        @type session_information_map: Dictionary
        @param session_information_map: The session information map to be used in the conversion.
        """

        for key, value in session_information_map.items():
            setattr(self, key, value)

class SessionRequest:
    """
    The session request class.
    """

    session_request_type = "none"
    """ The session request type """

    def __init__(self, session_request_type):
        self.session_request_type = session_request_type

class GetSessionMethodsSessionRequest(SessionRequest):
    """
    The get session methods session request class.
    """

    def __init__(self):
        SessionRequest.__init__(self, GET_SESSION_METHODS_TYPE_VALUE)

class CallSessionMethodSessionRequest(SessionRequest):
    """
    The call session method session request class.
    """

    session_entity = "none"
    """ The session entity """

    session_method = "none"
    """ The session method """

    session_method_arguments = []
    """ The session arguments """

    session_method_arguments_map = []
    """ The session arguments map """

    def __init__(self, session_entity = "none", session_method = "none", session_method_arguments = [], session_method_arguments_map = {}):
        SessionRequest.__init__(self, CALL_SESSION_METHOD_TYPE_VALUE)

        self.session_entity = session_entity
        self.session_method = session_method
        self.session_method_arguments = session_method_arguments
        self.session_method_arguments_map = session_method_arguments_map
