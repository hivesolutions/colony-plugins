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

__revision__ = "$LastChangedRevision: 421 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-11-20 15:16:53 +0000 (Qui, 20 Nov 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

TYPE_VALUE = "type"
""" The type value """

VALUE_VALUE = "value"
""" The value value """

EXTRA_TYPE_VALUE = "extra_type"
""" The extra type value """

TYPE_NUMBER_VALUE = "type_number"
""" The type number value """

TYPE_CONSTRUCTED_VALUE = "type_constructed"
""" The type constructed value """

TYPE_CLASS_VALUE = "type_class"
""" The type class value """

BIND_VALUE = "bind"
""" The bind value """

UNBIND_VALUE = "unbind"
""" The unbind value """

SEARCH_VALUE = "search"
""" The search value """

SEARCH_RESULT_ENTRY_VALUE = "search_result_entry"
""" The search result entry value """

SEARCH_RESULT_DONE_VALUE = "search_result_done"
""" The search result done value """

EOC_TYPE = 0x00
""" The eoc (end of content) type """

BOOLEAN_TYPE = 0x01
""" The boolean type """

INTEGER_TYPE = 0x02
""" The integer type """

BIT_STRING_TYPE = 0x03
""" The bit string type """

OCTET_STRING_TYPE = 0x04
""" The octet string type """

ENUMERATED_TYPE = 0x0a
""" The enumerated type """

SEQUENCE_TYPE = 0x10
""" The sequence type """

SET_TYPE = 0x11
""" The set type """

PRIMITIVE_MODE = 0x00
""" The primitive mode """

CONSTRUCTED_MODE = 0x01
""" The constructed mode """

UNIVERSAL_CLASS = 0x00
""" The universal class """

APPLICATION_CLASS = 0x01
""" The application class """

CONTEXT_SPECIFIC_CLASS = 0x02
""" The context specific class """

PRIVATE_CLASS = 0x03
""" The private class """

LDAP_REQUEST_TYPE_MAP = {
    BIND_VALUE : 0x00,
    UNBIND_VALUE : 0x02,
    SEARCH_VALUE : 0x03,
    "modify" : 0x06,
    "add" : 0x08,
    "delete" : 0x0a,
    "modify_dn" : 0x00,
    "compare" : 0x00,
    "abandon" : 0x00,
    "extended" : 0x00
}
""" The map of ldap request types """

LDAP_RESPONSE_TYPE_MAP = {
    BIND_VALUE : 0x01,
    SEARCH_RESULT_ENTRY_VALUE : 0x04,
    "search_result_reference" : 0x13,
    SEARCH_RESULT_DONE_VALUE : 0x05,
    "modify" : 0x07,
    "add" : 0x09,
    "delete" : 0x0b
}
""" The map of ldap response types """

class ProtocolOperation:

    def __init__(self):
        pass

    def process_value(self, value):
        # retrieves the protocol operation extra type
        protocol_operation_extra_type = value[EXTRA_TYPE_VALUE]

        # retrieves the protocol operation extra type number
        protocol_operation_extra_type_number = protocol_operation_extra_type[TYPE_NUMBER_VALUE]

        # retrieves the protocol operation class from the type
        # class map using the protocol operation extra type number
        protocol_operation_class = TYPE_CLASS_MAP[protocol_operation_extra_type_number]

        # creates a new protocol operation structure
        protocol_operation_structure = protocol_operation_class()

        # processes the value using the value, retrieving the protocol operation
        protocol_operation = protocol_operation_structure.process_value(value)

        # returns the protocol operation
        return protocol_operation

class SearchResultEntry(ProtocolOperation):

    object_name = None

    attributes = None

    def __init__(self, object_name = None, attributes = None):
        self.object_name = object_name
        self.attributes = attributes

    def process_value(self, value):
        # retrieves the ldap result value
        ldap_result_value = value[VALUE_VALUE]

        # retrieves the object name and the object name value
        object_name = ldap_result_value[0]
        object_name_value = object_name[VALUE_VALUE]

        # retrieves the attributes and the attributes value
        attributes = ldap_result_value[1]
        attributes_value = attributes[VALUE_VALUE]

        # creates the attributes value processed and
        # processes it
        attributes_value_processed = PartialAttributeList()
        attributes_value_processed.process_value(attributes_value)

        # sets the current values
        self.object_name = object_name_value
        self.attributes = attributes_value_processed

        # returns the self value
        return self

class PartialAttributeList:

    partial_attributes = None

    partial_attributes_map = None

    def __init__(self, partial_attributes = None):
        self.partial_attributes = partial_attributes

    def process_value(self, value):
        # creates the partial attributes processed value list
        partial_attributes_processed_value = []

        # iterates over all the partial
        # attribute values
        for partial_attribute_value in value:
            partial_attribute_processed = PartialAttributeListItem()
            partial_attribute_processed.process_value(partial_attribute_value)

            partial_attributes_processed_value.append(partial_attribute_processed)

        self.partial_attributes = partial_attributes_processed_value

        # returns the self value
        return self

    def generate_partial_attributes_map(self):
        # creates the partial attributes map
        self.partial_attributes_map = {}

        # iterates over all the partial attributes
        for partial_attribute in self.partial_attributes:
            # retrieves the partial attribute type and values
            partial_attribute_type = partial_attribute.type
            partial_attribute_values = partial_attribute.values

            # sets the partial attribute in the partial attributes map
            self.partial_attributes_map[partial_attribute_type] = partial_attribute_values

class PartialAttributeListItem:

    type = None

    values = None

    def __init__(self, type = None, values = None):
        self.type = type
        self.values = values

    def process_value(self, value):
        # retrieves the ldap result value
        ldap_result_value = value[VALUE_VALUE]

        # retrieves the type and the type value
        type = ldap_result_value[0]
        type_value = type[VALUE_VALUE]

        # retrieves the values and the values value
        values = ldap_result_value[1]
        values_value = values[VALUE_VALUE]

        # creates the values processed value list
        values_processed_value = []

        # iterates over all the values value value
        for values_value_value in values_value:
            values_value_value_value = values_value_value[VALUE_VALUE]
            values_processed_value.append(values_value_value_value)

        # sets the current values
        self.type = type_value
        self.values = values_processed_value

        # returns the self value
        return self

class LdapResult(ProtocolOperation):

    result_code = None

    matched_dn = None

    error_message = None

    referral = None

    def __init__(self, result_code = None, matched_dn = None, error_message = None, referral = None):
        ProtocolOperation.__init__(self)
        self.result_code = result_code
        self.error_message = error_message
        self.referral = referral

    def process_value(self, value):
        # retrieves the ldap result value
        ldap_result_value = value[VALUE_VALUE]

        # retrieves the result code and the result code value
        result_code = ldap_result_value[0]
        result_code_value = result_code[VALUE_VALUE]

        # retrieves the matched dn and the matched dn value
        matched_dn = ldap_result_value[1]
        matched_dn_value = matched_dn[VALUE_VALUE]

        # retrieves the error message and the error message value
        error_message = ldap_result_value[2]
        error_message_value = error_message[VALUE_VALUE]

        # sets the current values
        self.result_code = result_code_value
        self.matched_dn = matched_dn_value
        self.error_message = error_message_value

        # returns the self value
        return self

class BindResponse(LdapResult):
    pass

class SearchResultDone(LdapResult):
    pass

class BindRequest(ProtocolOperation):

    version = None

    name = None

    authentication = None

    def __init__(self, version = None, name = None, authentication = None):
        ProtocolOperation.__init__(self)
        self.version = version
        self.name = name
        self.authentication = authentication

    def get_value(self):
        # retrieves the bind request type
        bind_request_type = LDAP_REQUEST_TYPE_MAP[BIND_VALUE]

        # creates the version integer value
        version = {
            TYPE_VALUE: INTEGER_TYPE,
            VALUE_VALUE : self.version
        }

        # creates the name octet string value
        name = {
            TYPE_VALUE: OCTET_STRING_TYPE,
            VALUE_VALUE : self.name
        }

        # retrieves the authentication value
        authentication = self.authentication.get_value()

        # creates the protocol operation contents (list)
        protocol_operation_contents = [version, name, authentication]

        # creates the bind operation sequence value
        bind_operation = {
            TYPE_VALUE: SEQUENCE_TYPE,
            VALUE_VALUE : protocol_operation_contents,
            EXTRA_TYPE_VALUE : {
                TYPE_NUMBER_VALUE : bind_request_type,
                TYPE_CONSTRUCTED_VALUE : CONSTRUCTED_MODE,
                TYPE_CLASS_VALUE : APPLICATION_CLASS
            }
        }

        # returns the bind operation (value)
        return bind_operation

class UnbindRequest(ProtocolOperation):

    def __init__(self):
        ProtocolOperation.__init__(self)

    def get_value(self):
        # retrieves the unbind request type
        unbind_request_type = LDAP_REQUEST_TYPE_MAP[UNBIND_VALUE]

        # creates the protocol operation contents (list)
        protocol_operation_contents = []

        # creates the unbind operation sequence value
        unbind_operation = {
            TYPE_VALUE: SEQUENCE_TYPE,
            VALUE_VALUE : protocol_operation_contents,
            EXTRA_TYPE_VALUE : {
                TYPE_NUMBER_VALUE : unbind_request_type,
                TYPE_CLASS_VALUE : APPLICATION_CLASS
            }
        }

        # returns the unbind operation (value)
        return unbind_operation

class SearchRequest(ProtocolOperation):
    base_object = None

    scope = None

    deref_aliases = None

    size_limit = None

    time_limit = None

    types_only = None

    filter = None

    attributes = None

    def __init__(self, base_object = None, scope = None, deref_aliases = None, size_limit = None, time_limit = None, types_only = None, filter = None, attributes = None):
        self.base_object = base_object
        self.scope = scope
        self.deref_aliases = deref_aliases
        self.size_limit = size_limit
        self.time_limit = time_limit
        self.types_only = types_only
        self.filter = filter
        self.attributes = attributes

    def get_value(self):
        # retrieves the search request type
        search_request_type = LDAP_REQUEST_TYPE_MAP[SEARCH_VALUE]

        # creates the base object octet string value
        base_object = {
            TYPE_VALUE: OCTET_STRING_TYPE,
            VALUE_VALUE : self.base_object
        }

        # creates the scope enumerated value
        scope = {
            TYPE_VALUE: ENUMERATED_TYPE,
            VALUE_VALUE : self.scope
        }

        # creates the dref aliases enumerated value
        dref_aliases = {
            TYPE_VALUE: ENUMERATED_TYPE,
            VALUE_VALUE : self.deref_aliases
        }

        # creates the size limit integer value
        size_limit = {
            TYPE_VALUE: INTEGER_TYPE,
            VALUE_VALUE : self.size_limit
        }

        # creates the time limit integer value
        time_limit = {
            TYPE_VALUE: INTEGER_TYPE,
            VALUE_VALUE : self.time_limit
        }

        # creates the types only boolean value
        types_only = {
            TYPE_VALUE: BOOLEAN_TYPE,
            VALUE_VALUE : self.types_only
        }

        # retrieves the filter value
        filter = self.filter.get_value()

        # retrieves the attributes value
        attributes = self.attributes.get_value()

        # creates the protocol operation contents (list)
        protocol_operation_contents = [base_object, scope, dref_aliases, size_limit, time_limit, types_only, filter, attributes]

        # creates the search operation sequence value
        search_operation = {
            TYPE_VALUE: SEQUENCE_TYPE,
            VALUE_VALUE : protocol_operation_contents,
            EXTRA_TYPE_VALUE : {
                TYPE_NUMBER_VALUE : search_request_type,
                TYPE_CONSTRUCTED_VALUE : CONSTRUCTED_MODE,
                TYPE_CLASS_VALUE : APPLICATION_CLASS
            }
        }

        # returns the search operation (value)
        return search_operation

class Filter:

    def __init__(self):
        pass

class AndFilter(Filter):

    filters = None

    def __init__(self, filters = None):
        Filter.__init__(self)
        self.filters = filters

    def get_value(self):
        # creates the filters list
        filters = []

        # iterates over all the filters
        for filter in self.filters:
            # retrieves the filter value
            filter = filter.get_value()

            # adds the filter to the list of filters
            filters.append(filter)

        # creates the and filter set value
        and_filter = {
            TYPE_VALUE: SET_TYPE, VALUE_VALUE : filters,
            EXTRA_TYPE_VALUE : {
                TYPE_NUMBER_VALUE : 0,
                TYPE_CONSTRUCTED_VALUE : CONSTRUCTED_MODE,
                TYPE_CLASS_VALUE : CONTEXT_SPECIFIC_CLASS
            }
        }

        # returns the and filter (value)
        return and_filter

class EqualityMatchFilter(Filter):

    attribute_value_assertion = None

    def __init__(self, attribute_value_assertion = None):
        self.attribute_value_assertion = attribute_value_assertion

    def get_value(self):
        # retrieves the attribute value assertion value
        attribute_value_assertion = self.attribute_value_assertion.get_value()

        # sets the extra type in the attribute value assertion (value)
        attribute_value_assertion[EXTRA_TYPE_VALUE] = {
            TYPE_NUMBER_VALUE : 3,
            TYPE_CONSTRUCTED_VALUE : CONSTRUCTED_MODE,
            TYPE_CLASS_VALUE : CONTEXT_SPECIFIC_CLASS
        }

        # returns the attribute value assertion (value)
        return attribute_value_assertion

class PresentFilter(Filter):

    present = None

    def __init__(self, present = None):
        Filter.__init__(self)
        self.present = present

    def get_value(self):
        # creates the present filter octet string value
        present_filter = {
            TYPE_VALUE: OCTET_STRING_TYPE, VALUE_VALUE : self.present,
            EXTRA_TYPE_VALUE : {
                TYPE_NUMBER_VALUE : 7,
                TYPE_CLASS_VALUE : CONTEXT_SPECIFIC_CLASS
            }
        }

        # returns the present filter (value)
        return present_filter

class AttributeValueAssertion:

    attribute_description = None

    assertion_value = None

    def __init__(self, attribute_description = None, assertion_value = None):
        self.attribute_description = attribute_description
        self.assertion_value = assertion_value

    def get_value(self):
        # creates the attribute description octet string value
        attribute_description = {
            TYPE_VALUE: OCTET_STRING_TYPE,
            VALUE_VALUE : self.attribute_description
        }

        # creates the assertion value octet string value
        assertion_value = {
            TYPE_VALUE: OCTET_STRING_TYPE,
            VALUE_VALUE : self.assertion_value
        }

        # creates the attribute value assertion contents (list)
        attribute_value_assertion_contents = [attribute_description, assertion_value]

        # creates the attribute value assertion sequence value
        attribute_value_assertion = {
            TYPE_VALUE: SEQUENCE_TYPE,
            VALUE_VALUE : attribute_value_assertion_contents
        }

        # returns the attribute value assertion (value)
        return attribute_value_assertion

class Authentication:

    def __init__(self):
        pass

class SimpleAuthentication(Authentication):

    value = None

    def __init__(self, value):
        Authentication.__init__(self)
        self.value = value

    def get_value(self):
        # creates the authentication octet string value
        authentication = {
            TYPE_VALUE: OCTET_STRING_TYPE,
            VALUE_VALUE : self.value,
            EXTRA_TYPE_VALUE : {
                TYPE_NUMBER_VALUE : 0,
                TYPE_CLASS_VALUE : CONTEXT_SPECIFIC_CLASS
            }
        }

        # returns the authentication (value)
        return authentication

class Attributes:

    attributes = None

    def __init__(self, attributes = None):
        self.attributes = attributes

    def get_value(self):
        # creates the attributes contents list
        attributes_contents = []

        # iterates over all the attributes
        for attribute in self.attributes:
            # creates the attribute octet string value
            attribute = {
                TYPE_VALUE: OCTET_STRING_TYPE,
                VALUE_VALUE : attribute
            }

            # adds the attribute to the list of attributes contents
            attributes_contents.append(attribute)

        # creates the attributes sequence value
        attributes = {
            TYPE_VALUE: SEQUENCE_TYPE,
            VALUE_VALUE : attributes_contents
        }

        # returns the attributes
        return attributes

TYPE_CLASS_MAP = {
    LDAP_REQUEST_TYPE_MAP[BIND_VALUE] : BindRequest,
    LDAP_RESPONSE_TYPE_MAP[BIND_VALUE] : BindResponse,
    LDAP_REQUEST_TYPE_MAP[UNBIND_VALUE] : UnbindRequest,
    LDAP_REQUEST_TYPE_MAP[SEARCH_VALUE] : SearchRequest,
    LDAP_RESPONSE_TYPE_MAP[SEARCH_RESULT_ENTRY_VALUE] : SearchResultEntry,
    LDAP_RESPONSE_TYPE_MAP[SEARCH_RESULT_DONE_VALUE] : SearchResultDone
}
""" The map associating a type with a class map """
