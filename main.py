# Main file to run the application. To run the application, execute the following command: python main.py

# import required libraries
import importlib.util
import subprocess
import sys

# import custom modules
from connections import neo4j_driver
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

# verify if the Neo4j connection is working or start connection 
def ensure_neo4j():
    try:
        neo4j_driver.verify_connectivity()
    except Exception as e:
        print(f'*** ERROR *** Cannot connect to Neo4j: {e}. Connect to Neo4j in your terminal, with the command: neo4j console')
        sys.exit(1)

# ------------------------ Main -------------------
if __name__ == '__main__':
    ensure_packages()
    ensure_neo4j()
    main()
