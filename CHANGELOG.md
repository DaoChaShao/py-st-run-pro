<!-- insertion marker -->
<a name="0.1.0"></a>

## [0.1.0](https://github.com/DaoChaShao/py-st-run-pro/compare/5269934d43e0aff64830b13db930ff14b6cca7a5...0.1.0) (2026-11-05)

### Features

- **dbk:** implement SQLAlchemy engine initialization and database operations ([cea2f0e](https://github.com/DaoChaShao/py-st-run-pro/commit/cea2f0e8ce2e135884927f2ab296d03ec5e912d3))
- **dbk:** add DBConfig and engine utilities to public API ([bbc2ac5](https://github.com/DaoChaShao/py-st-run-pro/commit/bbc2ac5eaae80e98cbe94d3826799195be915ae5))
- update the data ([2d0095e](https://github.com/DaoChaShao/py-st-run-pro/commit/2d0095e36f9e250fffc9162828af476a966f4deb))
- **dbk:** add engines module skeleton ([1d99e7f](https://github.com/DaoChaShao/py-st-run-pro/commit/1d99e7f4c25feea11eb26fdcab0a215cd13dc26c))
- **dbk:** add SQLite database path constants ([60af501](https://github.com/DaoChaShao/py-st-run-pro/commit/60af501493b03f66df29e8a529bf152fe6c636a1))
- **dbk:** add database configuration dataclass ([3ae956d](https://github.com/DaoChaShao/py-st-run-pro/commit/3ae956d5c0fb9e572da4f4e2a9ae7f6918bcadd8))
- **dbk:** add SQLAlchemy declarative base for dbk module ([71e811a](https://github.com/DaoChaShao/py-st-run-pro/commit/71e811af43a4e739614ff7ea989e32ec530cb08a))
- **dbk:** add database core package initialization ([70ed94e](https://github.com/DaoChaShao/py-st-run-pro/commit/70ed94e2a5530eb30985c42c0c12a0bb875b2b9b))
- **main:** implement tabular data loading in main function ([790448a](https://github.com/DaoChaShao/py-st-run-pro/commit/790448adb0e86dab1383b757ebb14be52896e927))
- **types:** add FeatureScalers enum and remove TabularFormats ([90a11a0](https://github.com/DaoChaShao/py-st-run-pro/commit/90a11a09c764791d86c3b2f777f91c723618093f))
- **stats:** add TabularFormats enum for output types ([2df27b5](https://github.com/DaoChaShao/py-st-run-pro/commit/2df27b5d102b404100745ca98c1e543df6dab078))
- **stats:** add preprocessor for label distribution and data loading ([e35ea4e](https://github.com/DaoChaShao/py-st-run-pro/commit/e35ea4e005fde15fb41d27421390ccc5665e6205))
- **stats:** add NumpySeed context manager and DataFrame summary helpers ([9bfd8dc](https://github.com/DaoChaShao/py-st-run-pro/commit/9bfd8dc453a9608ba2f8d5f144a67889b66a681b))
- **utils:** add core enum type definitions ([ffde4d4](https://github.com/DaoChaShao/py-st-run-pro/commit/ffde4d4b9afb345d79a6f82fb193b24ffc863227))
- **stats:** add file loader and random seed utilities ([c46deb3](https://github.com/DaoChaShao/py-st-run-pro/commit/c46deb33b75d034dee1d8ad83d7dfebe53e88c9c))
- **stats:** add stats module init with core utilities ([f797bb2](https://github.com/DaoChaShao/py-st-run-pro/commit/f797bb265abde11282daefc2be071fcb36f6f474))
- add running data ([8c6b383](https://github.com/DaoChaShao/py-st-run-pro/commit/8c6b3836645b062e8c1f33af03e2d47822ceae81))
- update dependencies throughout uv ([e19437d](https://github.com/DaoChaShao/py-st-run-pro/commit/e19437dfe0514b935792b347568761d512253363))
- **utils:** add terminal text highlighting utility module ([33c82e1](https://github.com/DaoChaShao/py-st-run-pro/commit/33c82e1bccbf6d9284c34dcb31528b6834a35ec6))
- **utils:** add context manager utility classes ([e5c637b](https://github.com/DaoChaShao/py-st-run-pro/commit/e5c637b0d8fd61d034c9759e2d2492659bd54027))
- **utils:** add decorator utils for timing and logging ([db238a3](https://github.com/DaoChaShao/py-st-run-pro/commit/db238a31376d58cd02d8c2dd79194328ff86726d))
- **utils:** add constants module with width configuration ([8f948d3](https://github.com/DaoChaShao/py-st-run-pro/commit/8f948d32c40696a5c602e92c30804939f01fbda1))
- **utils:** add package init with decorators and helpers ([b84fda2](https://github.com/DaoChaShao/py-st-run-pro/commit/b84fda22b252048aabc9555826ba21f85aaec0f8))

### Bug Fixes

- **dbk:** rename sqlite db file to sqlite3.db ([98f464a](https://github.com/DaoChaShao/py-st-run-pro/commit/98f464a7a5f067e063c25625b5aa9168dcb2aabe))
- **dbk:** resolve relative path in SQLite connection URL ([8cd3135](https://github.com/DaoChaShao/py-st-run-pro/commit/8cd31359a4efcf99ba5a09776d647483edbd11d5))

### Chore

- **deps:** add sqlalchemy dependency to lock file ([abc27dc](https://github.com/DaoChaShao/py-st-run-pro/commit/abc27dc843d65fce3d6ee93882b18a5b38ccac25))
- **deps:** add sqlalchemy dependency ([7c9af9b](https://github.com/DaoChaShao/py-st-run-pro/commit/7c9af9b68dee85154494e8e04d504daecae924c0))
- **dbk:** add .gitignore for Python and IDE files ([dae43c0](https://github.com/DaoChaShao/py-st-run-pro/commit/dae43c0195e146fb473cb5baaa141c575fc73184))
- **deps:** add openpyxl dependency for Excel file support ([6f54d70](https://github.com/DaoChaShao/py-st-run-pro/commit/6f54d70d0ae672a5cd5138155dd4b88df10e8536))
- **deps:** add openpyxl dependency for Excel file handling ([c56c25c](https://github.com/DaoChaShao/py-st-run-pro/commit/c56c25c9cd9a763bacd0392a7b9b57852778f637))
- **deps:** add access-modifiers package as dependency ([acd23e8](https://github.com/DaoChaShao/py-st-run-pro/commit/acd23e813a08067230e3bdb9c327f6f15e305c29))
- **deps:** add access-modifiers dependency ([bfac532](https://github.com/DaoChaShao/py-st-run-pro/commit/bfac5329f1103dd9bd1eea31cf16ffdbc686468d))
- **project:** add pyproject.toml for project configuration ([492ebe4](https://github.com/DaoChaShao/py-st-run-pro/commit/492ebe41dea305820fb40c5d942c5b8bd8fd0be5))
- **python:** add .python-version file to pin Python 3.12 ([fb885c5](https://github.com/DaoChaShao/py-st-run-pro/commit/fb885c5735c4fcbf766121f55ad291e6c0a2c02f))
- **config:** add .gitignore for Python and IDE files ([aac93bf](https://github.com/DaoChaShao/py-st-run-pro/commit/aac93bfa5746f6fdb0d5f580acf610b477569f63))
- **utils:** add .gitignore for Python project files ([f142c11](https://github.com/DaoChaShao/py-st-run-pro/commit/f142c11917a528fde65e92d0f60011a7662ab272))
- **data:** add .gitignore file for Python project ([ac6cdf0](https://github.com/DaoChaShao/py-st-run-pro/commit/ac6cdf01610587a525d925e0d1fbd2374727c2ee))

### Docs

- **changelog:** update CHANGELOG.md with new dbk entries ([7ff50fc](https://github.com/DaoChaShao/py-st-run-pro/commit/7ff50fc4b85c1520e49cc5b28367b4d4d5c3214c))
- **changelog:** update CHANGELOG.md with new entries ([9789cfb](https://github.com/DaoChaShao/py-st-run-pro/commit/9789cfbaf2235944d9412a55a96466a84e810a83))
- **changelog:** update changelog with recent feature and refactor ([3747d38](https://github.com/DaoChaShao/py-st-run-pro/commit/3747d387d501222115d8a791970469304b97a472))
- **changelog:** update CHANGELOG.md with recent feature and refactor entries ([7b2aa4d](https://github.com/DaoChaShao/py-st-run-pro/commit/7b2aa4db761e089cd8395e0979692d4cfff90138))
- **changelog:** add CHANGELOG.md for v0.1.0 ([5621b8a](https://github.com/DaoChaShao/py-st-run-pro/commit/5621b8a4e5d46a2e882f393abaa5c21b3ca6bccd))
- **readme:** add Chinese README with env setup and changelog ([3b2a26d](https://github.com/DaoChaShao/py-st-run-pro/commit/3b2a26d79d016bdcc08c697a819dfbe8e4cb8439))
- **readme:** add comprehensive project documentation ([ea44e27](https://github.com/DaoChaShao/py-st-run-pro/commit/ea44e27474bb57acd2846350462c9f686c935d0b))

### Code Refactoring

- **main:** switch data source to SQLite DB ([c7b7f24](https://github.com/DaoChaShao/py-st-run-pro/commit/c7b7f249c668b01d92bd3684764fe19cbcba84a5))
- **stats:** redesign TabularLoader context manager API ([856d5c8](https://github.com/DaoChaShao/py-st-run-pro/commit/856d5c8754008e59799305689295fb1c640df468))
- **stats:** remove stats processor module ([de87fed](https://github.com/DaoChaShao/py-st-run-pro/commit/de87fedd1a0e44edbd271454950d35881caa06a7))
- **stats:** restructure module exports ([b19255b](https://github.com/DaoChaShao/py-st-run-pro/commit/b19255b151fcc86d2068b323986fcc45b88d8abc))
- **helper:** reorder class definitions in helper.py ([44fa05c](https://github.com/DaoChaShao/py-st-run-pro/commit/44fa05c8175ae19cecee5db502da6687d94e09d6))
- **decorator:** reorder clock and countdown definitions ([c1a8ecd](https://github.com/DaoChaShao/py-st-run-pro/commit/c1a8ecdcabaafe466b410ca7ad46b5e601352bb4))

