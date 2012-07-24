#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import sys
import code
import uuid
import types
import cStringIO

import colony.libs.import_util

mvc_utils = colony.libs.import_util.__import__("mvc_utils")
controllers = colony.libs.import_util.__import__("controllers")

class ConsoleController(controllers.Controller):
    """
    The nanger console controller.
    """

    interpreters = {}
    """ The map associating the identifier of the interpreter
    with the concrete instance containing the interpreter """

    def __init__(self, plugin, system):
        controllers.Controller.__init__(self, plugin, system)
        self.interpreters = {}

    def handle_execute(self, rest_request, parameters = {}):
        """
        Handles the given execute rest request.
        This request should execute a python command at the
        server side and then return the result of execution.

        @type rest_request: RestRequest
        @param rest_request: The rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the reference to the plugin manager running
        # in the current context
        plugin_manager = self.plugin.manager

        # retrieves the json plugin for the encoding of the
        # response value (serialized value)
        json_plugin = self.plugin.json_plugin

        # retrieves the command that it's meant to be executed by
        # the current python virtual machine, then retrieves the
        # id of the interpreter instance to be used
        command = self.get_field(rest_request, "command", "")
        instance = self.get_field(rest_request, "instance", None)

        # in case no instance (identifier) is found a new randomly generated
        # value is created for it (secure generation)
        instance = instance or str(uuid.uuid4())

        # creates the memory buffer that will hold the contents
        # resulting from the execution of the python code
        buffer_out = cStringIO.StringIO()
        buffer_err = cStringIO.StringIO()

        # creates the map containing the various local names to be used
        # in the interpreter, these are the values that will be made available
        # as entrance points to the end user
        locals = {
            "manager" : plugin_manager,
            "plugin_manager" : plugin_manager
        }

        # tries to retrieve the correct interpreter from the interpreters
        # map in case it does not exists creates a new one, then sets it
        # back in the interpreters map for latter usage
        interpreter = self.interpreters.get(instance, None)
        interpreter = interpreter or code.InteractiveInterpreter(locals = locals)
        self.interpreters[instance] = interpreter

        # updates the standard output and error buffer files to the new buffer
        # and then runs the command at the interpreter after the execution restore
        # the standard output and error back to the original values
        sys.stdout = buffer_out
        sys.stderr = buffer_err
        try: interpreter.runsource(command)
        finally: sys.stdout = sys.__stdout__; sys.stderr = sys.__stderr__

        # retrieves the values from the standard output and error and checks if
        # the resulting string values should be the error or the output
        result_out = buffer_out.getvalue()
        result_err = buffer_err.getvalue()
        result = result_err or result_out

        # creates the response map and serializes it with json to create the
        # final result contents, should retrieve the appropriate mime type
        response = {
            "result" : result,
            "instance" : instance
        }
        result = json_plugin.dumps(response)
        mime_type = json_plugin.get_mime_type()

        # sets the (resulting) contents in the rest request and sets the
        # appropriate mime type according to the serialization
        self.set_contents(rest_request, result, content_type = mime_type)

    def handle_autocomplete(self, rest_request, parameters = {}):
        """
        Handles the given autocomplete rest request.
        This request should try to find a series of results
        that may be used as "tips" for the correct command.

        @type rest_request: RestRequest
        @param rest_request: The rest request to be handled.
        @type parameters: Dictionary
        @param parameters: The handler parameters.
        """

        # retrieves the reference to the plugin manager running
        # in the current context
        plugin_manager = self.plugin.manager

        # retrieves the json plugin for the encoding of the
        # response value (serialized value)
        json_plugin = self.plugin.json_plugin

        # retrieves the command that it's meant to be executed by
        # the current python virtual machine, then retrieves the
        # id of the interpreter instance to be used
        command = self.get_field(rest_request, "command", "")
        instance = self.get_field(rest_request, "instance", None)

        # in case no instance (identifier) is found a new randomly generated
        # value is created for it (secure generation)
        instance = instance or str(uuid.uuid4())

        # creates the map containing the various local names to be used
        # in the interpreter, these are the values that will be made available
        # as entrance points to the end user
        locals = {
            "manager" : plugin_manager,
            "plugin_manager" : plugin_manager
        }

        # tries to retrieve the correct interpreter from the interpreters
        # map in case it does not exists creates a new one, then sets it
        # back in the interpreters map for latter usage, at the final part
        # of the execution updates the current locals reference
        interpreter = self.interpreters.get(instance, None)
        interpreter = interpreter or code.InteractiveInterpreter(locals = locals)
        self.interpreters[instance] = interpreter
        locals = interpreter.locals

        # creates a new list to hold the various commands to be sent as valid
        # autocomplete values for the client side
        commands = []

        # splits the command into the various sub components so that its possible
        # to use the partials value to recursively resolve the appropriate sequence
        # to be iterated for searching
        command_split = command.rsplit(".")
        base = command_split[-1]
        partials = command_split[:-1]
        values, container = self._resolve_value(partials, locals)

        # calculates the offset position where the value used in the command calculus
        # is starting, this value may be used for the prefix calculation at the client
        offset = len(command) - len(base)

        # iterates over the complete list of values to test the
        # beginning of each name against the command name
        for value in values:
            # in case the current value does not start
            # with the command text must be skipped, otherwise
            # adds the local name to the list of valid commands
            # for the autocomplete operation
            if not value.startswith(base): continue

            # retrieves the object associated with the current value (name)
            # taking into account the type of the container object (different
            # strategies apply for different container types)
            if type(container) == types.DictType: object = container[value]
            else: object = getattr(container, value)

            # retrieves the (python) object type and then uses it to convert
            # the type into the "normalized" string representation
            object_type = type(object)
            if object_type == types.MethodType: object_type_s = "method"
            elif object_type == types.FunctionType: object_type_s = "function"
            else: object_type_s = "object"

            # adds the value and the object type values as a tuple to the list
            # of commands (to be interpreted by the client side)
            commands.append((value, object_type_s))

        # creates the response map and serializes it with json to create the
        # final result contents, should retrieve the appropriate mime type
        response = {
            "result" : commands,
            "offset" : offset,
            "instance" : instance
        }
        result = json_plugin.dumps(response)
        mime_type = json_plugin.get_mime_type()

        # sets the (resulting) contents in the rest request and sets the
        # appropriate mime type according to the serialization
        self.set_contents(rest_request, result, content_type = mime_type)

    def _resolve_value(self, partials, names):
        # in case the names list is not valid (probably an unset
        # value from a resolution error) returns an empty map
        if not names: return ({}, {})

        # in case there are no more partials for resolution the
        # final values sequence must be returned, note that an
        # appropriate conversion is done in case no map type is
        # present (object value)
        if not partials: return type(names) == types.DictType and (names, names) or (dir(names), names)

        # retrieves the first partial values, this value
        # is going to be used as the reference value for
        # the attribute retrieval
        partial = partials[0]
        names_type = type(names)

        # uses the appropriate strategy to retrieve the value taking
        # into account the appropriate type
        if names_type == types.DictType: value = names.get(partial, None)
        else: value = hasattr(names, partial) and getattr(names, partial) or None

        # returns the result of the recursion step on top of the
        # the currently resolve value and the remainder list of
        # partials (new partials)
        return self._resolve_value(partials[1:], value)
