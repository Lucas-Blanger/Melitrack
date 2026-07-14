import smtplib
from email.message import EmailMessage

from config import get_settings
from core.logger import get_logger

logger = get_logger(__name__)

settings = get_settings()


class EmailService:

    @staticmethod
    async def send_reset_code(email: str, code: str) -> None:
        message = EmailMessage()

        message["Subject"] = "Password Recovery - Melitrack"
        message["From"] = settings.SMTP_FROM
        message["To"] = email

        message.set_content(f"""
Hello!

Your password recovery code is:

{code}

This code expires in 10 minutes.

If you didn't request a password reset, you can ignore this email.

Melitrack Team
""")

        try:
            with smtplib.SMTP(
                settings.SMTP_HOST,
                settings.SMTP_PORT,
            ) as smtp:

                smtp.starttls()

                smtp.login(
                    settings.SMTP_USERNAME,
                    settings.SMTP_PASSWORD,
                )

                smtp.send_message(message)

            logger.info("Recovery email sent to %s", email)

        except Exception:
            logger.exception(
                "Failed to send recovery email to %s",
                email,
            )
            raise
