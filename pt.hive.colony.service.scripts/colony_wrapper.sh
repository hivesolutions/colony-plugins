#!/bin/sh
# -*- coding: Cp1252 -*-

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

# __author__    = Luís Martinho <lmartinho@hive.pt> & João Magalhães <joamag@hive.pt>
# __version__   = 1.0.0
# __revision__  = $LastChangedRevision$
# __date__      = $LastChangedDate$
# __copyright__ = Copyright (c) 2008 Hive Solutions Lda.
# __license__   = GNU General Public License (GPL), Version 3

# the initial variables
COLONY_EXECUTABLE=colony
COLONY_DAEMON_TEST_EXECUTABLE=colony_daemon_test
COLONY_PATH=/usr/bin/$COLONY_EXECUTABLE
COLONY_DAEMON_TEST_PATH=/usr/bin/$COLONY_DAEMON_TEST_EXECUTABLE
COLONY_CONFIGURATION=/etc/colony/configuration.py
PID_FILE=/var/run/colony_wrapper.pid
LOG_FILE_STDOUT=/var/log/colony_wrapper.stdout.log
LOG_FILE_STDERR=/var/log/colony_wrapper.stderr.log
COLONY_DAEMON_FILE=/var/colony/colony.daemon
COLONY_DAEMON_CHECK_TIMEOUT=120

# export the colony home variable
export COLONY_HOME

# launches the colony and redirects the standard output and error
setsid $COLONY_PATH --configuration_file=$COLONY_CONFIGURATION 1> $LOG_FILE_STDOUT 2> $LOG_FILE_STDERR &

# saves the pid value
PID_VALUE=$!

# checks the colony daemon sanity
$COLONY_DAEMON_TEST_PATH $COLONY_DAEMON_FILE $PID_VALUE $COLONY_DAEMON_CHECK_TIMEOUT

# saves the daemon test return value
DAEMON_TEST_RETURN_VALUE=$?

# in case the daemon test was successful
if [ $DAEMON_TEST_RETURN_VALUE -eq 0 ]; then
    # touches the pid file with the current pid value
    echo DEFAULT_SLEEP_TIME > $PID_FILE
fi

# exits the process with the returning code of
# the daemon test
exit DAEMON_TEST_RETURN_VALUE
