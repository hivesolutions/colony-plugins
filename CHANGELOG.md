# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

* New `get_connection_address()` method in `RESTRequest` with proxy header resolution (`X-Forwarded-For`, `X-Client-IP`, `X-Real-IP`) and IPv6-mapped IPv4 cleanup (`::ffff:` prefix removal)
* New `get_connection_address()` method in `HTTPRequest` and `WSGIRequest` to provide a uniform interface for retrieving client connection address
* Optional `resolve` and `cleanup` parameters in `RESTRequest.get_address()` for controlling proxy resolution and IPv6 cleanup
* Tests for `get_connection_address()`, `get_address()`, and `get_port()` across REST, service HTTP, and WSGI modules
* Exception handling in `validated` decorator to catch `ControllerValidationError` raised during function execution and route to `validation_failed` handler
* Tests for the `validated` decorator covering pre-validation failures, in-function exception catching, re-raise behavior, and flag management
* New AT invoice management methods in ATClient: `change_invoice_status()`, `delete_invoice()`, `query_invoices()`, and `get_at_invoices()` for complete invoice lifecycle management
* New constants for AT invoice query operations: `QUERY_BASE_URL`, `QUERY_BASE_TEST_URL`, and `QUERY_WSDL_URL`
* Tests for `get_at_invoices()` method covering both populated and empty invoice responses
* Method `get_certificate_common_name()` in ATClient to extract the Common Name (CN) from the certificate's subject field
* Support for context-specific ASN.1 types in BER library, enabling X.509 certificate parsing
* Bit string padding removal implementation in BER library
* Test case for certificate PEM loading in PKCS1 module
* Regression tests for session GC and translate_result fixes in REST plugin

### Changed

* Service polling in `service_utils` now auto-selects the best available mechanism: `epoll` on Linux, `kqueue` on BSD/macOS, `poll` on other Unix systems, and `select` as fallback
* Implemented `EpollPolling` using `select.epoll()`, `KqueuePolling` using `select.kqueue()`, and `Epoll2Polling` using `select.poll()` as alternatives to `SelectPolling`, removing the 1024 file descriptor limit on supported platforms
* Client I/O polling in `client_utils` now uses the same platform-aware strategy via a new `poll_socket()` function, replacing direct `select.select()` calls in `_receive()` and `_send()` and removing the 1024 fd limit for epoll/kqueue/poll backends while preserving the guard for the `select` fallback

### Fixed

* Socket file descriptor leak in `client_utils` caused by unbounded reconnection attempts in `_send()`, stale socket references in `_reconnect_connection_socket()`, and missing cleanup of closed connections in `get_client_connection()` that could lead to "filedescriptor out of range in select()" errors
* Added unit tests for `poll_socket()`, `ClientConnection` lifecycle, I/O paths, and `_process_exception()` in `client_utils`; extended `MockSocket` with `fileno()`, close tracking, and configurable recv/send data
* Socket file descriptor leak in `service_utils` where accepted sockets could be orphaned when handler exceptions occurred for pending (handshake) or partially registered connections, and where `remove_socket()` could skip cleanup on missing map entries
* Race condition in `RESTSession.gc()` and `ShelveSession.gc()` that caused `RuntimeError: dictionary changed size during iteration` when expiring sessions during garbage collection
* Missing return statement in `REST.translate_result()` that caused the method to not return a value when no encoder name was specified
* Incorrect `super()` call in `RedisSession.unload()` that referenced `ShelveSession` instead of `RedisSession`
* Added type validation for unpickled sessions in `RedisSession.get_s()` to prevent potential security issues from malformed session data
* BER unpacker now properly handles unknown type numbers by falling back to sequence (constructed) or octet string (primitive) unpacking
* Certificate DER parsing now correctly extracts RSA public key from SubjectPublicKeyInfo structure
* Certificate parser now handles optional version field correctly, supporting both v1 certificates (no version) and v2/v3 certificates
