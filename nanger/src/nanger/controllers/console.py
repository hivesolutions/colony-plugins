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

import colony

import base

mvc_utils = colony.__import__("mvc_utils")

BASE_KEYWORDS = ("break", "continue", "pass")
""" The set of python keywords that are considered
basic because their are not suffixed """

SPACE_KEYWORDS = (
    "and", "as", "assert",
    "class", "def", "del",
    "elif", "except", "exec",
    "for", "from", "global",
    "if", "import", "in",
    "is", "lambda", "not",
    "or", "raise", "return",
    "while", "with", "yield"
)
""" The set of python keywords that are meant to
be suffixed with a space character """

DOT_KEYWORDS = ("else", "finally", "try")
""" The set of python keywords that are meant to
be suffixed with a dot character """

class ConsoleController(base.BaseController):
    """
    The nanger console controller.
    """

    interpreters = {}
    """ The map associating the identifier of the interpreter
    with the concrete instance containing the interpreter """

    def __init__(self, plugin, system):
        base.BaseController.__init__(self, plugin, system)
        self.interpreters = {}

    def init(self, request):
        """
        Handles the given initialization request.
        This request should start an execution instance and
        return the identifier to the caller.

        @type request: Request
        @param request: The request to be handled.
        """

        # retrieves the reference to the plugin manager running
        # in the current context
        plugin_manager = self.plugin.manager

        # retrieves the json plugin for the encoding of the
        # response value (serialized value)
        json_plugin = self.plugin.json_plugin

        # retrieves the id of the interpreter instance to be used
        # in case the instance id exists none is created
        instance = self.get_field(request, "instance", None)

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
            "plugins" : plugin_manager.plugins
        }

        # tries to retrieve the correct interpreter from the interpreters
        # map in case it does not exists creates a new one, then sets it
        # back in the interpreters map for latter usage
        interpreter = self.interpreters.get(instance, None)
        interpreter = interpreter or code.InteractiveInterpreter(locals = locals)
        self.interpreters[instance] = interpreter

        # resolves the configuration init file path using the plugins manager
        # then ensures that it exists falling back to the local resources init
        # file that is contained in the bundle
        configuration_file_path = plugin_manager.resolve_file_path("%configuration:" + self.plugin.id + "%/initrc", True)
        plugin_path = plugin_manager.get_plugin_path_by_id(self.plugin.id)
        init_file_path = plugin_path + "/nanger/resources/default/initrc"
        colony.ensure_file_path(configuration_file_path, init_file_path)

        # opens the configuration (init) file and reads the complete set of
        # contents in it (to be executed in the current instance)
        file = open(configuration_file_path, "rb")
        try: contents = file.read()
        except: file.close()

        # replaces the windows styled newlines with the normalized unix like
        # newline styled values (compatibility issues)
        contents = contents.replace("\r\n", "\n")

        # updates the standard output and error buffer files to the new buffer
        # and then runs the command at the interpreter after the execution restore
        # the standard output and error back to the original values
        sys.stdout = buffer_out
        sys.stderr = buffer_err

        try:
            # tries to run the source code extracted from the execution
            # file under the "exec" mode (this should print the results
            # to the standard output)
            interpreter.runsource(contents, configuration_file_path, symbol = "exec")
        finally:
            # restores both the standard output and the standard error streams
            # into the original values (further writes will be handled normally)
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

        # retrieves the values from the standard output and error and checks if
        # the resulting string values should be the error or the output
        result_out = buffer_out.getvalue()
        result_err = buffer_err.getvalue()
        result = result_err or result_out

        # creates the response map and serializes it with json to create the
        # final result contents, should retrieve the appropriate mime type
        response = dict(
            result = result,
            instance = instance
        )
        self.serialize(request, response, serializer = json_plugin)

    def execute(self, request):
        """
        Handles the given execute request.
        This request should execute a python command at the
        server side and then return the result of execution.

        @type request: Request
        @param request: The request to be handled.
        """

        # retrieves the reference to the plugin manager running
        # in the current context
        plugin_manager = self.plugin.manager

        # retrieves the json plugin for the encoding of the
        # response value (serialized value)
        json_plugin = self.plugin.json_plugin

        # retrieves the command that it's meant to be executed by
        # the current python virtual machine, then retrieves the
        # id of the interpreter instance to be used and the final
        # field attribute is the (is) file flag indicating if the
        # command should be compiled in multiple or single line mode
        command = self.get_field(request, "command", "")
        instance = self.get_field(request, "instance", None)
        file = self.get_field(request, "file", 0, int)
        name = self.get_field(request, "name", "<input>")

        # in case no instance (identifier) is found a new randomly generated
        # value is created for it (secure generation)
        instance = instance or str(uuid.uuid4())

        # in case the current command represents a file, a final newline token
        # must be included so that the interpreter knows that no more data
        # is coming, this avoids problems in the compilation
        if file: command += "\n"

        # retrieves the final (file) name defaulting to the input token in case
        # no file flag is set (command came from console)
        name = name if file else "<input>"

        # creates the memory buffer that will hold the contents
        # resulting from the execution of the python code
        buffer_out = cStringIO.StringIO()
        buffer_err = cStringIO.StringIO()

        # creates the map containing the various local names to be used
        # in the interpreter, these are the values that will be made available
        # as entrance points to the end user
        locals = {
            "manager" : plugin_manager,
            "plugins" : plugin_manager.plugins
        }

        # tries to retrieve the correct interpreter from the interpreters
        # map in case it does not exists creates a new one, then sets it
        # back in the interpreters map for latter usage
        interpreter = self.interpreters.get(instance, None)
        interpreter = interpreter or code.InteractiveInterpreter(locals = locals)
        self.interpreters[instance] = interpreter

        try:
            # tries to compile the command using the single line strategy
            # so that the return value is printed to the standard output, this
            # may fail in case a multiple line command is present
            command_code = code.compile_command(command, symbol = file and "exec" or "single")
        except:
            # compiles the provided command into the appropriate code representation
            # using the "exec" strategy, this operation should return an invalid value
            # in case the provided code is not complete (spans multiple lines)
            try: command_code = code.compile_command(command, symbol = "exec")
            except: command_code = None; exception = True
            else: exception = False
        else:
            # unsets the exception flag because no exception occurred while compiling
            # the command using the single line strategy
            exception = False

        # calculates the pending flag value using the returning command code value
        # and the exception flag to do it (this value is going to be sent to the client
        # side to be possible to continuously interpret it)
        pending = not command_code and True or False
        pending = not exception and pending or False

        # updates the standard output and error buffer files to the new buffer
        # and then runs the command at the interpreter after the execution restore
        # the standard output and error back to the original values
        sys.stdout = buffer_out
        sys.stderr = buffer_err
        try:
            # tries to run from either the "compiled" code object or from
            # the source code in case the exception mode was activated
            # this should allow syntax errors to be printed
            if command_code: interpreter.runcode(command_code)
            elif exception: interpreter.runsource(command, filename = name, symbol = "exec")
        finally:
            # restores both the standard output and the standard error streams
            # into the original values (further writes will be handled normally)
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

        # retrieves the values from the standard output and error and checks if
        # the resulting string values should be the error or the output
        result_out = buffer_out.getvalue()
        result_err = buffer_err.getvalue()
        result = result_err or result_out

        # creates the response map and serializes it with json to create the
        # final result contents, should retrieve the appropriate mime type
        response = dict(
            result = result,
            pending = pending,
            instance = instance
        )
        self.serialize(request, response, serializer = json_plugin)

    def autocomplete(self, request):
        """
        Handles the given autocomplete request.
        This request should try to find a series of results
        that may be used as "tips" for the correct command.

        @type request: Request
        @param request: The request to be handled.
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
        command = self.get_field(request, "command", "")
        instance = self.get_field(request, "instance", None)

        # in case no instance (identifier) is found a new randomly generated
        # value is created for it (secure generation)
        instance = instance or str(uuid.uuid4())

        # creates the map containing the various local names to be used
        # in the interpreter, these are the values that will be made available
        # as entrance points to the end user
        locals = {
            "manager" : plugin_manager,
            "plugins" : plugin_manager.plugins
        }

        # tries to retrieve the correct interpreter from the interpreters
        # map in case it does not exists creates a new one, then sets it
        # back in the interpreters map for latter usage, at the final part
        # of the execution updates the current locals reference
        interpreter = self.interpreters.get(instance, None)
        interpreter = interpreter or code.InteractiveInterpreter(locals = locals)
        self.interpreters[instance] = interpreter
        locals = interpreter.locals

        # copies the built in symbols (globally present) into the locals map
        # this allows the autocomplete to couple with these symbols
        colony.map_copy(__builtins__, locals)

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
            if object_type == types.FunctionType: object_type_s = "function"
            elif object_type == types.BuiltinFunctionType: object_type_s = "function"
            elif object_type == types.MethodType: object_type_s = "method"
            elif object_type == types.BuiltinMethodType: object_type_s = "method"
            else: object_type_s = "object"

            # retrieves the documentation part of the object, this is a raw
            # string and should be processed for correct handling
            doc = object.__doc__
            doc, params, _return = self._process_doc(doc)

            # creates the map of options that contains the base documentation
            # string an also the tuple containing the parameters reference
            options = {
                "doc" : doc,
                "params" : params,
                "return" : _return
            }

            # adds the value and the object type values as a tuple to the list
            # of commands (to be interpreted by the client side)
            commands.append((value, object_type_s, options))

        # iterates over all the base keywords in order to be able to
        # filter and add them to the commands list, these keywords
        # will have no extra values associated (basic keywords)
        for keyword in BASE_KEYWORDS:
            if not keyword.startswith(command): continue
            commands.append((keyword, "keyword", {}))

        # iterates over all the space keywords in order to be able to
        # filter and add them to the commands list, these keywords
        # will have the extra space character appended
        for keyword in SPACE_KEYWORDS:
            if not keyword.startswith(command): continue
            commands.append((keyword, "keyword", {"extra" : " "}))

        # iterates over all the base keywords in order to be able to
        # filter and add them to the commands list, these keywords
        # will have the extra dot character appended
        for keyword in DOT_KEYWORDS:
            if not keyword.startswith(command): continue
            commands.append((keyword, "keyword", {"extra" : ":"}))

        # sorts the commands according to their default (alphabetic order) so
        # that they are presented to the end user in the best way possible
        commands.sort()

        # creates the response map and serializes it with json to create the
        # final result contents, should retrieve the appropriate mime type
        response = dict(
            result = commands,
            offset = offset,
            instance = instance
        )
        self.serialize(request, response, serializer = json_plugin)

    def _resolve_value(self, partials, names):
        """
        Resolves a list of partial values into a proper list of
        names using the provided map of names for resolution.

        The provided names may also be an object like element
        and in such case the attributes reference will be used.

        @type partials: List
        @param partials: List of names considered to be the path
        until the element to be retrieved.
        @type names: Dictionary/Object
        @param names: The map or object used as the basic dictionary
        for the resolution of the value.
        @rtype: Tuple
        @return: The tuple containing both the names contained in
        the target element defined by the list of partials and the
        "proper" object pointed by the same list of partials.
        """

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

    def _process_doc(self, doc):
        """
        Processes a normalized documentation string according
        to the global python documentation specification.

        Initial validations are run to ensure that the provided
        documentation string complies with the specification in
        case it does not returns immediately the unprocessed
        string value (fallback situation).

        The processing of the documentation is an expensive
        task and should be cached whenever possible.

        @type doc: String
        @param doc: The documentation string to be parsed and
        processed with the objective of returning a structure.
        @rtype: Tuple
        @return: Tuple containing the base documentation string
        the various parameters and the returns value.
        """

        # in case the provided documentation element is not
        # valid must return immediately with the default values
        if not doc: return doc, (), None

        # in case the documentation element does not comply with
        # the standard structure for the parsing must return
        # with the default values immediately
        if not doc[0] == "\n": return doc, (), None

        # splits the various doc string lines around their newline
        # character, this should be able to return  the various lines
        # in the documentation
        lines = doc.split("\n")

        # initializes the basic structures that controls the documentation
        # lines the parameters and the return value
        _lines = []
        params = []
        params_map = {}
        _return = None

        # unsets the flag that controls if the current value is in transit
        # meaning that lines are pending for completion
        in_transit = False

        # starts the local reference to the currently used parameter and the
        # flag that controls if the current token is part of a the basic
        # documentation part of the string
        param = None
        is_doc = True

        # iterates over all the lines in the documentation string to parse them
        # and create the appropriate structures for returning
        for line in lines:
            # strips the current line removing any extra space like characters
            # available (required for a better look and feel)
            line = line.strip()

            # in case the in transit flag is set data may be pending to be
            # added to the currently loaded parameter observation
            if in_transit:
                # in case the line is not valid (empty) must continue immediately
                # cannot process an empty line
                if not line: continue

                # in case the line refers a special argument an unexpected situation
                # has occurred must skip the in transit situation otherwise must
                # process the in transit line and add it to the currently processing
                # parameters observations
                if line[0] == "@": in_transit = False
                else:
                    # in case the end line dot is the final character in the current
                    # line must unset the in transit situation (end of in transit)
                    if line[-1] == ".": in_transit = False

                    # in case there is a selected parameter and an observations field
                    # in it must add the current line into it
                    if param and param[2]:
                        # adds the current line to the observations part of the parameter
                        # and skips the current line processing
                        param[2] += "\n" + line
                        continue

            # in case the current line refers the parameter special token
            # must process the parameter observations
            if line.startswith("@param"):
                # splits the current line around the separator and then
                # uses the result to unpack the name and description
                parts = line[6:].split(":", 1)
                param_name = parts[0].strip()
                param_desc = "".join(parts[1:]).strip()

                # checks if the current parameter is not present in the map
                # containing the parameters and tries to retrieve it from there
                is_new = not param_name in params_map
                param = params_map.get(param_name, [param_name, None, None])
                param[2] = param_desc

                # in case the parameter is new adds it to the parameters map
                # and to the list of parameters
                if is_new: params_map[param_name] = param; params.append(param)

                # unsets the is documentation flag so that the in transit flag
                # may be set for multiple line parameter descriptions
                is_doc = False

            # in case the current line refers the type special token
            # must process the parameter type
            elif line.startswith("@type"):
                # splits the current line around the separator and then
                # uses the result to unpack the name and type
                parts = line[5:].split(":", 1)
                param_name = parts[0].strip()
                param_type = "".join(parts[1:]).strip()

                # checks if the current parameter is not present in the map
                # containing the parameters and tries to retrieve it from there
                is_new = not param_name in params_map
                param = params_map.get(param_name, [param_name, None, None])
                param[1] = param_type

                # in case the parameter is new adds it to the parameters map
                # and to the list of parameters
                if is_new: params_map[param_name] = param; params.append(param)

                # sets the is documentation flag to prevent the is transit flag
                # from being set (not required)
                is_doc = True

            # in case the current line refers the return special token
            # must process the return value observations
            elif line.startswith("@return"):
                # retrieves the second part of the line as the description
                # of the return value
                description = line[8:].strip()

                # tries to retrieve the currently set return value or creates
                # a new one and sets the values on it
                _return = _return or ["return", None, None]
                _return[2] = description

                # sets the return value as the current parameter in processing
                # and unsets the is documentation flag to allow in transit set
                param = _return
                is_doc = False

            # in case the current line refers the rtype special token
            # must process the return value type
            elif line.startswith("@rtype"):
                # retrieves the second part of the line as the type
                # of the return value
                _type = line[7:].strip()

                # tries to retrieve the currently set return value or creates
                # a new one and sets the values on it
                _return = _return or ["return", None, None]
                _return[1] = _type

                # sets the return value as the current parameter in processing
                # and sets the is documentation flag to avoid in transit set
                param = _return
                is_doc = True

            # otherwise it must be a line belonging to the base observations
            # string (and must be processed as such)
            else:
                # adds the current line to the list of lines (for the base documentation)
                # and sets the is documentation flag to present the in transit flag
                _lines.append(line)
                is_doc = True

            # in case the current token does not belong to a documentation
            # and there is a valid line as there is no dot at the end the
            # in transit flag is set to provide multiple line processing
            if not is_doc and line and not line[-1] == ".": in_transit = True

        # joins the various loaded line into a single documentation string
        # and then returns the a tuple containing that string, the parameters
        # list and the return tuple (processed information)
        _doc = "\n".join(_lines).strip()
        return _doc, params, _return
