#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Colony Framework. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

from .system import ATClient


class APIATTest(colony.Test):
    """
    The API AT infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (APIATBaseTestCase,)

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class APIATBaseTestCase(colony.ColonyTestCase):

    @staticmethod
    def get_description():
        return "API AT Base test case"

    def test_get_certificate_not_before_utc_time(self):
        """
        Tests parsing of UTCTime format (YYMMDDhhmmssZ) for not_before.

        UTCTime uses 2-digit year for dates 1950-2049.
        """

        # creates an ATClient with mock certificate info using UTCTime format
        client = ATClient(
            plugin=None,
            certificate_info={"not_before": "250415073858Z"},
        )

        # retrieves the timestamp and verifies it matches expected value
        # 2025-04-15 07:38:58 UTC = 1744702738
        not_before = client.get_certificate_not_before()
        self.assertEqual(not_before, 1744702738)

    def test_get_certificate_not_before_generalized_time(self):
        """
        Tests parsing of GeneralizedTime format (YYYYMMDDhhmmssZ) for not_before.

        GeneralizedTime uses 4-digit year for dates outside 1950-2049.
        """

        # creates an ATClient with mock certificate info using GeneralizedTime format
        client = ATClient(
            plugin=None,
            certificate_info={"not_before": "20500415073858Z"},
        )

        # retrieves the timestamp and verifies it matches expected value
        # 2050-04-15 07:38:58 UTC = 2533621138
        not_before = client.get_certificate_not_before()
        self.assertEqual(not_before, 2533621138)

    def test_get_certificate_not_after_utc_time(self):
        """
        Tests parsing of UTCTime format (YYMMDDhhmmssZ) for not_after.

        UTCTime uses 2-digit year for dates 1950-2049.
        """

        # creates an ATClient with mock certificate info using UTCTime format
        client = ATClient(
            plugin=None,
            certificate_info={"not_after": "270415074858Z"},
        )

        # retrieves the timestamp and verifies it matches expected value
        # 2027-04-15 07:48:58 UTC = 1807775338
        not_after = client.get_certificate_not_after()
        self.assertEqual(not_after, 1807775338)

    def test_get_certificate_not_after_generalized_time(self):
        """
        Tests parsing of GeneralizedTime format (YYYYMMDDhhmmssZ) for not_after.

        GeneralizedTime uses 4-digit year for dates outside 1950-2049.
        """

        # creates an ATClient with mock certificate info using GeneralizedTime format
        client = ATClient(
            plugin=None,
            certificate_info={"not_after": "20510415074858Z"},
        )

        # retrieves the timestamp and verifies it matches expected value
        # 2051-04-15 07:48:58 UTC = 2565157738
        not_after = client.get_certificate_not_after()
        self.assertEqual(not_after, 2565157738)

    def test_get_certificate_not_before_none(self):
        """
        Tests that get_certificate_not_before returns None when certificate_info is None.
        """

        client = ATClient(plugin=None, certificate_info=None)
        not_before = client.get_certificate_not_before()
        self.assertEqual(not_before, None)

    def test_get_certificate_not_after_none(self):
        """
        Tests that get_certificate_not_after returns None when certificate_info is None.
        """

        client = ATClient(plugin=None, certificate_info=None)
        not_after = client.get_certificate_not_after()
        self.assertEqual(not_after, None)

    def test_get_certificate_not_before_missing_field(self):
        """
        Tests that get_certificate_not_before returns None when not_before field is missing.
        """

        client = ATClient(plugin=None, certificate_info={})
        not_before = client.get_certificate_not_before()
        self.assertEqual(not_before, None)

    def test_get_certificate_not_after_missing_field(self):
        """
        Tests that get_certificate_not_after returns None when not_after field is missing.
        """

        client = ATClient(plugin=None, certificate_info={})
        not_after = client.get_certificate_not_after()
        self.assertEqual(not_after, None)
