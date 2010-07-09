// Hive Colony Framework
// Copyright (C) 2008 Hive Solutions Lda.
//
// This file is part of Hive Colony Framework.
//
// Hive Colony Framework is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Hive Colony Framework is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

// __author__    = João Magalhães <joamag@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision: 9229 $
// __date__      = $LastChangedDate: 2010-07-08 18:07:05 +0100 (qui, 08 Jul 2010) $
// __copyright__ = Copyright (c) 2008 Hive Solutions Lda.
// __license__   = GNU General Public License (GPL), Version 3

/**
 * Constructor of the class.
 */
function StringBuffer() {
    // creates the buffer to hold the (partial) strings
    this.buffer = [];
}

/**
 * Clears the current string buffer
 *
 * @return {Object} The current context.
 */
StringBuffer.prototype.clear = function(string) {
    // creates a new buffer, simulating the clearing of the previous
    this.buffer = [];

    // returns the context
    return this;
}

/**
 * Adds a string to the string buffer.
 *
 * @param {String}
 *            string The string to be added to the buffer.
 * @return {Object} The current context.
 */
StringBuffer.prototype.append = function(string) {
    // adds the string to the buffer
    this.buffer.push(string);

    // returns the context
    return this;
}

/**
 * Updates the buffer to a "new" buffer with the given value.
 *
 * @param {String}
 *            string The string to be used in the creation of the "new" buffer.
 * @return {Object} The current context.
 */
StringBuffer.prototype.replace = function(string) {
    // clears the read buffer
    this.clear();

    // adds the string to the read buffer
    this.append(string);

    // returns the context
    return this;
}

/**
 * Removes the last added string.
 *
 * @return {Object} The current context.
 */
StringBuffer.prototype.removeLastAppend = function() {
    // sets the last element as not valid (empty)
    this.buffer[this.buffer.size() - 1] = "";

    // returns the context
    return this;
}

/**
 * Converts the internal string buffer to a string.
 *
 * @return {String} The converted string value.
 */
StringBuffer.prototype.toString = function() {
    // returns the joined value of the strings
    // in the buffer
    return this.buffer.join("");
}
