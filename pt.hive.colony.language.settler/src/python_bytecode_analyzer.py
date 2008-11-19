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
    print "moddate %s (%s)" % (moddate.encode("hex"), modtime)

    # unmarshals the code object
    code = marshal.load(file)

    # show the code object information
    show_code(code)

def show_code(code, indent = ""):
    """
    Shows some code information about the given code object.
    
    @type code: Code
    @para code: The code object to show some code information.
    """

    # prints the code text
    print "%scode" % indent

    # idents the text
    indent += "   "

    # prints the number of arguments
    print "%sargcount %d" % (indent, code.co_argcount)

    # prints the number of locals
    print "%snlocals %d" % (indent, code.co_nlocals)

    # prints the stack size
    print "%sstacksize %d" % (indent, code.co_stacksize)

    # prints the compilation flags
    print "%sflags %04x" % (indent, code.co_flags)

    # prints the hexadecimal code in a string format
    show_hex("code", code.co_code, indent = indent)

    # disassembles the code 
    dis.disassemble(code)
    print "%sconsts" % indent
    for const in code.co_consts:
        if type(const) == types.CodeType:
            show_code(const, indent+"   ")
        else:
            print "   %s%r" % (indent, const)
    print "%snames %r" % (indent, code.co_names)
    print "%svarnames %r" % (indent, code.co_varnames)
    print "%sfreevars %r" % (indent, code.co_freevars)
    print "%scellvars %r" % (indent, code.co_cellvars)
    print "%sfilename %r" % (indent, code.co_filename)
    print "%sname %r" % (indent, code.co_name)
    print "%sfirstlineno %d" % (indent, code.co_firstlineno)
    show_hex("lnotab", code.co_lnotab, indent=indent)

def show_hex(label, h, indent):
    h = h.encode("hex")
    if len(h) < 60:
        print "%s%s %s" % (indent, label, h)
    else:
        print "%s%s" % (indent, label)
        for i in range(0, len(h), 60):
            print "%s   %s" % (indent, h[i:i+60])

if __name__ == "__main__":
    show_file(sys.argv[1])
