# Changelog[^1]

All notable changes to Pekora will be documented here. Breaking changes are marked with a 🚩.

Pekora adheres to [semantic versioning](https://semver.org/spec/v2.0.0.html).

## <a name="1-0-5">[1.0.5] - 2023-03-16</a>

### Changed

- `pekora calc` can no longer return a negative result. Results that would have previously been negative are now clamped
  to 0.

## <a name="1-0-4">[1.0.4] - 2023-03-14</a>

No user-facing changes are introduced in this release.

## <a name="1-0-3">[1.0.3] - 2023-03-14</a>

### Fixed

- Fixed a bug where passing negative numbers to `pekora read` or `pekora make --from` would cause an error.

## <a name="1-0-2">[1.0.2] - 2023-03-13</a>

### Fixed

- Fixed a bug where subtracting permissions could return an incorrect result if the difference of the permissions'
  integer values was a negative number.

## <a name="1-0-1">[1.0.1] - 2023-03-12</a>

No user-facing changes are introduced in this release.

## <a name="1-0-0">[1.0.0] - 2023-03-12</a>

This is the initial release of Pekora.

[^1]: Based on [Keep a Changelog](https://keepachangelog.com).
