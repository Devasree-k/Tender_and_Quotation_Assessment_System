
import asyncio
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

            A new quotation has been submitted in the Tender and Quotation Assessment System.

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
        total_score: int,
        decision: str,
        remarks: str | None,
    ) -> bool:

        return await asyncio.to_thread(
            self.send_evaluation_notification,
            vendor_email,
            quotation_id,
            total_score,
            decision,
            remarks,
        )


    # Notification 3: Tender awarded -> Winning vendor

    def send_sanction_notification(
        self,
        vendor_email: str,
        quotation_id: int,
        tender_id: int,
        sanctioned_amount: str,
    ) -> bool:

        subject = "Congratulations! Tender Awarded - Tender System"

        body = f"""
            Hello Vendor,

            Congratulations!

            Your quotation has been selected and the tender
            has been awarded to your company.

            Award Details
            -------------
            Quotation ID: {quotation_id}
            Tender ID: {tender_id}
            Sanctioned Amount: ₹{sanctioned_amount}

            Please log in to the system to view the complete
            sanction details and further instructions.

            Regards,
            Tender and Quotation Assessment System
        """

        return self.send_email(subject, body, recipient=vendor_email)

    async def send_sanction_notification_async(
        self,
        vendor_email: str,
        quotation_id: int,
        tender_id: int,
        sanctioned_amount: str,
    ) -> bool:

        return await asyncio.to_thread(
            self.send_sanction_notification,
            vendor_email,
            quotation_id,
            tender_id,
            sanctioned_amount,
        )
