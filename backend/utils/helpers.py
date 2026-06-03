import hashlib
import os
from pathlib import Path

from .constants import ALLOWED_EXTENSIONS

def validate_file_extension(filename: str):
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    return extension

def generate_secure_filename(filename: str):
    random_hash = hashlib.sha256(
        os.urandom(32)
    ).hexdigest()

    extension = Path(filename).suffix

    return f"{random_hash}{extension}"

def validate_safe_path(path: str):
    normalized = os.path.normpath(path)

    if ".." in normalized:
        raise ValueError("Unsafe file path detected")

    return normalized