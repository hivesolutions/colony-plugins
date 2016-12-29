#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2017 Hive Solutions Lda.
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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import colony

SIMPLE_OBJECT = [
    ["age", "country", "name"],
    [24, "Portugal", "João"],
    [12, "Ireland", "Michael"]
]

COMPLEX_OBJECT = [
    ["age", "country", "name"],
    [24, "Portugal", "João"],
    [12, "Ireland", "Michael"],
    [36, "China", "杰"]
]

SIMPLE_CSV = colony.legacy.u("""age;country;name
24;Portugal;João
12;Ireland;Michael
""")

COMPLEX_CSV = colony.legacy.u("""age;country;name
24;Portugal;João
12;Ireland;Michael
36;China;杰
""")

SIMPLE_RAW = [
    dict(
        age = colony.legacy.u("24"),
        country = colony.legacy.u("Portugal"),
        name = colony.legacy.u("João")
    ),
    dict(
        age = colony.legacy.u("12"),
        country = colony.legacy.u("Ireland"),
        name = colony.legacy.u("Michael")
    )
]

COMPLEX_RAW = [
    dict(
        age = colony.legacy.u("24"),
        country = colony.legacy.u("Portugal"),
        name = colony.legacy.u("João")
    ),
    dict(
        age = colony.legacy.u("12"),
        country = colony.legacy.u("Ireland"),
        name = colony.legacy.u("Michael")
    ),
    dict(
        age = colony.legacy.u("36"),
        country = colony.legacy.u("China"),
        name = colony.legacy.u("杰")
    )
]
