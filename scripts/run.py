import pkgutil
import importlib
import os

# List of packages you want to check
packages_to_check = [
    "Pillow",
    "screeninfo",
    "requests",
    "ttkbootstrap"
]

def check_packages(packages):
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
    os.system("pip install -r other\\requirements.txt")
    os.system("python scripts\\icepos.py")
else:
    print("All required packages are installed.")
    os.system("python scripts\\icepos.py")
