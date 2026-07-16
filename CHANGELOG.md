# Changelog

## 0.2.1 - 2026-07-16

### Changed
- Added old-reph.

## 0.2.0 - 2026-07-16

### Changed
- Removed an external dependency from the transliteration pipeline to simplify installation and reduce runtime requirements.

## 0.1.1 - 2026-07-15

### Fixed
- Improved transliteration handling for Malayalam words ending in virama-driven suffixes.
- Reduced unwanted trailing `u` artifacts in outputs such as `മേഖലയാണ്`.

### Added
- Added regression coverage for Malayalam suffix handling in the test suite.
