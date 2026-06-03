from fastapi_mail import FastMail
from fastapi_mail import MessageSchema

from auth.email_config import conf


class EmailSender:

    @staticmethod
    async def send_otp_email(
        email: str,
        otp: str
    ):

        message = MessageSchema(

            subject="AI Vault Verification OTP",

            recipients=[email],

            body=f"""

            Your AI Vault OTP is:

            {otp}

            Do not share this code.

            """,

            subtype="plain"
        )

        fm = FastMail(conf)

        await fm.send_message(message)