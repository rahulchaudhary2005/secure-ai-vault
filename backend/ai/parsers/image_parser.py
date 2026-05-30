from backend.ai.ocr.ocr_engine import OCREngine

class ImageParser:

    @staticmethod
    def extract_text(file_path: str):

        return OCREngine.extract_text(file_path)