import subprocess
import sys
import os

PACKAGE_NAME = "hash_method"

def build_package():
    """Build the Python package using setuptools."""
    # Remove previous builds
    dist_path = os.path.join(os.path.dirname(__file__), 'dist')
    if os.path.exists(dist_path):
        print(f"Removing previous builds in {dist_path}...")
        for file in os.listdir(dist_path):
            os.remove(os.path.join(dist_path, file))
        os.rmdir(dist_path)
    # Build the package
    print("Building the package...")
    result = subprocess.run([sys.executable, 'setup.py', 'sdist', 'bdist_wheel'])
    if result.returncode == 0:
        print("Build successful.")
    else:
        print("Build failed.")
        sys.exit(result.returncode)

if __name__ == "__main__":
    build_package()
