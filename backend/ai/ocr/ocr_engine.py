import tempfile
import os

import pytesseract

from PIL import Image


class OCREngine:

    @staticmethod
    def extract_text(
        file_bytes: bytes
    ):

        try:

            with tempfile.NamedTemporaryFile(

                delete=False,

                suffix=".png"
            ) as temp_file:

                temp_file.write(
                    file_bytes
                )

                temp_path = (
                    temp_file.name
                )

            image = Image.open(
                temp_path
            )

            text = (
                pytesseract
                .image_to_string(image)
            )

            os.remove(temp_path)

            return text

        except Exception as e:

            print(

                f"OCR ERROR: {e}"
            )

            return ""