# PyPI Publishing Guide 📦

Complete guide for publishing **py-googletraffic** to PyPI (Python Package Index).

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup PyPI Account](#setup-pypi-account)
- [Configure GitHub Secrets](#configure-github-secrets)
- [Pre-Release Checklist](#pre-release-checklist)
- [Publishing Methods](#publishing-methods)
- [Post-Release Tasks](#post-release-tasks)
- [Troubleshooting](#troubleshooting)

## Prerequisites

✅ All prerequisites are already met:
- Package structure with `setup.py` and `pyproject.toml`
- Documentation (README, CHANGELOG, CONTRIBUTING)
- Tests with good coverage
- LICENSE file (MIT)
- Version number defined in `__init__.py`
- GitHub Actions workflows configured

## Setup PyPI Account

### 1. Create PyPI Accounts

You need accounts on both:
- **PyPI** (production): https://pypi.org/account/register/
- **Test PyPI** (testing): https://test.pypi.org/account/register/

### 2. Enable Two-Factor Authentication (2FA)

For PyPI (required):
1. Go to https://pypi.org/manage/account/
2. Click "Add 2FA with authentication application"
3. Follow the setup instructions

### 3. Generate API Tokens

**For PyPI (Production):**
1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Name: `py-googletraffic-github-actions`
4. Scope: "Entire account" (or specific project after first upload)
5. Copy the token (starts with `pypi-...`)

**For Test PyPI (Testing):**
1. Go to https://test.pypi.org/manage/account/token/
2. Repeat the same process
3. Copy the token

⚠️ **Save these tokens securely!** You won't be able to see them again.

## Configure GitHub Secrets

Add the API tokens as GitHub repository secrets:

### Steps:
1. Go to your repository: https://github.com/kwahalf/py-googletraffic
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

### Add These Secrets:

| Name | Value | Description |
|------|-------|-------------|
| `PYPI_API_TOKEN` | `pypi-...` | Your PyPI production token |
| `TEST_PYPI_API_TOKEN` | `pypi-...` | Your Test PyPI token |

## Pre-Release Checklist

Before publishing, verify all these items:

### Code Quality
- [ ] All tests pass: `make test`
- [ ] Linting passes: `make lint`
- [ ] Code formatted: `make format`
- [ ] No critical TODOs in code

### Documentation  
- [ ] README.md is complete and accurate
- [ ] CHANGELOG.md updated with release notes
- [ ] All documentation links work (no "kwahalf" placeholders)
- [ ] Version number updated in all files
- [ ] Examples work correctly

### Version Management
- [ ] Version bumped in `googletraffic/__init__.py`
- [ ] Version bumped in `setup.py`
- [ ] Version bumped in `pyproject.toml`
- [ ] All three versions match!

### Legal & Attribution
- [ ] LICENSE file present (MIT)
- [ ] Copyright year is current
- [ ] CONTRIBUTORS.md updated
- [ ] No sensitive information in code/docs

### Package Structure
- [ ] All required files included in `MANIFEST.in`
- [ ] No unnecessary files in package
- [ ] Dependencies specified correctly
- [ ] Python version requirements correct

### Run Local Tests

```bash
# Clean build artifacts
rm -rf build/ dist/ *.egg-info

# Build package
python -m build

# Check package
twine check dist/*

# Test installation
pip install dist/*.whl
python -c "import googletraffic; print(googletraffic.__version__)"
```

## Publishing Methods

There are three ways to publish to PyPI:

### Method 1: Automatic on Version Change (Recommended)

This is already configured! Just:

1. **Update version** in all three files:
   - `googletraffic/__init__.py`
   - `setup.py`  
   - `pyproject.toml`

2. **Update CHANGELOG.md** with release notes

3. **Commit and push to main:**
   ```bash
   git add .
   git commit -m "Release v0.1.0"
   git push origin main
   ```

4. **GitHub Actions will automatically:**
   - Detect version change
   - Build package
   - Publish to PyPI
   - Create git tag
   - Create GitHub Release

**Workflow:** `.github/workflows/publish-on-version-change.yml`

### Method 2: Manual Release (Tag-Based)

Create a release manually:

1. **Update version and CHANGELOG**

2. **Commit changes:**
   ```bash
   git add .
   git commit -m "Release v0.1.0"
   git push
   ```

3. **Create and push tag:**
   ```bash
   git tag -a v0.1.0 -m "Version 0.1.0"
   git push origin v0.1.0
   ```

4. **Create GitHub Release:**
   - Go to: https://github.com/kwahalf/py-googletraffic/releases/new
   - Select tag: `v0.1.0`
   - Fill in release notes
   - Click "Publish release"

5. **GitHub Actions will automatically publish to PyPI**

**Workflow:** `.github/workflows/publish-pypi.yml`

### Method 3: Manual Local Upload

For testing or emergency fixes:

```bash
# 1. Build package
python -m build

# 2. Upload to Test PyPI first
twine upload --repository testpypi dist/*

# 3. Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ py-googletraffic

# 4. If all works, upload to real PyPI
twine upload dist/*
```

## Post-Release Tasks

After successful PyPI publication:

### 1. Verify Installation

```bash
# In a fresh environment
pip install py-googletraffic

# Test import
python -c "import googletraffic; print(googletraffic.__version__)"
```

### 2. Update Documentation

- [ ] Update README badges if needed
- [ ] Check PyPI page looks correct: https://pypi.org/project/py-googletraffic/
- [ ] Announce release (if applicable)

### 3. Monitor

- Check for installation issues: https://github.com/kwahalf/py-googletraffic/issues
- Monitor PyPI download stats: https://pypistats.org/packages/py-googletraffic

## Troubleshooting

### Error: "Invalid or non-existent authentication information"

**Cause:** API token not set or incorrect

**Solution:**
1. Verify token in GitHub Secrets
2. Make sure secret name matches workflow: `PYPI_API_TOKEN`
3. Token should start with `pypi-`

### Error: "File already exists"

**Cause:** Version already published to PyPI

**Solution:**
1. You cannot re-upload the same version
2. Bump version number
3. PyPI versions are immutable (security feature)

### Error: "Invalid distribution file"

**Cause:** Package build failed or corrupt

**Solution:**
```bash
# Clean and rebuild
rm -rf build/ dist/ *.egg-info
python -m build
twine check dist/*
```

### Error: "Version mismatch"

**Cause:** Version in `__init__.py` doesn't match `setup.py`

**Solution:**
Update version in all three files:
- `googletraffic/__init__.py` - `__version__ = "0.1.0"`
- `setup.py` - `version="0.1.0"`
- `pyproject.toml` - `version = "0.1.0"`

### Workflow isn't triggering

**Cause:** Various reasons

**Solution:**
1. Check workflow file syntax
2. Verify GitHub Actions enabled: Settings → Actions → General
3. Check if you have PYPI_API_TOKEN secret set
4. Review workflow run logs in Actions tab

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
  - **MAJOR**: Incompatible API changes
  - **MINOR**: New features (backward compatible)
  - **PATCH**: Bug fixes (backward compatible)

**Examples:**
- `0.1.0` → `0.1.1` - Bug fix
- `0.1.1` → `0.2.0` - New feature
- `0.2.0` → `1.0.0` - First stable release
- `1.0.0` → `2.0.0` - Breaking changes

**Pre-release versions:**
- `0.1.0-alpha.1` - Alpha release
- `0.1.0-beta.1` - Beta release
- `0.1.0-rc.1` - Release candidate

## Testing on Test PyPI

Before releasing to production PyPI, test on Test PyPI:

### 1. Trigger Test Workflow

```bash
# Method 1: Manual workflow trigger
# Go to: Actions → Publish to PyPI → Run workflow

# Method 2: Use workflow_dispatch
gh workflow run publish-pypi.yml
```

### 2. Install from Test PyPI

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple py-googletraffic
```

Note: `--extra-index-url` is needed for dependencies

### 3. Test Package

```python
import googletraffic as gt
print(gt.__version__)

# Test basic functionality
# (Requires Google API key)
```

## Security Best Practices

1. **Never commit API tokens** to git
2. **Use GitHub Secrets** for sensitive data
3. **Enable 2FA** on PyPI account
4. **Use project-scoped tokens** when possible
5. **Rotate tokens periodically**
6. **Review published package** immediately after release
7. **Monitor for unauthorized changes**

## Resources

- **PyPI**: https://pypi.org/project/py-googletraffic/
- **Test PyPI**: https://test.pypi.org/project/py-googletraffic/
- **PyPI Stats**: https://pypistats.org/packages/py-googletraffic
- **Python Packaging Guide**: https://packaging.python.org/
- **Semantic Versioning**: https://semver.org/
- **GitHub Actions**: https://docs.github.com/en/actions

## Getting Help

If you encounter issues:

1. Check [Troubleshooting](#troubleshooting) section above
2. Review GitHub Actions logs in the Actions tab
3. Check PyPI documentation: https://pypi.org/help/
4. Ask in [GitHub Discussions](https://github.com/kwahalf/py-googletraffic/discussions)

---

**Ready to publish?** Follow the [Pre-Release Checklist](#pre-release-checklist) and choose a [Publishing Method](#publishing-methods)!
