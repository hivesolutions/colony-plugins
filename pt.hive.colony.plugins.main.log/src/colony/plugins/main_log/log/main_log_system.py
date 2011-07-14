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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import logging

class MainLog:
    """
    The main log class.
    """

    main_log_plugin = None
    """ The main log plugin """

    loggers_map = {}
    """ The loggers map """

    def __init__(self, main_log_plugin):
        """
        Constructor of the class.

        @type main_log_plugin: MainLogPlugin
        @param main_log_plugin: The main log plugin
        """

        self.main_log_plugin = main_log_plugin

    def get_logger(self, logger_name):
        # in case the logger name does not exist in the
        # loggers map
        if not logger_name in self.loggers_map:
            # creates the logger with the logger name
            logger = DefaultLogger(logger_name)

            # sets the logger in the loggers map
            self.loggers_map[logger_name] = logger

        # retrieves the logger from the loggers map
        logger = self.loggers_map[logger_name]

        # return the logger
        return logger

    def get_default_handler(self):
        return DefaultHandler()

    def get_composite_handler(self):
        return CompositeHandler()

class Logger:
    """
    The logger class.
    """

    name = "none"
    handler = None

    def __init__(self, name):
        self.name = name

    def set_handler(self, handler):
        self.handler = handler

    def get_name(self):
        return self.name

class Handler:

    def __init__(self):
        pass

    def emit(self, record):
        pass

class DefaultLogger(Logger):

    logger = None

    handlers_list = []

    def __init__(self, name):
        Logger.__init__(self, name)
        self.logger = logging.getLogger(name)

        self.handlers_list = []

    def set_handler(self, handler):
        Logger.set_handler(self, handler)
        handler_proxy = DefaultHandlerProxy()
        handler_proxy.set_handler(handler)
        self.logger.addHandler(handler_proxy)
        self.handlers_list.append(handler_proxy)

    def unset_handler(self):
        for handler in self.handlers_list:
            self.logger.removeHandler(handler)
        self.handlers_list = []

    def get_logger(self):
        return self.logger

class DefaultHandler(Handler):

    def __init__(self):
        pass

    def emit(self, record):
        print "default: " + record

class CompositeHandler(Handler):

    handler_def = None

    def __init__(self):
        pass

    def emit(self, record):
        self.handler_def(record)

    def set_handler_def(self, handler_def):
        self.handler_def = handler_def

class DefaultHandlerProxy(logging.Handler):

    subject = "none"
    handler = None

    def __init__(self):
        logging.Handler.__init__(self)

    def set_handler(self, handler):
        self.handler = handler

    def get_subject(self, record):
        return self.subject

    def emit(self, record):
        msg = self.format(record)
        self.handler.emit(msg)
