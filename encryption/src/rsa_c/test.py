#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2014 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import colony

class RsaTest(colony.Test):
    """
    The rsa infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (
            RsaBaseTestCase,
        )

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

        system = self.plugin.system
        test_case.rsa = system.create_structure({})

class RsaBaseTestCase(colony.ColonyTestCase):

    @staticmethod
    def get_description():
        return "Rsa Plugin test case"

    def test__relatively_prime(self):
        result = self.rsa._relatively_prime(3, 1)
        self.assertEqual(result, True)

        result = self.rsa._relatively_prime(
            1303455847,
            80677199572618450341522439921473626971
        )
        self.assertEqual(result, True)

        result = self.rsa._relatively_prime(
            130347,
            80677199572618450341522439921472697123
        )
        self.assertEqual(result, False)

    def test__extended_euclid_greatest_common_divisor(self):
        result = self.rsa._extended_euclid_greatest_common_divisor(171, 10)
        self.assertEqual(result, (1, 1, -17))

        result = self.rsa._extended_euclid_greatest_common_divisor(418297, 225168)
        self.assertEqual(result, (1, -22391, 41596))

        result = self.rsa._extended_euclid_greatest_common_divisor(35713992551911994100259367902610573100, 1585944697)
        self.assertEqual(result, (1, -157708412, 3551446063785330185006617352461492633))
