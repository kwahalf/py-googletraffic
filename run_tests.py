#!/usr/bin/env python
"""
Test runner script for py-googletraffic.

This script provides a convenient way to run tests with different configurations.
"""

import sys
import os
import subprocess
import argparse


def run_tests(runner='nose2', verbose=False, coverage=False, pattern=None):
    """
    Run tests with specified configuration.
    
    Parameters
    ----------
    runner : str
        Test runner to use ('nose2', 'pytest', or 'unittest')
    verbose : bool
        Enable verbose output
    coverage : bool
        Generate coverage report
    pattern : str
        Test file pattern to run (e.g., 'test_utils')
    """
    cmd = []
    
    if runner == 'nose2':
        cmd = ['nose2']
        if verbose:
            cmd.append('-v')
        if coverage:
            cmd.extend(['--with-coverage', '--coverage-report', 'term', 
                       '--coverage-report', 'html'])
        if pattern:
            cmd.append(f'tests.{pattern}')
    
    elif runner == 'pytest':
        cmd = ['pytest']
        if verbose:
            cmd.append('-v')
        if coverage:
            cmd.extend(['--cov=googletraffic', '--cov-report=html', '--cov-report=term'])
        if pattern:
            cmd.append(f'tests/{pattern}.py')
        else:
            cmd.append('tests/')
    
    elif runner == 'unittest':
        cmd = ['python', '-m', 'unittest']
        if verbose:
            cmd.append('-v')
        if pattern:
            cmd.append(f'tests.{pattern}')
        else:
            cmd.extend(['discover', 'tests'])
    
    else:
        print(f"Unknown test runner: {runner}")
        return 1
    
    print(f"Running: {' '.join(cmd)}")
    print("-" * 60)
    
    result = subprocess.run(cmd)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description='Run py-googletraffic tests',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all tests with nose2
  python run_tests.py
  
  # Run with pytest and coverage
  python run_tests.py --runner pytest --coverage
  
  # Run specific test file
  python run_tests.py --pattern test_utils
  
  # Run with verbose output
  python run_tests.py -v
        """
    )
    
    parser.add_argument(
        '--runner',
        choices=['nose2', 'pytest', 'unittest'],
        default='nose2',
        help='Test runner to use (default: nose2)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Generate coverage report'
    )
    
    parser.add_argument(
        '--pattern',
        help='Test file pattern (e.g., test_utils)'
    )
    
    parser.add_argument(
        '--install-deps',
        action='store_true',
        help='Install test dependencies before running'
    )
    
    args = parser.parse_args()
    
    # Install dependencies if requested
    if args.install_deps:
        print("Installing test dependencies...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-e', '.[test]'])
        print()
    
    # Run tests
    return run_tests(
        runner=args.runner,
        verbose=args.verbose,
        coverage=args.coverage,
        pattern=args.pattern
    )


if __name__ == '__main__':
    sys.exit(main())
