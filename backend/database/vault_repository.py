from backend.database.database import (
    SessionLocal
)

from backend.database.models import (
    VaultDocument
)


class VaultRepository:

    @staticmethod
    def save_document(

        owner_email: str,

        encrypted_path: str,

        original_filename: str,

        vector_collection: str

    ):

        db = SessionLocal()

        try:

            document = VaultDocument(

                owner_email=owner_email,

                encrypted_path=encrypted_path,

                original_filename=original_filename,

                vector_collection=vector_collection
            )

            db.add(document)

            db.commit()

            db.refresh(document)

            return document

        finally:

            db.close()

    @staticmethod
    def get_user_documents(
        owner_email: str
    ):

        db = SessionLocal()

        try:

            documents = (
                db.query(VaultDocument)
                .filter(
                    VaultDocument.owner_email
                    == owner_email
                )
                .all()
            )

            return documents

        finally:

            db.close()