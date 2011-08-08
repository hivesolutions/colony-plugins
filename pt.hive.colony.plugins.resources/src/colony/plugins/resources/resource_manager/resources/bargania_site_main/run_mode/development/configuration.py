#!/usr/bin/python
# -*- coding: utf-8 -*-

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

__author__ = "Luís Martinho <lmartinho@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 2341 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:42:37 +0100 (qua, 01 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

configuration = {
    "email" : {
        "sender_email" : "no-reply@bargania.com",
        "sender_name" : "Bargania",
        "smtp" : {
            "hostname" : "localhost",
            "port" : 25,
            "username" : None,
            "password" : None,
            "tls" : False
        }
    },
    "facebook" : {
        "consumer_id" : "193570730692520",
        "consumer_key" : "70aa4a18192b1d3c7cd00eebd0189d0a",
        "consumer_secret" : "2a6e545effd2776c0c6d6b3f2d8fb819",
        "consumer_scope" : "email"
    },
    "site" : {
        "base_url" : "http://localhost:8080/bargania/"
    },
    "tasks" : {
        "fetch_deals" : {
            "schedule" : False
        },
        "cleanup_deals" : {
            "schedule" : False
        },
        "close_trades" : {
            "schedule" : False
        }
    }
}
