"""
This file installs the packages listed in requirements.txt
using the project's sys.executable.
"""

if __name__ == "__main__":
    import sys
    import subprocess

    with open("requirements.txt", "r") as inp:
        packages = [line.strip() for line in inp]

    subprocess.call([sys.executable, "-m", "pip", "install", *packages])
