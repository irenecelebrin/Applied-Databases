# main file to run the application. To run the application, execute the following command: python main.py

import importlib.util
import subprocess
import sys

# import menu 
from menu import main

# verify if the required packages are installed, and if not, install them 
# Based on: https://stackoverflow.com/questions/1051254/check-if-python-package-is-installed
def ensure_packages():
    with open("requirements.txt") as f:
        packages = [line.strip() for line in f if line.strip()]
    for package in packages:
        if importlib.util.find_spec(package) is None:
            print(f"Installing missing package: {package}")
            # install the packages and print status messages. Source: https://docs.python.org/3/library/subprocess.html#subprocess.check_call
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

ensure_packages()



# -------------------------------------------
if __name__ == '__main__':
    main()
