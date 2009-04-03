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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import copy
import socket

import main_soap_manager_namespace

from types import *

class SOAPConfig:
    __readonly = ("SSLserver", "SSLclient", "GSIserver", "GSIclient")

    def __init__(self, config = None, **kw):
        d = self.__dict__

        if config:
            if not isinstance(config, SOAPConfig):
                raise AttributeError, "initializer must be SOAPConfig instance"

            s = config.__dict__

            for k, v in s.items():
                if k[0] != "_":
                    d[k] = v
        else:
            # Setting debug also sets returnFaultInfo,
            # dumpHeadersIn, dumpHeadersOut, dumpSOAPIn, and dumpSOAPOut
            self.debug = 0
            self.dumpFaultInfo = 1
            # Setting namespaceStyle sets typesNamespace, typesNamespaceURI,
            # schemaNamespace, and schemaNamespaceURI
            self.namespaceStyle = "1999"
            self.strictNamespaces = 0
            self.typed = 1
            self.buildWithNamespacePrefix = 1
            self.returnAllAttrs = 0

            # Strict checking of range for floats and doubles
            self.strict_range = 0

            # Default encoding for dictionary keys
            self.dict_encoding = "ascii"

            # New argument name handling mechanism.  See
            # README.MethodParameterNaming for details
            self.specialArgs = 1

            # If unwrap_results=1 and there is only element in the struct,
            # SOAPProxy will assume that this element is the result
            # and return it rather than the struct containing it.
            # Otherwise SOAPproxy will return the struct with all the
            # elements as attributes.
            self.unwrap_results = 1

            # Automatically convert SOAP complex types, and
            # (recursively) public contents into the corresponding
            # python types. (Private subobjects have names that start
            # with '_'.)
            #
            # Conversions:
            # - faultType    --> raise python exception
            # - arrayType    --> array
            # - compoundType --> dictionary
            #
            self.simplify_objects = 0

            # Per-class authorization method.  If this is set, before
            # calling a any class method, the specified authorization
            # method will be called.  If it returns 1, the method call
            # will proceed, otherwise the call will throw with an
            # authorization error.
            self.authMethod = None

            # Globus Support if pyGlobus.io available
            try:
                from pyGlobus import io;
                d["GSIserver"] = 1
                d["GSIclient"] = 1
            except:
                d["GSIserver"] = 0
                d["GSIclient"] = 0


            # Server SSL support if M2Crypto.SSL available
            try:
                from M2Crypto import SSL
                d["SSLserver"] = 1
            except:
                d["SSLserver"] = 0

            # Client SSL support if socket.ssl available
            try:
                from socket import ssl
                d["SSLclient"] = 1
            except:
                d["SSLclient"] = 0

        for k, v in kw.items():
            if k[0] != "_":
                setattr(self, k, v)

    def __setattr__(self, name, value):
        if name in self.__readonly:
            raise AttributeError, "readonly configuration setting"

        d = self.__dict__

        if name in ("typesNamespace", "typesNamespaceURI",
                    "schemaNamespace", "schemaNamespaceURI"):

            if name[-3:] == "URI":
                base, uri = name[:-3], 1
            else:
                base, uri = name, 0

            if type(value) == StringType:
                if main_soap_manager_namespace.Namespace.NSMAP.has_key(value):
                    n = (value, main_soap_manager_namespace.Namespace.NSMAP[value])
                elif main_soap_manager_namespace.Namespace.NSMAP_R.has_key(value):
                    n = (main_soap_manager_namespace.Namespace.NSMAP_R[value], value)
                else:
                    raise AttributeError, "unknown namespace"
            elif type(value) in (ListType, TupleType):
                if uri:
                    n = (value[1], value[0])
                else:
                    n = (value[0], value[1])
            else:
                raise AttributeError, "unknown namespace type"

            d[base], d[base + "URI"] = n

            try:
                d["namespaceStyle"] = \
                    main_soap_manager_namespace.Namespace.STMAP_R[(d["typesNamespace"], d["schemaNamespace"])]
            except:
                d["namespaceStyle"] = ""

        elif name == "namespaceStyle":
            value = str(value)

            if not main_soap_manager_namespace.Namespace.STMAP.has_key(value):
                raise AttributeError, "unknown namespace style"

            d[name] = value
            n = d["typesNamespace"] = main_soap_manager_namespace.Namespace.STMAP[value][0]
            d["typesNamespaceURI"] = main_soap_manager_namespace.Namespace.NSMAP[n]
            n = d["schemaNamespace"] = main_soap_manager_namespace.Namespace.STMAP[value][1]
            d["schemaNamespaceURI"] = main_soap_manager_namespace.Namespace.NSMAP[n]

        elif name == "debug":
            d[name]                     = \
                d["returnFaultInfo"]    = \
                d["dumpHeadersIn"]      = \
                d["dumpHeadersOut"]     = \
                d["dumpSOAPIn"]         = \
                d["dumpSOAPOut"]        = value
        else:
            d[name] = value

Config = SOAPConfig()
