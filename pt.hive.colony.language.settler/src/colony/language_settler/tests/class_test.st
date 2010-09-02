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

# __author__    = João Magalhães <joamag@hive.pt>
# __version__   = 1.0.0
# __revision__  = $LastChangedRevision$
# __date__      = $LastChangedDate$
# __copyright__ = Copyright (c) 2008 Hive Solutions Lda.
# __license__   = GNU General Public License (GPL), Version

import sys
import colony.base.plugin_system

class Settler1:
    function print_hello():
        print("hello world")
    end
end

class Settler2:
    function print_hello():
        print("hello world")
    end
end

class Settler extends Settler1, Settler2:
    a = 200
    function set_settler(b):
        self.a = b
    end
    function print_a():
        print(self.a)
    end
    static function print_settler(a):
        print(a)
    end
end

plugin SettlerPlugin implements SettlerCapability allows T1:

    id = "pt.hive.settler"

    platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]

    function set_settler(b):
        self.a = b
        print("ola")
    end

end

platforms = [colony.base.plugin_system.CPYTHON_ENVIRONMENT]

# creates the first settler instance
settler_instance_1 = Settler()

settler_instance_1.set_settler(1)
settler_instance_1.print_a()

# creates the second settler instance
settler_instance_2 = Settler()
settler_instance_2.set_settler(2)
settler_instance_2.a = 20
settler_instance_2.print_hello()

# makes a static call
Settler.print_settler("static call")

# python native call
sys.stdout.write("ola")

# prints the newline
print("")

# loads the settler plugin
#load SettlerPlugin
