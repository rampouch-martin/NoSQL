import subprocess

print("Import cars...")
subprocess.run(["python", "import_cars.py"])

print("Import car_prices...")
subprocess.run(["python", "import_prices.py"])

print("Import sales...")
subprocess.run(["python", "import_sales.py"])

print("Import Wolt...")
subprocess.run(["python", "import_wolt.py"])

print("Import images... (this may take a while)")
subprocess.run(["python", "import_images.py"])

print("All data imported successfully.")
