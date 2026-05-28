
from pypdf import PdfReader

class PDFParser:

    @staticmethod
    def extract_text(file_path: str):

        reader = PdfReader(file_path)

        extracted_text = ""

        for page in reader.pages:
            extracted_text += page.extract_text() + "\n"

        return extracted_text