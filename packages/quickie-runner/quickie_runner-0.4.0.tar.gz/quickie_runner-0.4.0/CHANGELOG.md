# Quickie Change Log

## Release 0.1.0

- Initial release.

## Release 0.2.0

### Added

- Create tasks from functions.
- Add arguments to the parser of tasks via decorators.
- Define tasks that must run before or after another task.
- Define cleanup tasks for a task.
- Allow conditions for running tasks.
- Define partial tasks.
- Load from another task by name.

### Changed

- Renamed classes and parameters for clarity.
- Removed support for file-based configuration in favor of environment variables.
- Removed `-g` argument in favor of separate global runner.

## Release 0.2.1

Fixes for global runner.

## Release 0.2.2

Fixes for global runner.

## Release 0.3.0

### Changed

- Removed Task.Meta and Task.DefaultMeta in favor of configuration in the task class.
- Task names inferred from class name preserve the case.
- Refactored and moved things around.
- Task classes starting with an underscore are now considered private by default.
- Namespace tasks using the `NAMESPACES` attribute instead of `QCK_NAMESPACES`.
- `NAMESPACES` (previously `QCK_NAMESPACES`) now also accepts a list of modules to load for
  a single namespace.

## Release 0.3.1

### Changed

- fix quickie-runner-global dependencies


## Release 0.3.2

### Added

- Listing tasks also shows the file and line where the task is defined.

### Fixed

- Fix bug causing tasks the help message for tasks to not include the docstring.


## Release 0.3.3

### Changed

- Tasks are listed sorted by location, and grouped by class, creating a new table for aliases.


## Release 0.4.0

### Changed

- NAMESPACES now accepts and ignores null values.
- Command now accepts unix style command strings.
- Script now allows defining the executable
- Cleaner exit on keyboard interrupt.
- Changed command from `qck` and `qckg` to `qk` and `qkg`.
