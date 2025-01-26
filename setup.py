from setuptools import setup, find_packages
import os
import sys
import platform
from typing import List, Dict

def check_system_requirements() -> Dict[str, bool]:
    return {
        "platform": platform.system() == "Darwin",
        "processor": "M4" in platform.processor(),
        "python_version": sys.version_info >= (3, 9)
    }

def initialize_analysis(install_deps: bool = True) -> int:
    try:
        # Install dependencies if requested
        if install_deps:
            os.system(f"{sys.executable} -m pip install -r requirements.txt")

        # Initialize project structure
        directories = [
            'data',
            'models',
            'logs',
            'certificates',
            'analysis',
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

        # Create initial certificate store
        with open('certificates/chain.dat', 'wb') as f:
            f.write(b'\x00' * 64)  # Initialize empty certificate chain

        return 0

    except Exception as e:
        print(f"Initialization failed: {str(e)}")
        return 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python setup.py [command]")
        print("\nCommands:")
        print("  initialize_analysis    Initialize analysis environment")
        sys.exit(1)

    command = sys.argv[1]
    if command == "initialize_analysis":
        sys.exit(initialize_analysis())
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

# Standard setup configuration
setup(
    name="codemutant-x",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.24.3',
        'scipy>=1.11.1',
        'torch>=2.0.1',
        'networkx>=3.1',
        'cryptography>=41.0.1',
        'pqcrypto>=0.7.2',
        'sympy>=1.12',
    ],
    entry_points={
        'console_scripts': [
            'codemutant=run:main',
        ],
    },
    python_requires='>=3.9',
    author="Steve Seguin",
    description="The future of code is not written - it's mutated",
    license="MIT",
)
