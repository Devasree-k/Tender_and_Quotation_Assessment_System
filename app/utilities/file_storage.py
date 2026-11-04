
from pathlib import Path
from uuid import uuid4

import aiofiles
from fastapi import UploadFile

from app.core.config import BASE_DIR
from app.core.exceptions.exception import QuotationBusinessRuleException


UPLOAD_DIR = BASE_DIR / "uploads" / "quotations"

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

ALLOWED_EXTENSION = ".pdf"
ALLOWED_CONTENT_TYPE = "application/pdf"


async def save_quotation_file(file: UploadFile) -> tuple[str, str]:

    if not file.filename:
        raise QuotationBusinessRuleException(
            "File name is required"
        )

    extension = Path(file.filename).suffix.lower()

    if extension != ALLOWED_EXTENSION:
        raise QuotationBusinessRuleException(
            "Only PDF files are allowed"
        )

    if file.content_type != ALLOWED_CONTENT_TYPE:
        raise QuotationBusinessRuleException(
            "Invalid file content type"
        )

    content = await file.read()

    if not content:
        raise QuotationBusinessRuleException(
            "Uploaded file is empty"
        )

    if len(content) > MAX_FILE_SIZE:
        raise QuotationBusinessRuleException(
            "File size must not exceed 10 MB"
        )

    if not content.startswith(b"%PDF-"):
        raise QuotationBusinessRuleException(
            "Uploaded file is not a valid PDF"
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    unique_filename = f"{uuid4().hex}.pdf"

    file_path = UPLOAD_DIR / unique_filename

    async with aiofiles.open(file_path, "wb") as saved_file:
        await saved_file.write(content)

    relative_path = str(file_path.relative_to(BASE_DIR)).replace("\\", "/")

    return relative_path, file.filename
