<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: GPL-2.0-or-later
-->

# Changelog

All notable changes to the tina project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.13] - 2024-12-22

### Fixes

- Use `AC_SYS_LARGEFILE` in the configure script instead of relying on
  getconf(1): the latter may even be wrong when cross-building

### Additions

- Add a basic unit tests suite
- Add a `tina-convert` tool for exporting and importing the tina
  database into JSON and YAML
- Add some `MkDocs` documentation

## [0.1.12] - 2016-04-12

### Fixes

- Refresh the autotools packaging files
- Remove the arguments from the `AM_INIT_AUTOMAKE` invocation
- Fix some compiler warnings

### Additions

- Let the configure script also add `-Wstrict-prototypes` if possible
- Let the configure script check for Large File Support
- Add some copyright notices

### Other changes

- Adopted by Peter Pentchev

## [0.1.11] - 2007-08-16

### Other changes

- Last release within Debian by Matt Kraai

[Unreleased]: https://gitlab.com/tina-mgr/tina-mgr/-/compare/release%2F0.1.13...master
[0.1.13]: https://gitlab.com/tina-mgr/tina-mgr/-/tags/release%2F0.1.13
[0.1.12]: https://gitlab.com/tina-mgr/tina-mgr/-/tags/release%2F0.1.12
[0.1.11]: https://gitlab.com/tina-mgr/tina-mgr/-/tags/debian%2F0.1.11
