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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

def invertDict(dict):
    d = {}

    for k, v in dict.items():
        d[v] = k

    return d

class NS:
    """
    The namespace class.
    """

    XML = "http://www.w3.org/XML/1998/namespace"

    ENV = "http://schemas.xmlsoap.org/soap/envelope/"
    ENC = "http://schemas.xmlsoap.org/soap/encoding/"

    XSD = "http://www.w3.org/1999/XMLSchema"
    XSD2 = "http://www.w3.org/2000/10/XMLSchema"
    XSD3 = "http://www.w3.org/2001/XMLSchema"

    XSD_L = [XSD, XSD2, XSD3]
    EXSD_L = [ENC, XSD, XSD2, XSD3]

    XSI = "http://www.w3.org/1999/XMLSchema-instance"
    XSI2 = "http://www.w3.org/2000/10/XMLSchema-instance"
    XSI3 = "http://www.w3.org/2001/XMLSchema-instance"
    XSI_L = [XSI, XSI2, XSI3]

    URN = "http://soapinterop.org/xsd"

    # for generated messages
    XML_T = "xml"
    ENV_T = "SOAP-ENV"
    ENC_T = "SOAP-ENC"
    XSD_T = "xsd"
    XSD2_T = "xsd2"
    XSD3_T = "xsd3"
    XSI_T = "xsi"
    XSI2_T = "xsi2"
    XSI3_T = "xsi3"
    URN_T = "urn"

    NSMAP = {ENV_T: ENV, ENC_T: ENC, XSD_T: XSD, XSD2_T: XSD2,
             XSD3_T: XSD3, XSI_T: XSI, XSI2_T: XSI2, XSI3_T: XSI3,
             URN_T: URN}
    NSMAP_R = invertDict(NSMAP)

    STMAP = {"1999" : (XSD_T, XSI_T), "2000" : (XSD2_T, XSI2_T), "2001" : (XSD3_T, XSI3_T)}
    STMAP_R = invertDict(STMAP)

    def __init__(self):
        raise Error, "Don't instantiate this"
