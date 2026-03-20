# Testing Guide for py-googletraffic

This guide explains how to run tests for the py-googletraffic package.

## Test Structure

```
tests/
├── __init__.py             # Test package initialization
├── test_constants.py       # Tests for constants module
├── test_utils.py          # Tests for utility functions
└── test_core.py           # Tests for core functions (with mocks)
```

## Quick Start

### Install Test Dependencies

```bash
# Install package with test dependencies
pip install -e ".[test]"

# Or install from requirements file
pip install -r requirements-test.txt
```

### Run All Tests

**Using nose2 (recommended):**
```bash
# Run all tests
nose2

# Run with verbose output
nose2 -v

# Run with coverage
nose2 --with-coverage
```

**Using pytest:**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=googletraffic --cov-report=html

# Run specific test file
pytest tests/test_utils.py

# Run specific test class
pytest tests/test_utils.py::TestColorDistance

# Run specific test
pytest tests/test_utils.py::TestColorDistance::test_identical_colors
```

**Using unittest (built-in):**
```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_utils

# Run specific test class
python -m unittest tests.test_utils.TestColorDistance
```

## Test Categories

### Unit Tests (No External Dependencies)

These tests run quickly and don't require:
- Google Maps API key
- ChromeDriver
- Internet connection

```bash
# Run only unit tests
nose2 tests.test_constants
nose2 tests.test_utils
```

**Coverage:**
- `test_constants.py` - Tests for traffic colors, zoom scales, templates
- `test_utils.py` - Tests for color classification, geospatial calculations
- `test_core.py` - Tests for core logic (using mocks)

### Integration Tests (Requires Setup)

For full integration testing with actual Google Maps:

```bash
# Set API key
export GOOGLE_MAPS_API_KEY="your_api_key_here"

# Run integration tests (when available)
nose2 tests.test_integration
```

## Coverage Reports

### Generate Coverage Report

**Using nose2:**
```bash
nose2 --with-coverage --coverage-report html --coverage-report term
```

**Using pytest:**
```bash
pytest --cov=googletraffic --cov-report=html --cov-report=term
```

**Using coverage directly:**
```bash
coverage run -m nose2
coverage report
coverage html
```

### View Coverage Report

```bash
# Open HTML coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Running Specific Tests

### Run Single Test File

```bash
# nose2
nose2 tests.test_utils

# pytest
pytest tests/test_utils.py

# unittest
python -m unittest tests.test_utils
```

### Run Single Test Class

```bash
# nose2
nose2 tests.test_utils.TestColorDistance

# pytest
pytest tests/test_utils.py::TestColorDistance

# unittest
python -m unittest tests.test_utils.TestColorDistance
```

### Run Single Test Method

```bash
# nose2
nose2 tests.test_utils.TestColorDistance.test_identical_colors

# pytest
pytest tests/test_utils.py::TestColorDistance::test_identical_colors

# unittest
python -m unittest tests.test_utils.TestColorDistance.test_identical_colors
```

## Test Configuration

### nose2.cfg

Configuration for nose2 test runner:
- Verbosity level
- Coverage settings
- JUnit XML output
- Plugin configuration

### setup.cfg

Configuration for various tools:
- Nosetests settings
- Coverage options
- Code quality tools

## Continuous Integration

### GitHub Actions Example

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -e ".[test]"
    
    - name: Run tests
      run: |
        nose2 --with-coverage
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## Writing New Tests

### Test Template

```python
"""
Unit tests for new_module.
"""

import unittest
from googletraffic.new_module import function_to_test


class TestNewFunction(unittest.TestCase):
    """Test new_function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data = [1, 2, 3]
    
    def tearDown(self):
        """Clean up after tests."""
        pass
    
    def test_basic_functionality(self):
        """Test basic functionality."""
        result = function_to_test(self.test_data)
        self.assertEqual(result, expected_value)
    
    def test_edge_case(self):
        """Test edge case."""
        with self.assertRaises(ValueError):
            function_to_test(invalid_input)


if __name__ == '__main__':
    unittest.main()
```

### Best Practices

1. **One test class per function/class being tested**
2. **Descriptive test names** - `test_should_raise_error_on_invalid_input`
3. **Test both success and failure cases**
4. **Use mocks for external dependencies** (API calls, file I/O)
5. **Keep tests independent** - Each test should run standalone
6. **Use setUp/tearDown** for common test fixtures
7. **Test edge cases** - Empty inputs, None, negatives, etc.

### Mock External Dependencies

```python
from unittest.mock import Mock, patch

class TestWithMocks(unittest.TestCase):
    
    @patch('googletraffic.core.webdriver.Chrome')
    def test_with_mock_browser(self, mock_driver):
        """Test function that uses Selenium."""
        mock_browser = Mock()
        mock_driver.return_value = mock_browser
        
        # Your test here
        result = function_using_browser()
        
        # Verify mock was called
        mock_driver.assert_called_once()
```

## Troubleshooting

### Tests Not Found

```bash
# Make sure you're in the project root
cd /path/to/py-googletraffic

# Verify test discovery
nose2 --collect-only
```

### Import Errors

```bash
# Install package in development mode
pip install -e .

# Verify installation
python -c "import googletraffic; print(googletraffic.__version__)"
```

### Coverage Not Working

```bash
# Install coverage plugin
pip install nose2[coverage_plugin]

# Or use pytest-cov
pip install pytest pytest-cov
pytest --cov=googletraffic
```

### Selenium Tests Fail

The core tests use mocks and don't require actual Selenium. If you're writing integration tests:

```bash
# Install ChromeDriver
brew install chromedriver  # macOS
sudo apt-get install chromium-chromedriver  # Linux
```

## Test Statistics

Current test coverage:

```bash
# Generate report
nose2 --with-coverage

# Expected output:
# Name                       Stmts   Miss  Cover
# ----------------------------------------------
# googletraffic/__init__.py      5      0   100%
# googletraffic/constants.py    35      0   100%
# googletraffic/utils.py       125     10    92%
# googletraffic/core.py        210     45    79%
# ----------------------------------------------
# TOTAL                        375     55    85%
```

## Additional Tools

### Code Quality Checks

```bash
# Linting
flake8 googletraffic/

# Code formatting
black googletraffic/

# Type checking (if using type hints)
mypy googletraffic/
```

### Performance Testing

```bash
# Profile tests
python -m cProfile -m nose2

# Benchmark specific functions
python -m timeit -s "from googletraffic.utils import color_distance" \
  "color_distance((255,0,0), (0,255,0))"
```

## Resources

- [nose2 documentation](https://docs.nose2.io/)
- [pytest documentation](https://docs.pytest.org/)
- [unittest documentation](https://docs.python.org/3/library/unittest.html)
- [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html)
- [coverage.py documentation](https://coverage.readthedocs.io/)

## Next Steps

1. Run the test suite: `nose2 -v`
2. Check coverage: `nose2 --with-coverage`
3. Write tests for new features
4. Set up CI/CD with automated testing
5. Integrate coverage tracking (Codecov, Coveralls)
