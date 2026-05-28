from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".txt",
    ".docx",
    ".pptx",
    ".mp4",
    ".mp3",
    ".wav"
}

MAX_FILE_SIZE = 1024 * 1024 * 500

AES_KEY_SIZE = 32

CHUNK_SIZE = 1024

OCR_LANG = "eng"

LOG_FORMAT = (
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)