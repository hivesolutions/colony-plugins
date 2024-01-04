#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2023 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2023 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

from . import asynchronous
from . import exceptions
from . import synchronous
from . import system
from . import threads

from .asynchronous import SelectPolling, EpollPolling, KqueuePolling, Connection
from .exceptions import (
    ServiceUtilsException,
    SocketProviderNotFound,
    SocketUpgraderNotFound,
    ServerRequestTimeout,
    ClientRequestTimeout,
    ServerResponseTimeout,
    ClientResponseTimeout,
    RequestClosed,
    PortStarvationReached,
    ConnectionChangeFailure,
)
from .synchronous import (
    AbstractServiceConnectionHandler,
    AbstractServiceConnectionlessHandler,
)
from .system import ServiceUtils
from .threads import ServiceAcceptingThread, ServiceExecutionThread

from .asynchronous import AbstractService as AbstractServiceAsync
from .synchronous import AbstractService as AbstractServiceSync
