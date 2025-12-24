# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

* Hi-Lo generator strategy (`generator_type="hilo"`) for entity ID generation that reduces database contention by pre-allocating ID pools
* New `HILO_POOL_SIZE` constant (default: 100) for configuring pool size globally
* Support for per-field pool size customization via `generator_pool_size` attribute
* Thread-safe pool management with local locking that only accesses the database during pool allocation

### Changed

*

### Fixed

*
