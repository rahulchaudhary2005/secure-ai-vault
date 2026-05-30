from sqlalchemy.exc import IntegrityError

from backend.database.database import SessionLocal
from backend.database.models import User


class UserRepository:

    @staticmethod
    def create_user(
        email: str,
        hashed_password: str
    ):

        db = SessionLocal()

        try:
            user = User(
                email=email,
                hashed_password=hashed_password
            )

            db.add(user)
            db.commit()
            db.refresh(user)

            return user

        except IntegrityError:
            db.rollback()
            return None

        finally:
            db.close()

    @staticmethod
    def get_by_email(
        email: str
    ):

        db = SessionLocal()

        try:
            return (
                db.query(User)
                .filter(User.email == email)
                .first()
            )

        finally:
            db.close()

    @staticmethod
    def get_total_users():

        db = SessionLocal()

        try:
            return db.query(User).count()

        finally:
            db.close()
