# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

* Method `get_certificate_common_name()` in ATClient to extract the Common Name (CN) from the certificate's subject field
* Support for context-specific ASN.1 types in BER library, enabling X.509 certificate parsing
* Bit string padding removal implementation in BER library
* Test case for certificate PEM loading in PKCS1 module
* Regression tests for session GC and translate_result fixes in REST plugin

### Fixed

* Race condition in `RESTSession.gc()` and `ShelveSession.gc()` that caused `RuntimeError: dictionary changed size during iteration` when expiring sessions during garbage collection
* Missing return statement in `REST.translate_result()` that caused the method to not return a value when no encoder name was specified
* Incorrect `super()` call in `RedisSession.unload()` that referenced `ShelveSession` instead of `RedisSession`
* Added type validation for unpickled sessions in `RedisSession.get_s()` to prevent potential security issues from malformed session data
* BER unpacker now properly handles unknown type numbers by falling back to sequence (constructed) or octet string (primitive) unpacking
* Certificate DER parsing now correctly extracts RSA public key from SubjectPublicKeyInfo structure
* Certificate parser now handles optional version field correctly, supporting both v1 certificates (no version) and v2/v3 certificates
