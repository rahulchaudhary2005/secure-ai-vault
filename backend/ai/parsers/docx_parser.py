from docx import Document

class DOCXParser:

    @staticmethod
    def extract_text(file_path: str):

        document = Document(file_path)

        full_text = []

        for para in document.paragraphs:
            full_text.append(para.text)

        return "\n".join(full_text)