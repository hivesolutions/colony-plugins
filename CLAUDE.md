# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**Additional generic instructions for AI Agents can be found in the [AGENTS.md](AGENTS.md) file.**

## Testing Conventions

### File Structure
- Tests are placed in `test.py` within each module (e.g., `client/src/client_utils/test.py`)
- Mock classes go in a separate `mocks.py` file in the same directory
- Register tests in `__init__.py` with `from . import test`

### Import Style
Use module-level imports with prefix access:
```python
from . import system
from . import exceptions
from . import mocks

# Usage
service = system.ServiceHTTP(mocks.MockPlugin())
```

### Test Class Structure
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

### Plugin Registration
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

### Test Isolation
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

### Code Style
- Run `black` for formatting before committing
- Avoid inline comments unless explaining complex logic
- Windows line endings (CRLF) are expected
