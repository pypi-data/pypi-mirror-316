# Changelog

## Version 0.3.0

- chore: Remove Python 3.8 (EOL)
- precommit: Replace docformatter with ruff's formatter

## Version 0.2.8

- Set dependency for `scipy`. Seems like the hstack and vstack functions
have been updated in 1.13.0+.

## Version 0.2.0 - 0.2.7

- Support multi apply
- Add tests and documentation
- Sync package with the rest of the BiocPy

## Version 0.1 (development)

- first release
- performs some basic operations over numpy or scipy matrices.
- provides apply method so user can extend the underlying logic to any function
