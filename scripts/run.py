import pkgutil
import importlib
import os
from os.path import abspath

# List of packages you want to check
packages_to_check = [
    "Pillow",
    "screeninfo",
    "requests",
    "ttkbootstrap"
]

def check_packages(packages):
    """
    Checks if the given packages are installed.

    Args:
        packages (list): A list of package names to check.

    Returns:
        list: A list of missing packages.
    """
    missing_packages = []

    for package in packages:
        if not pkgutil.find_loader(package):
            missing_packages.append(package)

    return missing_packages

missing_packages = check_packages(packages_to_check)

if missing_packages:
    print("Missing packages:")
    for package in missing_packages:
        print(package)
    os.system("venv\\Scripts\\activate")
    os.system("pip install -r requirements.txt")
    os.system("python scripts\\icepos.py")
else:
    print("All required packages are installed.")
    os.system("python scripts\\icepos.py")
