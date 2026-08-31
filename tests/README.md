# Tests

Tests should focus on boundaries:

- B construct -> intermediate/threaded representation
- PDP-11 assembly -> words
- runtime operator -> machine behavior
- tape record -> decoded bytes/checksum
- PDP-7-produced tape -> PDP-11-loaded memory

End-to-end tests should preserve provenance and identify any modern instrumentation involved.
