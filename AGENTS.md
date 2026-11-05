# AGENTS.md file

## Python Virtual Environment (venv)

The Python virtual environment for this repository is typically located in `.venv`.

## Formatting

Always format the code before commiting using, making sure that the Python code is properly formatted using:

```bash
pip install black
black .
```

## Testing

To run the custom suite of unit test for Colony Plugins use the following sequence of commands that will install dependencies
and run the appropriate test suite (last command).

Try to run the unit tests whenever making changes to the codebase, before commiting new code.

```bash
pip install -r requirements.txt
RUN_MODE=development DB_ENGINE=sqlite HTTPBIN=httpbin.bemisc.com PLUGIN_PATH=./*/src;./*/*src python setup.py test
```

The SQLite engine synchronizes every write of its databases to the disk by default (`DB_SYNCHRONOUS=2`, the `synchronous` pragma of SQLite). The tests destroy their databases after each test, so on a slow or busy disk set `DB_SYNCHRONOUS=0` to run them without the synchronization.

### Writing Tests

#### File Structure

- Tests are placed in `test.py` within each module (e.g., `client/src/client_utils/test.py`)
- Mock classes go in a separate `mocks.py` file in the same directory
- Register tests in `__init__.py` with `from . import test`

#### Import Style

Use module-level imports with prefix access:

```python
from . import system
from . import exceptions
from . import mocks

# Usage
service = system.ServiceHTTP(mocks.MockPlugin())
```

#### Test Class Structure

```python
class ModuleNameTest(colony.Test):
    """
    The module name infra-structure test class, responsible
    for the returning of the associated tests.
    """

    def get_bundle(self):
        return (
            SomeTestCase,
            AnotherTestCase,
        )

    def set_up(self, test_case):
        colony.Test.set_up(self, test_case)

    def tear_down(self, test_case):
        colony.Test.tear_down(self, test_case)


class SomeTestCase(colony.ColonyTestCase):
    @staticmethod
    def get_description():
        return "Some test case"

    def test_something(self):
        self.assertEqual(actual, expected)
```

#### Plugin Registration

Add test capability to the plugin file:

```python
capabilities = [
    "existing_capability",
    "test",
]

def load_plugin(self):
    # ... existing code ...
    self.test = module.ModuleNameTest(self)
```

#### Test Isolation

When overriding `setUp`, always call parent first:

```python
def setUp(self):
    colony.ColonyTestCase.setUp(self)
    # your setup code
```

For class-level state, save in `setUp` and restore in `tearDown`:

```python
def setUp(self):
    colony.ColonyTestCase.setUp(self)
    self._saved_map = SomeClass.class_level_map.copy()
    SomeClass.class_level_map = {}

def tearDown(self):
    SomeClass.class_level_map = self._saved_map
```

## Style Guide

- Always update `CHANGELOG.md` according to semantic versioning, mentioning your changes in the unreleased section.
- Document every new configuration value in the [Configuration](README.md#configuration) section of `README.md`, in the table of its area (name, type, default and description).
- Write commit messages using [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
- Never bump the internal package version in `setup.py`. This is handled automatically by the release process.
- Python files use CRLF as the line ending.
- The implementation should be done in Python 2.7+ and compatible with Python 3.13.
- No type annotations should exist in the `.py` files and if they exist they should be isolated in the `.pyi` files.
- The style should respect the black formatting.
- The implementation should be done in a way that is compatible with the existing codebase.
- Prefer `not item in list` over `item not in list`.
- Prefer `item == None` over `item is None`.
- The commenting style of the project is unique, try to keep commenting style consistent.

## Commit Messages

This project follows [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) with the following structure:

```text
<type>: <description>

<body>
```

### Commit Types

| Type       | Description                                             |
| ---------- | ------------------------------------------------------- |
| `feat`     | A new feature or functionality                          |
| `fix`      | A bug fix                                               |
| `docs`     | Documentation only changes                              |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `chore`    | Maintenance tasks, dependency updates, build changes    |
| `test`     | Adding or updating tests                                |
| `version`  | Version bump commits (reserved for releases)            |

### Guidelines

- Use lowercase for the type prefix.
- Use imperative mood in the description (e.g., "Add feature" not "Added feature").
- Keep the first line under 50 characters.
- Reference issue/PR numbers when applicable using `(#123)` at the end.
- For version releases, use the format `version: X.Y.Z`.
- Add an extra newline between subject and body.
- Make the body a series of bullet points about the commit.
- Be descriptive always making use of the body of the message.

### Examples

```text
feat: Add user authentication with OAuth 2.0 support (#138)
fix: Resolve race condition in database connection pool
docs: Add API endpoint documentation for v2 routes
refactor: Extract validation logic into reusable utility module
chore: Update dependencies to latest stable versions
test: Add integration tests for payment processing flow
version: 1.8.0
```

## Pre-Commit Checklist

Before committing, ensure that the following operations items check:

- [ ] Code is formatted with `black .`
- [ ] Tests pass: `RUN_MODE=development DB_ENGINE=sqlite HTTPBIN=httpbin.bemisc.com PLUGIN_PATH="./*/src;./*/*src" python setup.py test`
- [ ] CHANGELOG.md is updated in [Unreleased] section
- [ ] New configuration values are documented in the Configuration section of README.md
- [ ] No debugging print statements or commented-out code
- [ ] CRLF line endings are preserved
- [ ] No type annotations in .py files (use .pyi if needed)

## New Release

There is no manual release process, every push to `master` is released by the Deploy Workflow (`.github/workflows/deploy.yml`):

- The unit tests are run and must pass.
- Every plugin is uploaded to the Colony repository with `cpm upload`.

## License

Colony Plugins is licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).
