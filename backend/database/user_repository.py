from sqlalchemy.exc import IntegrityError

from database.database import SessionLocal
from database.models import User


class UserRepository:

    # =========================================
    # CREATE USER
    # =========================================

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

    # =========================================
    # GET USER BY EMAIL
    # =========================================

    @staticmethod
    def get_by_email(
        email: str
    ):

        db = SessionLocal()

        try:

            return (

                db.query(User)

                .filter(
                    User.email == email
                )

                .first()
            )

        finally:

            db.close()

    # =========================================
    # TOTAL USERS
    # =========================================

    @staticmethod
    def get_total_users():

        db = SessionLocal()

        try:

            return (

                db.query(User)

                .count()
            )

        finally:

            db.close()

    # =========================================
    # GET SETTINGS
    # =========================================

    @staticmethod
    def get_settings(
        email: str
    ):

        db = SessionLocal()

        try:

            return (

                db.query(User)

                .filter(
                    User.email == email
                )

                .first()
            )

        finally:

            db.close()

    # =========================================
    # GET AI SETTINGS
    # =========================================

    @staticmethod
    def get_ai_settings(
        email: str
    ):

        db = SessionLocal()

        try:

            user = (

                db.query(User)

                .filter(
                    User.email == email
                )

                .first()
            )

            if not user:

                return {

                    "ai_model": "gemma:2b",

                    "ai_temperature": 0.3,

                    "context_window": 2048,

                    "max_response_length": 1000,

                    "streaming_enabled": True,

                    "reasoning_enabled": False
                }

            return {

                "ai_model":
                    getattr(
                        user,
                        "ai_model",
                        "gemma:2b"
                    ),

                "ai_temperature":
                    float(
                        getattr(
                            user,
                            "ai_temperature",
                            0.3
                        )
                    ),

                "context_window":
                    getattr(
                        user,
                        "context_window",
                        2048
                    ),

                "max_response_length":
                    getattr(
                        user,
                        "max_response_length",
                        1000
                    ),

                "streaming_enabled":
                    getattr(
                        user,
                        "streaming_enabled",
                        True
                    ),

                "reasoning_enabled":
                    getattr(
                        user,
                        "reasoning_enabled",
                        False
                    )
            }

        finally:

            db.close()

    # =========================================
    # UPDATE SETTINGS
    # =========================================

    @staticmethod
    def update_settings(

        email: str,

        settings: dict
    ):

        db = SessionLocal()

        try:

            user = (

                db.query(User)

                .filter(
                    User.email == email
                )

                .first()
            )

            if not user:

                return None

            # =====================================
            # PROFILE SETTINGS
            # =====================================

            user.full_name = (

                settings.get(
                    "full_name",
                    getattr(
                        user,
                        "full_name",
                        ""
                    )
                )
            )

            user.role = (

                settings.get(
                    "role",
                    getattr(
                        user,
                        "role",
                        ""
                    )
                )
            )

            # =====================================
            # AI MODEL SETTINGS
            # =====================================

            user.ai_model = (

                settings.get(
                    "ai_model",
                    getattr(
                        user,
                        "ai_model",
                        "gemma:2b"
                    )
                )
            )

            user.ai_temperature = (

                settings.get(
                    "ai_temperature",
                    getattr(
                        user,
                        "ai_temperature",
                        "0.3"
                    )
                )
            )

            user.response_style = (

                settings.get(
                    "response_style",
                    getattr(
                        user,
                        "response_style",
                        "professional"
                    )
                )
            )

            # =====================================
            # AUTO LOCK
            # =====================================

            if hasattr(
                user,
                "auto_lock_minutes"
            ):

                user.auto_lock_minutes = (

                    settings.get(
                        "auto_lock_minutes",
                        getattr(
                            user,
                            "auto_lock_minutes",
                            15
                        )
                    )
                )

            # =====================================
            # ADVANCED AI SETTINGS
            # =====================================

            if hasattr(
                user,
                "context_window"
            ):

                user.context_window = (

                    settings.get(
                        "context_window",
                        getattr(
                            user,
                            "context_window",
                            2048
                        )
                    )
                )

            if hasattr(
                user,
                "max_response_length"
            ):

                user.max_response_length = (

                    settings.get(
                        "max_response_length",
                        getattr(
                            user,
                            "max_response_length",
                            1000
                        )
                    )
                )

            if hasattr(
                user,
                "streaming_enabled"
            ):

                user.streaming_enabled = (

                    settings.get(
                        "streaming_enabled",
                        getattr(
                            user,
                            "streaming_enabled",
                            True
                        )
                    )
                )

            if hasattr(
                user,
                "reasoning_enabled"
            ):

                user.reasoning_enabled = (

                    settings.get(
                        "reasoning_enabled",
                        getattr(
                            user,
                            "reasoning_enabled",
                            False
                        )
                    )
                )

            # =====================================
            # SAVE
            # =====================================

            db.commit()

            db.refresh(user)

            return user

        except Exception as e:

            db.rollback()

            print(
                "\n========== SETTINGS UPDATE ERROR =========="
            )

            print(str(e))

            print(
                "==========================================\n"
            )

            return None

        finally:

            db.close()