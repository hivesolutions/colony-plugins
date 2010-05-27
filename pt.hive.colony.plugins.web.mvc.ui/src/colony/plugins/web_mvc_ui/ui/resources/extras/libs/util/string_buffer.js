// Take The Bill Service
// Copyright (C) 2010 Hive Solutions Lda.
//
// This file is part of Take The Bill Service.
//
// Take The Bill Service is confidential and property of Hive Solutions Lda,
// its usage is constrained by the terms of the Hive Solutions
// Confidential Usage License.
//
// Take The Bill Service should not be distributed under any circumstances,
// violation of this may imply legal action.
//
// If you have any questions regarding the terms of this license please
// refer to <http://www.hive.pt/licenses/>.

// __author__    = João Magalhães <joamag@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision$
// __date__      = $LastChangedDate$
// __copyright__ = Copyright (c) 2010 Hive Solutions Lda.
// __license__   = Hive Solutions Confidential Usage License (HSCUL)

function StringBuffer() {
    this.buffer = [];
}

StringBuffer.prototype.append = function(string) {
    this.buffer.push(string);
    return this;
}

StringBuffer.prototype.removeLastAppend = function(string) {
    this.buffer[this.buffer.size() - 1] = "";
    return this;
}

StringBuffer.prototype.toString = function() {
    return this.buffer.join("");
}
