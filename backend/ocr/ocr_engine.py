from PIL import Image

import pytesseract

class OCREngine:

    @staticmethod
    def extract_text(image_path: str):

        image = Image.open(image_path)

        text = pytesseract.image_to_string(image)

        return text