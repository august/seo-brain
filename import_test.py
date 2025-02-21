# import_test.py (Forcefully isolate venv paths - TRY THIS!)
import sys
import os

venv_site_packages = os.path.join(os.getcwd(), "venv", "lib", "python3.12", "site-packages") # Adjust python version if needed
sys.path = [venv_site_packages, os.getcwd()] #  <---  REPLACE sys.path - ONLY venv and project dir!

print(f"sys.path (modified): {sys.path}") # Print sys.path to verify

from google.generativeai.types.content_types import Blob, Content, Part

print("Import successful (if you see this, import worked after forceful path isolation)!")