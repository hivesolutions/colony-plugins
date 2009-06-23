#!/usr/bin/python
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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 2339 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2009-04-01 17:39:24 +0100 (qua, 01 Abr 2009) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import sys

import PyQt4.QtCore
import PyQt4.QtGui
import PyQt4.QtWebKit

class MainWebView:
    """
    The main web view class.
    """

    main_web_view_plugin = None
    """ The main web view plugin """

    application = None
    """ The application object """

    main_window = None
    """ The main window """

    def __init__(self, main_web_view_plugin):
        """
        Constructor of the class

        @type main_web_view_plugin: Plugin
        @param main_web_view_plugin: The main web view plugin.
        """

        self.main_web_view_plugin = main_web_view_plugin

    def start(self):
        # creates a new qt gui application
        self.application = PyQt4.QtGui.QApplication(sys.argv )

        self.mt = MyThread()

        self.mt.start()

        # notifies the ready semaphore
        self.main_web_view_plugin.release_ready_semaphore()

        # loops through the application
        self.application.exec_()

    def stop(self):
        self.mt.add_event("close")

class MainWindow(PyQt4.QtGui.QWidget):
    """
    The main window class.
    """

    def __init__(self):
        """
        Constructor of the class.
        """

        PyQt4.QtGui.QWidget.__init__(self)

        #icon = QtGui.QIcon("omni.png")

        self.a = A(self)
        self.txt = PyQt4.QtWebKit.QWebView()

        self.txt.setUrl(PyQt4.QtCore.QUrl("file:///C:/Users/joamag/workspace/pt.hive.colony.web.ui/test_web_ui.html"))

        #self.txt.page().mainFrame().evaluateJavaScript("alert(1)")

        tab = PyQt4.QtGui.QVBoxLayout()

        tab.addWidget(self.txt)

        tab.setContentsMargins(0, 0, 0, 0)
        self.setLayout(tab)
        #self.setWindowIcon(icon)
        self.setWindowTitle('Hive Colony')

        self.close_signal = PyQt4.QtCore.SIGNAL("close")

        self.connect(self, self.close_signal, self.close_2)

        self.connect(self.txt.page().mainFrame(), PyQt4.QtCore.SIGNAL("javaScriptWindowObjectCleared()"), self.object_cleared)

    def object_cleared(self):
        self.txt.page().mainFrame().addToJavaScriptWindowObject("a", self.a)

    def close_2(self):
        self.close()

    def call_signal(self):
        self.emit(self.close_signal)

class MyThread(PyQt4.QtCore.QThread ):
    def __init__(self):
        PyQt4.QtCore.QThread.__init__( self )

        self.queue = []

    def run(self):
        # creates the main window
        self.main_window = MainWindow()

        # shows the main window
        self.main_window.show()

        while True:
            print "adeus"
            if self.queue:
                value = self.queue.pop()
                if value == "close":
                    self.main_window.close()

            self.sleep(1)
            print "ola"

    def add_event(self, event_name):
        self.queue.append(event_name)

class A(PyQt4.QtCore.QObject):
    def __init__(self, window):
        PyQt4.QtCore.QObject.__init__(self)
        self.window = window
        self.b = 24

    @PyQt4.QtCore.pyqtSlot(result = int)
    def b(self):
        return 2

    @PyQt4.QtCore.pyqtSlot(result = int)
    def full(self):
        self.window.showFullScreen()
        return 1

    @PyQt4.QtCore.pyqtSlot(result = int)
    def normal(self):
        self.window.showNormal()
        return 1

    @PyQt4.QtCore.pyqtSlot(result = bool)
    def is_full(self):
        return self.window.isFullScreen()
