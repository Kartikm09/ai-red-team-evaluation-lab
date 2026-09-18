# Verified repair scope

The starting source was `b7fb15f166c65fa1f4f3cda76e97a1142364f4e7`. The bundled example commands completed,
but there was no automated assertion suite. Bounded synthetic input probes
exposed the defect addressed here.

Reject missing/invalid reviewer scores rather than inventing0 or accepting100.

New regression tests failed before the repair. After the change, `make verify`
passed 3 test methods, including independent result oracles and negative
command-line cases. Every original documented sample command was rerun. Test
counts are methods; parameterized inputs are not inflated into separate tests.

The tests use the standard library and synthetic fixtures. They do not claim
comprehensive schema validation, real model quality, external evidence quality,
or production readiness. CI repeats the discoverable verification command.
