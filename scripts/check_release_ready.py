#!/usr/bin/env python3
"""
Pre-release checklist for py-googletraffic.

Checks if the package is ready for PyPI publication.
"""

import os
import sys
import subprocess
import re
from pathlib import Path


class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"


def print_header(text):
    """Print section header."""
    print(f"\n{Colors.BLUE}{'=' * 70}{Colors.RESET}")
    print(f"{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BLUE}{'=' * 70}{Colors.RESET}\n")


def print_check(passed, message):
    """Print check result."""
    if passed:
        print(f"{Colors.GREEN}✓{Colors.RESET} {message}")
        return True
    else:
        print(f"{Colors.RED}✗{Colors.RESET} {message}")
        return False


def run_command(cmd, check=False):
    """Run shell command and return output."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=check,
        )
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        return False, str(e)


def check_file_exists(filepath, description):
    """Check if a file exists."""
    exists = Path(filepath).exists()
    return print_check(exists, f"{description}: {filepath}")


def get_version_from_file(filepath, pattern):
    """Extract version from a file using regex pattern."""
    try:
        with open(filepath, "r") as f:
            content = f.read()
            match = re.search(pattern, content)
            if match:
                return match.group(1)
    except Exception:
        pass
    return None


def main():
    """Run all checks."""
    print_header("🚀 PRE-RELEASE CHECKLIST FOR PY-GOOGLETRAFFIC")

    all_passed = True
    warnings = []

    # =========================================================================
    # 1. REQUIRED FILES
    # =========================================================================
    print_header("1. Required Files")

    required_files = [
        ("setup.py", "Setup script"),
        ("pyproject.toml", "Modern packaging config"),
        ("README.md", "Main documentation"),
        ("LICENSE", "License file"),
        ("CHANGELOG.md", "Version history"),
        ("MANIFEST.in", "Package manifest"),
        ("googletraffic/__init__.py", "Package init"),
    ]

    for filepath, desc in required_files:
        if not check_file_exists(filepath, desc):
            all_passed = False

    # =========================================================================
    # 2. VERSION CONSISTENCY
    # =========================================================================
    print_header("2. Version Consistency")

    version_init = get_version_from_file(
        "googletraffic/__init__.py", r'__version__\s*=\s*["\']([^"\']+)["\']'
    )
    version_setup = get_version_from_file("setup.py", r'version\s*=\s*["\']([^"\']+)["\']')
    version_pyproject = get_version_from_file(
        "pyproject.toml", r'version\s*=\s*["\']([^"\']+)["\']'
    )

    print(f"Version in __init__.py: {version_init}")
    print(f"Version in setup.py: {version_setup}")
    print(f"Version in pyproject.toml: {version_pyproject}")

    versions_match = (
        version_init == version_setup == version_pyproject and version_init is not None
    )

    if print_check(versions_match, "All versions match"):
        print(f"  → Version: {Colors.GREEN}{version_init}{Colors.RESET}")
    else:
        all_passed = False

    # =========================================================================
    # 3. GIT STATUS
    # =========================================================================
    print_header("3. Git Status")

    # Check for uncommitted changes
    success, output = run_command("git status --porcelain")
    uncommitted = len(output) > 0
    if uncommitted:
        print_check(False, "No uncommitted changes")
        print(f"  {Colors.YELLOW}Found uncommitted changes:{Colors.RESET}")
        print(f"  {output[:200]}")
        warnings.append("Uncommitted changes detected")
    else:
        print_check(True, "No uncommitted changes")

    # Check current branch
    success, branch = run_command("git rev-parse --abbrev-ref HEAD")
    is_main = branch in ["main", "master"]
    print_check(is_main, f"On main branch (currently on: {branch})")
    if not is_main:
        warnings.append(f"Not on main branch (on {branch})")

    # =========================================================================
    # 4. DOCUMENTATION
    # =========================================================================
    print_header("4. Documentation")

    # Check for placeholder URLs
    success, readme_content = run_command("cat README.md")
    has_placeholders = "kwahalf" in readme_content.lower()
    print_check(
        not has_placeholders, "No placeholder URLs in README (no 'kwahalf')"
    )
    if has_placeholders:
        warnings.append("Found 'kwahalf' placeholders in README")

    # Check CHANGELOG has latest version
    success, changelog = run_command("cat CHANGELOG.md")
    if version_init and version_init in changelog:
        print_check(True, f"CHANGELOG.md mentions version {version_init}")
    else:
        print_check(False, f"CHANGELOG.md should mention version {version_init}")
        warnings.append(f"Update CHANGELOG.md for version {version_init}")

    # =========================================================================
    # 5. CODE QUALITY
    # =========================================================================
    print_header("5. Code Quality")

    # Run tests
    success, _ = run_command("python3 -m nose2 --quiet 2>&1")
    if print_check(success, "Tests pass"):
        pass
    else:
        print(f"  {Colors.YELLOW}Run: make test{Colors.RESET}")
        all_passed = False

    # Check linting
    success, _ = run_command(
        "flake8 googletraffic/ --max-line-length=100 --ignore=E203,W503,E501,F841"
    )
    if print_check(success, "Linting passes"):
        pass
    else:
        print(f"  {Colors.YELLOW}Run: make lint{Colors.RESET}")
        warnings.append("Fix linting errors")

    # Check formatting
    success, _ = run_command("black --check googletraffic/ tests/ --line-length=100 --quiet")
    if print_check(success, "Code formatted with black"):
        pass
    else:
        print(f"  {Colors.YELLOW}Run: make format{Colors.RESET}")
        warnings.append("Format code with black")

    # =========================================================================
    # 6. PACKAGE BUILD
    # =========================================================================
    print_header("6. Package Build Test")

    # Clean previous builds
    run_command("rm -rf build/ dist/ *.egg-info")

    # Try building
    success, build_output = run_command("python3 -m build 2>&1")
    if print_check(success, "Package builds successfully"):
        # Check with twine
        success, _ = run_command("twine check dist/* 2>&1")
        if print_check(success, "Package passes twine check"):
            pass
        else:
            print(f"  {Colors.YELLOW}Run: python -m build && twine check dist/*{Colors.RESET}")
            all_passed = False
    else:
        print(f"  {Colors.RED}Build failed:{Colors.RESET}")
        print(f"  {build_output[:500]}")
        all_passed = False

    # =========================================================================
    # 7. GITHUB ACTIONS
    # =========================================================================
    print_header("7. GitHub Actions Configuration")

    workflows = [
        (".github/workflows/tests.yml", "CI/CD testing workflow"),
        (".github/workflows/publish-pypi.yml", "PyPI publish (on release)"),
        (
            ".github/workflows/publish-on-version-change.yml",
            "PyPI publish (on version change)",
        ),
    ]

    for filepath, desc in workflows:
        check_file_exists(filepath, desc)

    # =========================================================================
    # 8. GITHUB SECRETS
    # =========================================================================
    print_header("8. GitHub Secrets (Manual Check Required)")

    print(f"{Colors.YELLOW}⚠{Colors.RESET}  Manually verify these secrets exist:")
    print("  1. Go to: https://github.com/kwahalf/py-googletraffic/settings/secrets/actions")
    print(f"  2. Check for: {Colors.BLUE}PYPI_API_TOKEN{Colors.RESET}")
    print(f"  3. Check for: {Colors.BLUE}TEST_PYPI_API_TOKEN{Colors.RESET} (optional)")
    print()
    print("  See PUBLISHING.md for setup instructions")

    # =========================================================================
    # SUMMARY
    # =========================================================================
    print_header("📋 SUMMARY")

    if all_passed and len(warnings) == 0:
        print(f"{Colors.GREEN}✓ ALL CHECKS PASSED!{Colors.RESET}")
        print(f"\n{Colors.GREEN}Your package is ready for publication!{Colors.RESET}\n")
        print("Next steps:")
        print("  1. Ensure GitHub secrets are configured (see section 8)")
        print("  2. Review PUBLISHING.md for publishing methods")
        print("  3. Choose a publishing method and proceed")
        print()
        print("Quick publish:")
        print(f"  {Colors.BLUE}git push origin main{Colors.RESET}")
        print("  (If version changed, GitHub Actions will auto-publish)")
        return 0
    else:
        if not all_passed:
            print(f"{Colors.RED}✗ CRITICAL ISSUES FOUND{Colors.RESET}")
            print("\nFix the errors marked with ✗ above before publishing.\n")

        if warnings:
            print(f"{Colors.YELLOW}⚠ WARNINGS:{Colors.RESET}")
            for warning in warnings:
                print(f"  • {warning}")
            print()

        print("Review the checklist above and fix all issues.")
        print(f"\nSee {Colors.BLUE}PUBLISHING.md{Colors.RESET} for detailed guidance.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
