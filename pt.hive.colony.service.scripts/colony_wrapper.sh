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
COLONY_HOME=/home/jomag/hive-main/pt.hive.colony/trunk/pt.hive.colony/src
COLONY_CONFIGURATION=/etc/colony/configuration.py
PID_FILE=/var/run/colony_wrapper.pid
LOG_FILE_STDOUT=/var/log/colony_wrapper.stdout.log
LOG_FILE_STDERR=/var/log/colony_wrapper.stderr.log

# export the colony home variable
export COLONY_HOME

# launches the colony and redirects the standard output and error
setsid $COLONY_EXECUTABLE --configuration_path=$COLONY_CONFIGURATION 1> $LOG_FILE_STDOUT 2> $LOG_FILE_STDERR &

# touches the pid file with the current pid value
echo $! > $PID_FILE
