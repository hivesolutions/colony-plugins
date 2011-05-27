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

__author__ = "João Magalhães <joamag@hive.pt> & Tiago Silva <tsilva@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 14422 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2011-05-27 14:46:32 +0100 (Fri, 27 May 2011) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os

import wx.stc

CARET = ">>>"
""" The caret """

NAVIGATION_KEYS = (
    wx.WXK_END,
    wx.WXK_LEFT,
    wx.WXK_RIGHT,
    wx.WXK_UP,
    wx.WXK_DOWN,
    wx.WXK_PRIOR,
    wx.WXK_NEXT
)
""" The navigation keys """

RETURN_KEYS = (
    wx.WXK_RETURN,
    wx.WXK_NUMPAD_ENTER
)
""" The return keys """

# in case the current platform is windows
if "wxMSW" in wx.PlatformInfo:
    FACES = {
        "times"     : "Times New Roman",
        "mono"      : "Courier New",
        "helv"      : "Arial",
        "lucida"    : "Lucida Console",
        "other"     : "Comic Sans MS",
        "size"      : 10,
        "lnsize"    : 8,
        "backcol"   : "#FFFFFF",
        "calltipbg" : "#FFFFB8",
        "calltipfg" : "#404040"
    }
# in case the current platform is gtk (unix, linux, etc.)
elif "wxGTK" in wx.PlatformInfo and "gtk2" in wx.PlatformInfo:
    FACES = {
        "times"     : "Serif",
        "mono"      : "Monospace",
        "helv"      : "Sans",
        "other"     : "new century schoolbook",
        "size"      : 10,
        "lnsize"    : 9,
        "backcol"   : "#FFFFFF",
        "calltipbg" : "#FFFFB8",
        "calltipfg" : "#404040"
    }
# in case the current platform is mac os x
elif "wxMac" in wx.PlatformInfo:
    FACES = {
        "times"     : "Lucida Grande",
        "mono"      : "Monaco",
        "helv"      : "Geneva",
        "other"     : "new century schoolbook",
        "size"      : 13,
        "lnsize"    : 10,
        "backcol"   : "#FFFFFF",
        "calltipbg" : "#FFFFB8",
        "calltipfg" : "#404040"
    }
# in case the current platform is mac os x
else:
    FACES = {
        "times"     : "Times",
        "mono"      : "Courier",
        "helv"      : "Helvetica",
        "other"     : "new century schoolbook",
        "size"      : 12,
        "lnsize"    : 10,
        "backcol"   : "#FFFFFF",
        "calltipbg" : "#FFFFB8",
        "calltipfg" : "#404040"
    }

class ColonyConsoleWindow(wx.stc.StyledTextCtrl):
    """
    The colony console window class.
    """

    def __init__(self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.CLIP_CHILDREN, intro_message = "none"):
        # calls the super
        wx.stc.StyledTextCtrl.__init__(self, parent, id, pos, size, style)

        # sets the intro message
        self.intro_message = intro_message

        # sets the editor to be in wrap mode
        self.SetWrapMode(True)

        # sets the styles
        self.set_styles(FACES)

        # assign handlers for keyboard events
        self.Bind(wx.EVT_CHAR, self.on_char)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

        # starts the console
        self.start_console()

    def set_console_plugin(self, console_plugin):
        # sets the console plugin
        self.console_plugin = console_plugin

    def set_display_line_numbers(self, state):
        if state:
            self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
            self.SetMarginWidth(1, 40)
        else:
            # leave a small margin so the feature hidden lines marker can be seen
            self.SetMarginType(1, 0)
            self.SetMarginWidth(1, 10)

    def set_styles(self, faces):
        """
        Configures font size, typeface and color for lexer.

        @type faces: Dictionary
        @param faces: The dictionary that contains the style attributes.
        """

        # sets the default style
        self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, "face:%(mono)s,size:%(size)d,back:%(backcol)s" % faces)

        # retrieves the colors
        foreground_color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        background_color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)

        # sets the colors
        self.StyleClearAll()
        self.SetSelForeground(True, foreground_color)
        self.SetSelBackground(True, background_color)

        # sets the built in styles
        self.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER, "back:#C0C0C0,face:%(mono)s,size:%(lnsize)d" % FACES)
        self.StyleSetSpec(wx.stc.STC_STYLE_CONTROLCHAR, "face:%(mono)s" % faces)
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT, "fore:#0000FF,back:#FFFF88")
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD, "fore:#FF0000,back:#FFFF88")

        # sets the python styles
        self.StyleSetSpec(wx.stc.STC_P_DEFAULT, "face:%(mono)s" % faces)
        self.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, "fore:#007F00,face:%(mono)s" % faces)
        self.StyleSetSpec(wx.stc.STC_P_NUMBER, "")
        self.StyleSetSpec(wx.stc.STC_P_STRING, "fore:#7F007F,face:%(mono)s" % faces)
        self.StyleSetSpec(wx.stc.STC_P_CHARACTER, "fore:#7F007F,face:%(mono)s" % faces)
        self.StyleSetSpec(wx.stc.STC_P_WORD, "fore:#00007F,bold")
        self.StyleSetSpec(wx.stc.STC_P_TRIPLE, "fore:#7F0000")
        self.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, "fore:#000033,back:#FFFFE8")
        self.StyleSetSpec(wx.stc.STC_P_CLASSNAME, "fore:#0000FF,bold")
        self.StyleSetSpec(wx.stc.STC_P_DEFNAME, "fore:#007F7F,bold")
        self.StyleSetSpec(wx.stc.STC_P_OPERATOR, "")
        self.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, "")
        self.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F")
        self.StyleSetSpec(wx.stc.STC_P_STRINGEOL, "fore:#000000,face:%(mono)s,back:#E0C0E0,eolfilled" % faces)

    def start_console(self):
        # writes the introduction
        self.write_intro()

        # writes the caret
        self.write_caret()

    def write(self, text):
        """
        Displays the text in the shell and replaces
        line endings with OS-specific endings.

        @type text: String
        @param text: The text to displayed.
        """

        # fixes the line endings
        text = self.fix_line_endings(text)

        # adds the text
        self.AddText(text)

        # ensures the caret is visible
        self.EnsureCaretVisible()

    def write_new_line(self, text, new_line = True):
        # writes the text
        self.write(text)

        # adds a new line
        new_line and self.AddText("\n")

    def write_intro(self):
        # writes the introduction message
        self.write_new_line(self.intro_message)

    def write_caret(self):
        # retrieves the current end position of the text
        current_end_position = self.GetTextLength()

        # moves the caret to the last position of the text
        self.SetCurrentPos(current_end_position)

        # writes the caret
        self.write(CARET + " ")

        # sets the carret position end
        self.carret_position_end = self.GetCurrentPos()

    def fix_line_endings(self, text):
        """
        Return text with line endings replaced by OS-specific endings.

        @type text: String
        @param text: The text to be returned with line endings replaced by OS-specific endings.
        @rtype: String
        @return: The text with line endings replaced by OS-specific endings.
        """

        # splits the text into lines
        lines = text.split("\r\n")

        # calculates the number of lines
        number_lines = len(lines)

        # creates the line range
        line_range = range(number_lines)

        for line_index in line_range:
            # retrieves the line
            line = lines[line_index]

            # splits the line into chunks
            chunks = line.split("\r")

            # calculates the number of chunks
            number_chunks = len(chunks)

            # creates the chunk range
            chunk_range = range(number_chunks)

            # for each chunk
            for chunk_index in chunk_range:
                # retrieves the chunk
                chunk = chunks[chunk_index]

                # retrieves the chunk tokens
                chunk_tokens = chunk.split("\n")

                # joins the chunk tokens
                chunks[chunk_index] = os.linesep.join(chunk_tokens)

            # joins the chunks
            lines[line_index] = os.linesep.join(chunks)

        # joins the lines
        text = os.linesep.join(lines)

        # returns the text
        return text

    def can_edit(self):
        """
        Returns true if editing should succeed.

        @rtype: bool
        @return: The result of the edit test (if successful or not).
        """

        # retrieves the current position
        current_position = self.GetCurrentPos()

        # retrieves the selection start
        selection_start = self.GetSelectionStart()

        # retrieves the selection end
        selection_end = self.GetSelectionEnd()

        # tests if editing should succeed
        edit = not selection_start == selection_end and (selection_start >= self.carret_position_end and selection_end >= self.carret_position_end) or current_position >= self.carret_position_end

        # returns the edit flag
        return edit

    def can_remove(self):
        """
        Returns true if removal should succeed.

        @rtype: bool
        @return: The result of the removal test (if successful or not)
        """

        # retrieves the current position
        current_position = self.GetCurrentPos()

        # retrieves the selection start
        selection_start = self.GetSelectionStart()

        # retrieves the selection end
        selection_end = self.GetSelectionEnd()

        # tests if removal should succeed
        remove = not selection_start == selection_end and (selection_start >= self.carret_position_end and selection_end >= self.carret_position_end) or current_position > self.carret_position_end

        # returns the remove flag
        return remove

    def on_char(self, event):
        # skips the event
        event.Skip()

    def on_key_down(self, event):
        """
        Handler for the key down event.

        @type event: Event
        @param event: The triggered event
        """

        # retrieves the keycode for the key pressed
        key = event.GetKeyCode()

        # retrieves the current end position
        current_end_position = self.GetTextLength()

        # retrieves the control down status
        control_down = event.ControlDown()

        # retrieves the shift down status
        shift_down = event.ShiftDown()

        # checks if edition is allowed
        can_edit = self.can_edit()

        # in case the enter (or return) key has been pressed
        if key in RETURN_KEYS and can_edit:
            # retrieves the current line and position
            current_line, _position = self.GetCurLine()

            # moves the caret to the last position of the text
            self.SetCurrentPos(current_end_position)

            # removes the caret and the space from the current line
            current_line_no_caret = current_line.replace(">>> ", "")

            # writes a newline character
            self.write("\n")

            # processes the command in the console engine
            self.console_plugin.process_command_line(current_line_no_caret, self.write_new_line)

            # writes the newline caret
            self.write_caret()
        # in case any of the navigation keys has been pressed
        elif key in NAVIGATION_KEYS:
            # skips the event
            event.Skip()
        # in case the backspace key has been pressed
        elif key == wx.WXK_BACK:
            # skips the event in case removal is possible
            self.can_remove() and event.Skip()
        # in case the control key is pressed and c is also pressed (copy)
        elif control_down and not shift_down and key in (ord('C'), ord('c'), wx.WXK_INSERT):
            # copies the text
            self.copy()
        # in case any other key has been pressed
        elif can_edit:
            # skips the event
            event.Skip()

    def copy(self):
        """
        Copies the current selection and place it on the clipboard.
        """

        # retrieves the selected text
        selected_text = self.GetSelectedText()

        # retrieves the selected text data
        selected_text_data = wx.TextDataObject(selected_text)

        # copies the selected text data to the clipboard
        self._clip(selected_text_data)

    def _clip(self, data):
        """
        Copies the given data to the clipboard.

        @type data: DataObject
        @param data: The data to be copied to the clipboard
        """

        # checks if the clipboard is open
        clipboard_open = wx.TheClipboard.Open()

        # in case the clipboard is not open
        if not clipboard_open:
            # returns
            return

        # sets the data in the clipboard
        wx.TheClipboard.UsePrimarySelection(False)
        wx.TheClipboard.SetData(data)
        wx.TheClipboard.Flush()
        wx.TheClipboard.Close()
