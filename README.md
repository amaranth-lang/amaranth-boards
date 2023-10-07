# Board definitions for Amaranth HDL

The Amaranth Board Definitions contain platform specific information for deploying Amaranth projects onto readily available and common FPGA hardware. The boards defined within this repository are listed within `amaranth_boards/`.

*TODO: describe a typical board file, or point to general Amarnath documentation.*

For a quick reference of the boards described by this repository, reference the [Boards Table](docs/boards_table.md) or see the board sources defined in [`amaranth_boards/`](amaranth_boards/) directly.

## Installation

After following the setup instructions for the core [Amaranth HDL tool chain](https://amaranth-lang.org/docs/amaranth/latest/install.html), the `amaranth_boards` package can be installed in the same location as site-packages or dist-packages. The boards package follows a conventional setup process for a source based python package.

### Setup Requirements

This guide assumes a supported version of Python and `pip` are available on the host system. Reference the [Amaranth HDL documentation](https://amaranth-lang.org/docs/amaranth/latest/install.html) for specific versions and detailed setup instructions for for python and pip.

Prior to attempting to install the boards package, ensure your system has the required setuptools packages available.

- `setuptools` > 67.0
- `setuptools_scm[toml]` > 6.2

If you find you are missing either setuptools package, running the following command should install them locally assuming `pip` is available.

```bash
pip install setuptools setuptools_scm[toml]
```

### Local Installation

Either clone a copy of the source code from the repository, or download a bundled copy of the current `main` branch from the releases on this page. From within the root directory of the repository run the following command to install the current release of the boards package to the current user's python packages directory.

```bash
pip install --user .
```

## License

Amaranth is released under the very permissive two-clause BSD license. Under the terms of this license, you are authorized to use Amaranth for closed-source proprietary designs.

See LICENSE file for full copyright and license info.
