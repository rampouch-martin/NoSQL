import subprocess
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

print("Import cars...")
subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, "import_cars.py")])

print("Import car_prices...")
subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, "import_prices.py")])

print("Import sales...")
subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, "import_sales.py")])

print("Import Wolt...")
subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, "import_wolt.py")])

print("Import images... (this may take a while)")
subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, "import_images.py")])

print("All data imported successfully.")

