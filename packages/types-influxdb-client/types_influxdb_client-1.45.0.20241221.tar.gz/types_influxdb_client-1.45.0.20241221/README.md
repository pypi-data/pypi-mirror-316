## Typing stubs for influxdb-client

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`influxdb-client`](https://github.com/influxdata/influxdb-client-python) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `influxdb-client`. This version of
`types-influxdb-client` aims to provide accurate annotations for
`influxdb-client==1.45.*`.

Note: `types-influxdb-client` has required `urllib3>=2` since v1.37.0.1. If you need to install `types-influxdb-client` into an environment that must also have `urllib3<2` installed into it, you will have to use `types-influxdb-client<1.37.0.1`.

*Note:* The `influxdb-client` package includes type annotations or type stubs
since version 1.46.0. Please uninstall the `types-influxdb-client`
package if you use this or a newer version.


This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/influxdb-client`](https://github.com/python/typeshed/tree/main/stubs/influxdb-client)
directory.

This package was tested with
mypy 1.14.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`097581ea47d0fd77f097c88d80d5947e0218d9c4`](https://github.com/python/typeshed/commit/097581ea47d0fd77f097c88d80d5947e0218d9c4).