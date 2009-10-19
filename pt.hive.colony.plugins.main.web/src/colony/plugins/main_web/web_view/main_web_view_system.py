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

import main_web_view_exceptions

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
        if not MainWebView.application:
            self.application = PyQt4.QtGui.QApplication(sys.argv)
            MainWebView.application = self.application
        else:
            raise main_web_view_exceptions.MainWebViewInvalidWindow("window already created")

        # creates the main window
        self.main_window = MainWindow(self.main_web_view_plugin)

        # constructs the main window
        self.main_window.contruct()

        # shows the main window
        self.main_window.show()

        # notifies the ready semaphore
        self.main_web_view_plugin.release_ready_semaphore()

        # loops through the application
        self.application.exec_()

    def stop(self):
        # exits the application
        self.application.exit()

class MainWindow(PyQt4.QtGui.QWidget):
    """
    The main window class.
    """

    main_web_view_plugin = None
    """ The main web view plugin """

    web_view = None
    """ The web view """

    main_frame = None
    """ The main frame """

    def __init__(self, main_web_view_plugin):
        """
        Constructor of the class.
        """

        PyQt4.QtGui.QWidget.__init__(self)

        self.main_web_view_plugin = main_web_view_plugin

    def contruct(self):
        """
        The method to construct the ui.
        """

        # retrieves the plugin path
        plugin_path = self.main_web_view_plugin.manager.get_plugin_path_by_id(self.main_web_view_plugin.id)

        # creates a new icon
        icon = PyQt4.QtGui.QIcon(plugin_path + "/main_web/web_view/resources/omni.png")

        # creates the base url value
        base_url = PyQt4.QtCore.QUrl("http://localhost:8080/colony_web/main.html")

        # creates the web view
        self.web_view = PyQt4.QtWebKit.QWebView()

        # retrieves the main frame
        self.main_frame = self.web_view.page().mainFrame()

        # sets the base url value
        self.web_view.setUrl(base_url)

        # creates the box layout
        box_layout = PyQt4.QtGui.QVBoxLayout()

        # adds the web view widget to the box layout
        box_layout.addWidget(self.web_view)

        # resets the box layout margins
        box_layout.setContentsMargins(0, 0, 0, 0)

        # sets the layout
        self.setLayout(box_layout)

        # sets the window icon
        self.setWindowIcon(icon)

        # sets the window title
        self.setWindowTitle("Hive Colony")

        # connects the register symbols method to the java script window object cleared signal
        self.connect(self.main_frame, PyQt4.QtCore.SIGNAL("javaScriptWindowObjectCleared()"), self.register_symbols)

    def register_symbols(self):
        # creates the window access instance
        window_access = WindowAccess(self)

        # registers the symbol in the javascript engine
        self.main_frame.addToJavaScriptWindowObject("windowAccess", window_access)

class WindowAccess(PyQt4.QtCore.QObject):
    """
    The window access class.
    """

    def __init__(self, window):
        PyQt4.QtCore.QObject.__init__(self)

        self.window = window

    @PyQt4.QtCore.pyqtSlot()
    def full(self):
        self.window.showFullScreen()

    @PyQt4.QtCore.pyqtSlot()
    def normal(self):
        self.window.showNormal()

    @PyQt4.QtCore.pyqtSlot(result = bool)
    def is_full(self):
        return self.window.isFullScreen()

    @PyQt4.QtCore.pyqtSlot(result = bool)
    def exit(self):
        return self.window.main_web_view_plugin.manager.unload_system();
