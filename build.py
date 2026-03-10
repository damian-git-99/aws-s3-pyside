#!/usr/bin/env python3
"""
Build script for PyInstaller executable.
Run with: python build.py [--distpath PATH]
"""

import argparse
import os
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description='Build S3 Bucket Browser executable')
    parser.add_argument(
        '--distpath',
        default='dist',
        help='Output directory for the executable (default: dist)'
    )
    parser.add_argument(
        '--clean',
        action='store_true',
        help='Clean build directories before building'
    )
    args = parser.parse_args()

    spec_file = 's3-bucket-browser.spec'

    if not os.path.exists(spec_file):
        print(f"Error: Spec file '{spec_file}' not found.")
        sys.exit(1)

    cmd = ['pyinstaller', spec_file, '--distpath', args.distpath]

    if args.clean:
        cmd.append('--clean')

    print(f"Building executable with command: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print(f"\nBuild successful! Executable located in: {args.distpath}/")
    else:
        sys.exit(result.returncode)


if __name__ == '__main__':
    main()
