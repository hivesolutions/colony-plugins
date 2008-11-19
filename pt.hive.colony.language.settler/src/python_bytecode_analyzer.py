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

__revision__ = "$LastChangedRevision: 72 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2008-10-21 23:29:54 +0100 (Ter, 21 Out 2008) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import dis
import marshal
import struct
import sys
import time
import types

def show_file(file_name):
    """
    Shows some python bytecode information about the file with the given name.
    
    @type file_name: String
    @param file_name: The file name of the file to show some python bytecode information.
    """

    # opens the file in read binary mode
    file = open(file_name, "rb")

    # read the magic number
    magic = file.read(4)

    # retrieves the modification date
    modification_date = file.read(4)

    # creates the modification time structure from the modification date
    modification_time = time.asctime(time.localtime(struct.unpack("L", modification_date)[0]))

    # prints the magic number
    print "magic %s" % (magic.encode("hex"))

    # prints the modification date
    print "moddate %s (%s)" % (modification_date.encode("hex"), modification_time)

    # unmarshals the code object
    code = marshal.load(file)

    # show the code object information
    show_code(code)

def show_code(code, indentation = ""):
    """
    Shows some code information about the given code object.
    
    @type code: Code
    @param code: The code object to show some code information.
    @type indentation: String
    @param indentation: The indentation value.
    """

    # prints the code text
    print "%scode" % indentation

    # indents the text
    indentation += "   "

    # prints the number of arguments
    print "%sargcount %d" % (indentation, code.co_argcount)

    # prints the number of locals
    print "%snlocals %d" % (indentation, code.co_nlocals)

    # prints the stack size
    print "%sstacksize %d" % (indentation, code.co_stacksize)

    # prints the compilation flags
    print "%sflags %04x" % (indentation, code.co_flags)

    # prints the hexadecimal code in a string format
    show_hex("code", code.co_code, indentation = indentation)

    # disassembles the code 
    dis.disassemble(code)

    # prints the constants text
    print "%sconsts" % indentation

    # iterates over all the constants
    for constant in code.co_consts:
        # in case is of type code
        if type(constant) == types.CodeType:
            show_code(constant, indentation + "   ")
        else:
            print "   %s%r" % (indentation, constant)

    # prints the names
    print "%snames %r" % (indentation, code.co_names)

    # prints the variable names
    print "%svarnames %r" % (indentation, code.co_varnames)

    # prints the free variables
    print "%sfreevars %r" % (indentation, code.co_freevars)

    # prints the cell variables
    print "%scellvars %r" % (indentation, code.co_cellvars)

    # prints the filename
    print "%sfilename %r" % (indentation, code.co_filename)

    # prints the name
    print "%sname %r" % (indentation, code.co_name)

    # prints the first line number
    print "%sfirstlineno %d" % (indentation, code.co_firstlineno)

    # prints the lnotab value in a string format
    show_hex("lnotab", code.co_lnotab, indentation = indentation)

def show_hex(label, hex_value, indentation):
    """
    Prints the give hexadecimal value to the stdout with the given label and indentation.
    
    @type label: String
    @param label: The label value to be printed.
    @type hex_value: String
    @param hex_value: The hexadecimal value.
    @type indentation: String
    @param indent: The indentation value.
    """

    # encode the hex value in hexadecimal
    hex_value_encoded = hex_value.encode("hex")

    # in case the length of the hexadecimal value is less than 60
    if len(hex_value_encoded) < 60:
        print "%s%s %s" % (indentation, label, hex_value_encoded)
    else:
        print "%s%s" % (indentation, label)
        for index in range(0, len(hex_value_encoded), 60):
            print "%s   %s" % (indentation, hex_value_encoded[index:index + 60])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Invalid number of arguments, the file name is required"
    else:
        show_file(sys.argv[1])
