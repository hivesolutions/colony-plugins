# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

* Support for context-specific ASN.1 types in BER library, enabling X.509 certificate parsing
* Bit string padding removal implementation in BER library
* Test case for certificate PEM loading in PKCS1 module

### Fixed

* BER unpacker now properly handles unknown type numbers by falling back to sequence (constructed) or octet string (primitive) unpacking
* Certificate DER parsing now correctly extracts RSA public key from SubjectPublicKeyInfo structure
* Certificate parser now handles optional version field correctly, supporting both v1 certificates (no version) and v2/v3 certificates
