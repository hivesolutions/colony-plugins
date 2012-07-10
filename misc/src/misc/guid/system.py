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

import time
import socket
import random
import threading

import colony.base.system

MAX_COUNTER = 0xfffffffe
""" The max counter value """

class Guid(colony.base.system.System):
    """
    The guid class.
    """

    def __init__(self, plugin):
        colony.base.system.System.__init__(self, plugin)

        self.counter = 0L
        self.first_counter = MAX_COUNTER
        self.last_time = 0
        self.ip = ""
        self.lock = threading.RLock()

        try:
            self.ip = socket.getaddrinfo(socket.gethostname(), 0)[-1][-1][0]
            self.hexadecimal_ip = make_hexadecimal_ip(self.ip)
        # in case there is no ip, defaults to something in the 10.x.x.x private range
        except:
            self.ip = "10"
            rand = random.Random()
            for _index in range(3):
                # might as well use IPv6 range if we're making it up
                self.ip += "." + str(rand.randrange(1, 0xffff))
            self.hexadecimal_ip = make_hexadecimal_ip(self.ip)

    def generate_guid(self):
        """
        Generates a guid (unique in space and time) number.

        @rtype: String
        @return: The unique guid.
        """

        # acquires the lock, only one guid at the same time
        self.lock.acquire()
        try:
            # the list that represents the various parts of the guid
            parts = []

            # do we need to wait for the next millisecond (are we out of counters?)
            now = long(time.time() * 1000)

            while self.last_time == now and self.counter == self.first_counter:
                time.sleep(.01)
                now = long(time.time() * 1000)

            # appends time part
            parts.append("%016x" % now)

            # time to start counter over since we have a different millisecond
            if self.last_time != now:
                # start at random position
                self.first_counter = long(random.uniform(1, MAX_COUNTER))

                self.counter = self.first_counter
            self.counter += 1
            if self.counter > MAX_COUNTER:
                self.counter = 0
            self.last_time = now

            # appends counter part
            parts.append("%08x" % (self.counter))

            # appends ip part
            parts.append(self.hexadecimal_ip)

            # put all the parts together
            return "".join(parts)
        finally:
            # releases the lock, more guid can be generated now
            self.lock.release()

make_hexadecimal_ip = lambda ip: "".join(["%04x" % long(index) for index in ip.split(".")])
""" Makes an hexadecimal IP from a decimal dot-separated ip (eg: 127.0.0.1) """
