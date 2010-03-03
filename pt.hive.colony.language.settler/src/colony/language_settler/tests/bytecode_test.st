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

function settler(a, b):
    print(a)
    return 1 + 2 + b
end

a = 2
print(1 + 2 * 12 + 34)
print("ola")
print(-a)
print(1 == 1)

settler("rabeton", 2)

a = 6

if a > 1 and a < 10:
    if a > 3 and a < 5:
        print("ola")
    elif a > 5 and a < 7:
        print("adeus")
    elif a > 7 and a < 9:
        print("settler")
    else:
        print("bosta")
    end
else:
    print("a = other")
end

a = False
b = False
c = False
d = False
e = False

if (a and b or c) and d or b and c:
    print(a)
end

a = 1

while a < 10:
    a = a + 1
    print(a)
end

function rabeta(a, b):
    return a + b
end

print(rabeta(1, 3))
