# pyProfileMgr <!-- omit in toc -->

pyProfileMgr is a Python module containing the Profile Manager component.

It also provides CLI access for reading, writing, listing and updating profiles.
A profile contains server URL, type, credentials (token or username/password) and certificate data.

[![License](https://img.shields.io/badge/license-bsd-3.svg)](https://choosealicense.com/licenses/bsd-3-clause/) [![Repo Status](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip) [![CI](https://github.com/NewTec-GmbH/pyProfileMgr/actions/workflows/test.yml/badge.svg)](https://github.com/NewTec-GmbH/pyProfileMgr/actions/workflows/test.yml)

- [Overview](#overview)
- [Installation](#installation)
- [SW Documentation](#sw-documentation)
- [Used Libraries](#used-libraries)
- [Issues, Ideas And Bugs](#issues-ideas-and-bugs)
- [License](#license)
- [Contribution](#contribution)

## Overview

![overview](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/NewTec-GmbH/pyProfileMgr/main/doc/uml/overview.puml)

More information on the deployment and architecture can be found in the [doc](./doc/README.md) folder.

## Installation

```bash
git clone https://github.com/NewTec-GmbH/pyProfileMgr.git
cd pyProfileMgr
pip install .
```

## SW Documentation

More information on the deployment and architecture can be found in the [documentation](./doc/README.md)

For Detailed Software Design run `$ /doc/detailed-design/make html` to generate the detailed design documentation that then can be found
in the folder `/doc/detailed-design/_build/html/index.html`

## Used Libraries

Used 3rd party libraries which are not part of the standard Python package:

| Library | Description | License |
| ------- | ----------- | ------- |
| [colorama](https://github.com/tartley/colorama) | ANSI color support | BSD-3 License |
| [toml](https://github.com/uiri/toml) | Parsing [TOML](https://en.wikipedia.org/wiki/TOML) | MIT |

Sections below, for Github only

## Issues, Ideas And Bugs

If you have further ideas or you found some bugs, great! Create an [issue](https://github.com/NewTec-GmbH/pyProfileMgr/issues) or if you are able and willing to fix it by yourself, clone the repository and create a pull request.

## License

The whole source code is published under [BSD-3-Clause](https://github.com/NewTec-GmbH/pyProfileMgr/blob/main/LICENSE).
Consider the different licenses of the used third party libraries too!

## Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, shall be licensed as above, without any additional terms or conditions.
