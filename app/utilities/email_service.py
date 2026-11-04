
import asyncio
from datetime import date
from decimal import Decimal
import logging
import smtplib
from email.message import EmailMessage
from email.utils import formatdate

from app.core.config import (
    ADMIN_EMAIL,
    EMAIL_PASSWORD,
    EMAIL_SENDER,
)

logger = logging.getLogger(__name__)


class EmailService:

    def send_email(
        self,
        subject: str,
        body: str,
        recipient: str | None = None,
    ) -> bool:

        receiver = recipient or ADMIN_EMAIL

        if not EMAIL_SENDER or not EMAIL_PASSWORD or not receiver:
            logger.error("Email configuration is missing")
            return False

        try:
            message = EmailMessage()

            message["Subject"] = subject
            message["From"] = EMAIL_SENDER
            message["To"] = receiver
            message["Date"] = formatdate(localtime=True)

            message.set_content(body)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as smtp:

                smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
                smtp.send_message(message)

            logger.info("Notification email sent successfully")
            return True

        except (smtplib.SMTPException, OSError):
            logger.exception("Failed to send notification email")
            return False

    # Notification 1: New quotation submitted -> Admin

    def send_quotation_notification(
        self,
        quotation_id: int,
        tender_id: int,
        vendor_id: int,
        amount_quoted: str,
    ) -> bool:

        subject = "New Quotation Submitted - Tender System"

        body = f"""

            Hello Admin,

            A new quotation has been submitted in the
            Tender and Quotation Assessment System.

            Quotation Details
            -----------------
            Quotation ID: {quotation_id}
            Tender ID: {tender_id}
            Vendor ID: {vendor_id}
            Quoted Amount: ₹{amount_quoted}

            Please log in to the system to review the quotation.

            Regards,
            Tender and Quotation Assessment System
        """

        return self.send_email(subject, body)

    async def send_quotation_notification_async(
        self,
        quotation_id: int,
        tender_id: int,
        vendor_id: int,
        amount_quoted: str,
    ) -> bool:

        return await asyncio.to_thread(
            self.send_quotation_notification,
            quotation_id,
            tender_id,
            vendor_id,
            amount_quoted,
        )

    # Notification 2: Evaluation completed -> Vendor
    def send_evaluation_notification(
        self,
        vendor_email: str,
        quotation_id: int,
        tender_id: int,
        total_score: int,
        decision: str,
        remarks: str | None,
    ) -> bool:

        subject = "Quotation Evaluation Completed - Tender System"

        body = f"""
            Hello Vendor,

            Your submitted quotation has been evaluated.

            Evaluation Details
            -----------------
            Quotation ID: {quotation_id}
            Tender ID: {tender_id}
            Total Score: {total_score}/100
            Decision: {decision}
            Remarks: {remarks or "No remarks provided"}

            Please log in to the system to view further details.

            Regards,
            Tender and Quotation Assessment System
        """

        return self.send_email(subject, body, recipient=vendor_email,)

    async def send_evaluation_notification_async(
        self,
        vendor_email: str,
        quotation_id: int,
        tender_id: int,
        total_score: int,
        decision: str,
        remarks: str | None,
    ) -> bool:

        return await asyncio.to_thread(
            self.send_evaluation_notification,
            vendor_email,
            quotation_id,
            tender_id,
            total_score,
            decision,
            remarks,
        )


    # Notification 3: Tender awarded -> Winning vendor

    def send_award_notification(
        self,
        vendor_email: str,
        vendor_name: str,
        tender_title: str,
        tender_id: int,
        sanctioned_amount: Decimal,
        sanction_date: date,
    ) -> bool:

        if not EMAIL_SENDER or not EMAIL_PASSWORD:
            logger.error("Email configuration is missing.")
            return False

        subject = f"Congratulations! Tender #{tender_id} Awarded"

        body = f"""
        Hello {vendor_name},

        Congratulations!

        Your quotation has been selected and sanctioned.

        Tender Details
        -------------------------
        Tender ID: {tender_id}
        Tender Title: {tender_title}
        Sanctioned Amount: {sanctioned_amount}
        Sanction Date: {sanction_date.isoformat()}

        Please log in to the Public Tender and Quotation
        Assessment System to view your sanction details.

        Regards,
        Public Tender and Quotation Assessment System
        """

        try:
            message = EmailMessage()

            message["Subject"] = subject
            message["From"] = EMAIL_SENDER
            message["To"] = vendor_email
            message["Date"] = formatdate(localtime=True)

            message.set_content(body)

            with smtplib.SMTP_SSL(
                "smtp.gmail.com",
                465,
                timeout=15,
            ) as smtp:

                smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
                smtp.send_message(message)

            logger.info(
                "Award notification email sent. tender_id=%s recipient=%s",
                tender_id,
                vendor_email,
            )

            return True

        except (smtplib.SMTPException, OSError):
            logger.exception(
                "Failed to send award notification. tender_id=%s",
                tender_id,
            )

            return False


    async def send_award_notification_async(
        self,
        vendor_email: str,
        vendor_name: str,
        tender_title: str,
        tender_id: int,
        sanctioned_amount: Decimal,
        sanction_date: date,
    ) -> bool:

        return await asyncio.to_thread(
            self.send_award_notification,
            vendor_email,
            vendor_name,
            tender_title,
            tender_id,
            sanctioned_amount,
            sanction_date,
        )
