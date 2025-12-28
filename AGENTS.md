# AGENTS.md file

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
- Write commit messages using [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
- Never bump the internal package version in `setup.py`. This is handled automatically by the release process.
- Python files use CRLF as the line ending.
- The implementation should be done in Python 2.7+ and compatible with Python 3.13.
- No type annotations should exist in the `.py` files and if the exist they should isolated in th `.pyi` files.
- The style should respect the black formatting.
- The implementation should be done in a way that is compatible with the existing codebase.
- Prefer `item not in list` over `not item in list`.
- Prefer `item == None` over `item is None`.
- The commenting style of the project is unique, try to keep commenting style consistent.

## Pre-Commit Checklist

Before committing, ensure that the following operations items check:

- [ ] Code is formatted with `black .`
- [ ] Tests pass: `RUN_MODE=development DB_ENGINE=sqlite HTTPBIN=httpbin.bemisc.com PLUGIN_PATH="./*/src;./*/*src" python setup.py test`
- [ ] CHANGELOG.md is updated in [Unreleased] section
- [ ] No debugging print statements or commented-out code
- [ ] CRLF line endings are preserved
- [ ] No type annotations in .py files (use .pyi if needed)

## License

Colony Plugins is licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).
