import os
import zipfile
from typing import Optional

def is_within_directory(directory: str, target: str) -> bool:
    abs_directory = os.path.abspath(directory)
    abs_target = os.path.abspath(target)
    return os.path.commonpath([abs_directory]) == os.path.commonpath([abs_directory, abs_target])

def safe_extract_zip(zip_path: str, dest_dir: str):
    with zipfile.ZipFile(zip_path, "r") as z:
        for member in z.namelist():
            # skip absolute paths
            normalized = os.path.normpath(member)
            if normalized.startswith("..") or os.path.isabs(normalized):
                # potential path traversal attempt; skip
                continue
            target = os.path.join(dest_dir, normalized)
            target_dir = os.path.dirname(target)
            os.makedirs(target_dir, exist_ok=True)
            with z.open(member) as source, open(target, "wb") as target_f:
                data = source.read()
                target_f.write(data)
