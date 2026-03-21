# Contributing to py-googletraffic

Thank you for your interest in contributing to py-googletraffic! This document provides guidelines for contributing to the project.

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/py-googletraffic.git
cd py-googletraffic
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install in Development Mode

```bash
# Install package with all dependencies
pip install -e ".[dev,test,jupyter]"
```

### 4. Verify Setup

```bash
# Run tests
make test

# Check code style
make lint
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

- Write clear, documented code
- Follow PEP 8 style guidelines
- Add docstrings to functions and classes
- Update documentation as needed

### 3. Write Tests

```bash
# Add tests in tests/ directory
# Run tests locally
make test

# Run specific test
nose2 tests.test_your_module
```

### 4. Format and Lint

```bash
# Format code
make format

# Check linting
make lint
```

### 5. Commit Changes

```bash
git add .
git commit -m "Brief description of changes"
```

**Commit Message Guidelines:**
- Use present tense ("Add feature" not "Added feature")
- First line should be 50 characters or less
- Add detailed description after blank line if needed

### 6. Push and Create PR

```bash
git push origin your-branch-name
```

Then create a Pull Request on GitHub.

## Code Style

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://github.com/psf/black) for code formatting
- Maximum line length: 100 characters
- Use type hints where appropriate

### Docstring Format

Use Google-style docstrings:

```python
def function_name(param1, param2):
    """
    Brief description of function.
    
    Longer description if needed.
    
    Parameters
    ----------
    param1 : type
        Description of param1
    param2 : type
        Description of param2
    
    Returns
    -------
    type
        Description of return value
    
    Examples
    --------
    >>> result = function_name(1, 2)
    >>> print(result)
    3
    """
```

## Testing Guidelines

### Writing Tests

1. **Location:** Add tests in `tests/` directory
2. **Naming:** Test files should start with `test_`
3. **Structure:** One test class per function/class being tested
4. **Coverage:** Aim for >80% code coverage

### Test Example

```python
import unittest
from googletraffic.module import function_to_test


class TestFunctionName(unittest.TestCase):
    """Test function_to_test."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data = [1, 2, 3]
    
    def test_expected_behavior(self):
        """Test normal operation."""
        result = function_to_test(self.test_data)
        self.assertEqual(result, expected_value)
    
    def test_edge_case(self):
        """Test edge case."""
        with self.assertRaises(ValueError):
            function_to_test(invalid_input)
```

### Running Tests

```bash
# All tests
make test

# With coverage
make test-cov

# Specific test
nose2 tests.test_module.TestClass.test_method
```

## Documentation

### Update Documentation

If your changes affect usage:

1. Update relevant `.md` files (README.md, INSTALLATION.md, etc.)
2. Update docstrings
3. Add examples if introducing new features
4. Update [examples/getting_started.ipynb](examples/getting_started.ipynb) if relevant

### Documentation Files

- `README.md` - Main documentation
- `INSTALLATION.md` - Installation instructions
- `QUICKSTART.md` - Quick start guide
- `WINDOWS.md` - Windows-specific guide
- `tests/README.md` - Testing documentation

## Pull Request Process

### Before Submitting

- [ ] Tests pass locally (`make test`)
- [ ] Code is formatted (`make format`)
- [ ] Linting passes (`make lint`)
- [ ] Documentation is updated
- [ ] Commit messages are clear

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Testing
Describe testing performed

## Checklist
- [ ] Tests pass
- [ ] Code formatted
- [ ] Documentation updated
- [ ] Breaking changes documented
```

### Review Process

1. Automated tests run on GitHub Actions
2. Maintainers review code
3. Address review comments
4. Once approved, PR will be merged

## Issue Guidelines

### Reporting Bugs

**Use the bug report template:**

```markdown
**Description:**
Clear description of the bug

**To Reproduce:**
Steps to reproduce:
1. ...
2. ...

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- OS: [e.g., Windows 10, macOS 12, Ubuntu 20.04]
- Python version: [e.g., 3.9.7]
- Package version: [e.g., 0.1.0]

**Additional Context:**
Any other relevant information
```

### Feature Requests

```markdown
**Feature Description:**
Clear description of proposed feature

**Use Case:**
Why is this feature needed?

**Proposed Implementation:**
Ideas for how to implement (optional)

**Alternatives Considered:**
Other approaches considered
```

## Code Review Guidelines

### For Reviewers

- Be constructive and respectful
- Focus on code, not the person
- Explain reasoning for suggestions
- Approve when satisfied, don't block on minor issues

### For Contributors

- Respond to feedback promptly
- Ask questions if feedback is unclear
- Don't take criticism personally
- Update PR based on feedback

## Release Process

(For maintainers)

1. Update version in `setup.py` and `__init__.py`
2. Update `NEWS.md` or `CHANGELOG.md`
3. Create release tag: `git tag -a v0.1.0 -m "Release 0.1.0"`
4. Push tag: `git push origin v0.1.0`
5. GitHub Actions will build and publish to PyPI

## Getting Help

- 📖 Read the [documentation](README.md)
- 💬 Ask questions in [GitHub Discussions](https://github.com/kwahalf/py-googletraffic/discussions)
- 🐛 Report bugs in [GitHub Issues](https://github.com/kwahalf/py-googletraffic/issues)
- 💡 Suggest features in [GitHub Issues](https://github.com/kwahalf/py-googletraffic/issues)

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone.

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community

### Unacceptable Behavior

- Harassment, trolling, or discriminatory comments
- Publishing others' private information
- Other conduct inappropriate in a professional setting


## Recognition

All contributors are automatically recognized! Your contributions will appear in:

- **[CONTRIBUTORS.md](CONTRIBUTORS.md)** - Auto-generated from git commits
- **[README.md](README.md)** - Contributors section with avatars
- **[GitHub Contributors Page](https://github.com/yourusername/py-googletraffic/graphs/contributors)** - Visual contribution graph
- **Release notes** - Mentioned for significant contributions

### How It Works

Every time code is merged into the main branch:
1. A GitHub Action automatically runs
2. It analyzes git commit history
3. Updates CONTRIBUTORS.md with current statistics
4. All commit authors are credited

**Note:** Make sure your git email matches your GitHub email to be properly credited with your GitHub profile.

### Update Contributors Manually

You can also generate the contributors list locally:

```bash
# Generate/update CONTRIBUTORS.md
python scripts/generate_contributors.py

# Or use the Makefile target
make contributors
```

Thank you for contributing to py-googletraffic! 🎉
