import os
import zipfile
import shutil
from typing import List
from utils.file_safe import safe_extract_zip

def ensure_dirs(*paths):
    for p in paths:
        os.makedirs(p, exist_ok=True)

def create_zip_from_folder(folder_path: str, output_zip: str):
    shutil.make_archive(base_name=output_zip.replace(".zip", ""), format="zip", root_dir=folder_path)
    # shutil adds .zip; ensure path endswith .zip
    if not output_zip.endswith(".zip"):
        output_zip = output_zip + ".zip"
    return output_zip
