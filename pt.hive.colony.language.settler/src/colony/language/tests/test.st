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

a = 1

function sum_values(a, b, c):
	return_value = a + b + c
	return return_value
end

function print_counter(limit_number):
	counter = 0
	while counter < limit_number:
		print(counter)
		counter = counter + 1
	end
	return 1
end

function hello_world():
	print("hello world")
	return 1
end

function test_global_a():
	global a
	a = a + 10
	print(a)
end

hello_world()
print_counter(30)
sum_result = sum_values(1, 2, 3)
#print("sum: " + str(sum_result))

# changes the global a variable
test_global_a()

# print the new a variable
print(a)
