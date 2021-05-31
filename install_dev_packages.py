"""
This file installs the packages listed in requirements-dev.txt
using the project's sys.executable.
"""

if __name__ == "__main__":
    import sys
    import subprocess

    with open("requirements-dev.txt", "r") as inp:
        packages = [line.strip() for line in inp]

    subprocess.call([sys.executable, "-m", "pip", "install", *packages])
