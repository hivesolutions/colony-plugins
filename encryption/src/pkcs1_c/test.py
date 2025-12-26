#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2024 Hive Solutions Lda.
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

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os

import colony


class PKCS1Test(colony.Test):
    """
    The PKCS1 infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (PKCS1BaseTestCase,)

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

        manager = self.plugin.manager
        system = self.plugin.system

        plugin_path = manager.get_plugin_path_by_id(self.plugin.id)
        resources_path = os.path.join(plugin_path, "ssl_c", "resources")

        test_case.private_path = os.path.join(resources_path, "private.key")
        test_case.public_path = os.path.join(resources_path, "public.key")

        test_case.pkcs1 = system.create_structure({})

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)

        test_case.private_path = None
        test_case.public_path = None
        test_case.pkcs1 = None


class PKCS1BaseTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "PKCS1 Base test case"

    def test_load_certificate_pem(self):
        certificate = self.pkcs1.load_certificate_pem(
            """-----BEGIN CERTIFICATE-----
MIIIiTCCBnGgAwIBAgITNwAAADtjHvNQBL8xtgAAAAAAOzANBgkqhkiG9w0BAQsF
ADBHMRUwEwYKCZImiZPyLGQBGRYFbG9jYWwxFTATBgoJkiaJk/IsZAEZFgVyaXR0
YTEXMBUGA1UEAxMOQVQgSXNzdWluZyBDQTIwHhcNMjUwNDE1MDczODU4WhcNMjcw
NDE1MDc0ODU4WjCBnTELMAkGA1UEBhMCUFQxDzANBgNVBAgTBkxpc2JvYTEPMA0G
A1UEBxMGTGlzYm9hMSowKAYDVQQKEyFBdXRvcmlkYWRlIFRyaWJ1dGFyaWEgZSBB
ZHVhbmVpcmExHzAdBgNVBAsTFlNpc3RlbWFzIGRlIEluZm9ybWFjYW8xHzAdBgNV
BAMTFkNoYXZlIENpZnJhIFB1YmxpY2EgQVQwggIiMA0GCSqGSIb3DQEBAQUAA4IC
DwAwggIKAoICAQDEsF/ynpM8LYortcvmrrzVDN9vXn6rqZNTw1UWAAW1hJsbc3k2
IyYXh32ITN1vFTC6eXrkakhwx9bwdXrUhrZK5iAiNYy/xrReQTzZm7gMj63wJo9e
rJp8CN2S3tdUdhFHWo07QSXhH+Vl/7/tDBfOQVAObdlguigP81IjhPQYLuXq5Q3W
74TESKGiz/x+I/+Jt5I+IRokFqRMWFXZLqSaLqiIsTN8H/4xDatujPbgI6p0BLAl
86+M130M3Jz3w3o6+6kScpGcyTvzKnZYTGfUOvAptvxNuu0/8MgzXICI+MqkLKjF
X49y9D1mlKwN+wFT5i2H1q3qn1OlcglOL9QN1yN3qAOdJdotpcFSFsFjn7iOn6ED
dKyUdb4tensIh4NjvswlbLTn/WMQGeKM8QW4VtmgyHlEXfsPjAO+BOKM+OibHZhE
GEYsGH2844mz3oUZoY4ubBpvif6zvi8wv6SPUVRkxIVF/TKBhnkX28pA6tCNGotG
nnNwO0K3L3pYjqeQGFgSRP6lxNgvycUO75u45lDlUttsLtRVvYWv4ep2EkcTTpuU
A7qAb2450V1M3QYmlwVD8q2A81y8KzLBNwucUTwdZ7oi7Ui1qAjvOfS0HZZO0RMu
H7btnNB/gH+trFv+UHE5MKUDAL/8iv1ffbccDRJ30kqKB2VfinCAzHMjOQIDAQAB
o4IDFTCCAxEwCwYDVR0PBAQDAgQwMD0GCSsGAQQBgjcVBwQwMC4GJisGAQQBgjcV
CIKNnTmCjuwqhP2TE4L21W6Cmb9zUoLygWWG+p8uAgFkAgEcMEQGCSqGSIb3DQEJ
DwQ3MDUwDgYIKoZIhvcNAwICAgCAMA4GCCqGSIb3DQMEAgIAgDAHBgUrDgMCBzAK
BggqhkiG9w0DBzAdBgNVHQ4EFgQUXZ1TUXUSifWjgywNK7Exb21VjsQwHwYDVR0j
BBgwFoAUUG1ppVaG6wzOUa0w0LXKXhevZ7gwggEBBgNVHR8EgfkwgfYwgfOggfCg
ge2GgbpsZGFwOi8vL0NOPUFUJTIwSXNzdWluZyUyMENBMixDTj1zdzUwMDI2MixD
Tj1DRFAsQ049UHVibGljJTIwS2V5JTIwU2VydmljZXMsQ049U2VydmljZXMsQ049
Q29uZmlndXJhdGlvbixEQz1yaXR0YSxEQz1sb2NhbD9jZXJ0aWZpY2F0ZVJldm9j
YXRpb25MaXN0P2Jhc2U/b2JqZWN0Q2xhc3M9Y1JMRGlzdHJpYnV0aW9uUG9pbnSG
Lmh0dHA6Ly9wa2kuYXQuZ292LnB0L0NlcnREYXRhL0FUSXNzdWluZ0NBMi5jcmww
ggEABggrBgEFBQcBAQSB8zCB8DCBsQYIKwYBBQUHMAKGgaRsZGFwOi8vL0NOPUFU
JTIwSXNzdWluZyUyMENBMixDTj1BSUEsQ049UHVibGljJTIwS2V5JTIwU2Vydmlj
ZXMsQ049U2VydmljZXMsQ049Q29uZmlndXJhdGlvbixEQz1yaXR0YSxEQz1sb2Nh
bD9jQUNlcnRpZmljYXRlP2Jhc2U/b2JqZWN0Q2xhc3M9Y2VydGlmaWNhdGlvbkF1
dGhvcml0eTA6BggrBgEFBQcwAoYuaHR0cDovL3BraS5hdC5nb3YucHQvQ2VydERh
dGEvQVRJc3N1aW5nQ0EyLmNydDAVBgNVHSUEDjAMBgorBgEEAYI3CgMEMB0GCSsG
AQQBgjcVCgQQMA4wDAYKKwYBBAGCNwoDBDANBgkqhkiG9w0BAQsFAAOCAgEAYNG/
qRzmTTuRP+3HyjK8Xw43GXhui4tnRX3eqmoyZ0xFwhh9G+9FONaFgKnk0XAbDUVr
EX09DZ2VpTTL+fMgH2kGCiOgdXFw4TfzqzrDCSUxmDnlcv7ea+tO6PG9tqc4izdA
RsnFZhxKgI1Lt3RZN+9bnWVzgseANRB/IUgzRnN7TIZLIpbwBr7N/sx7pcF1+yxm
0I5tkMb0YkitDq4bhUb/JqCz2tHh2gzqZz1b2aSObs8ylvN8OALidiTqpG4pR4EU
SD+N7szy5B56PimvYsAd7dDs3bVKOOV4/v4YTxVCrHPgBwmwt2S85Ql7wdr2qg0I
/q7BhHFi8KLfATne3sMRTamA+hxT+mS/iUF7FBxedLHmu5xflVcu1xHBUPq4QP1A
JQ4Nq5OGLMDD0SP8ZERoHJMnDpI9NMGaQXYVoKsstPgUwVRRT7eFw+44NsJeIbd2
/7E+qaIyyaXpzXZwpM8Y/dRXfFxa3E5Onn33eYb0WNYPYKp0/zqVsE6kCitGS3jt
sh1MoR6OVGfW8+ZyIsyrOSXaePw2s+LsM+A/DNOaovUTfer3n5fGmeAbAtic/ATf
oipvlTLirPGg9lDEgWUsElTmJdNsXKpXmndICSSSmYWf1rEg6XDHSGLpn502RATM
dJ996JOFis6KMdzf/FUNNORTOObJsP4JZRmfn6o=
-----END CERTIFICATE-----"""
        )

        # verifies that certificate was loaded and contains expected structure
        self.assertNotEqual(certificate, None)
        self.assertEqual(type(certificate), dict)

        # verifies all expected keys are present in the certificate
        self.assertTrue("version" in certificate)
        self.assertTrue("serial_number" in certificate)
        self.assertTrue("signature_algorithm" in certificate)
        self.assertTrue("issuer" in certificate)
        self.assertTrue("not_before" in certificate)
        self.assertTrue("not_after" in certificate)
        self.assertTrue("subject" in certificate)
        self.assertTrue("public_key" in certificate)

        # verifies version is v3 (value 2, since 0=v1, 1=v2, 2=v3)
        self.assertEqual(certificate["version"], 2)

        # verifies the serial number matches the expected value
        self.assertEqual(
            certificate["serial_number"],
            1226540986227540198135250146913179895272046651,
        )

        # verifies the signature algorithm is SHA256 with RSA (OID 1.2.840.113549.1.1.11)
        self.assertEqual(
            certificate["signature_algorithm"], (1, 2, 840, 113549, 1, 1, 11)
        )

        # verifies the validity period (UTCTime format: YYMMDDHHMMSSZ)
        self.assertEqual(certificate["not_before"], "250415073858Z")
        self.assertEqual(certificate["not_after"], "270415074858Z")

        # verifies issuer and subject are present and are lists
        self.assertEqual(type(certificate["issuer"]), list)
        self.assertEqual(type(certificate["subject"]), list)

        # verifies public key structure (tuple with public_key, private_key, extras)
        public_key = certificate["public_key"]
        self.assertEqual(type(public_key), tuple)
        self.assertEqual(len(public_key), 3)

        # verifies the RSA public key has correct values
        public_key_data = public_key[0]
        self.assertEqual(public_key_data["e"], 65537)
        self.assertEqual(public_key_data["n"].bit_length(), 4096)
