
import logging
import uuid
from pathlib import Path

import aiofiles
from fastapi import UploadFile

from app.core.config import BASE_DIR


logger = logging.getLogger(__name__)

UPLOAD_DIR = BASE_DIR / "uploads" / "quotations"

MAX_FILE_SIZE = 10 * 1024 * 1024

ALLOWED_EXTENSION = ".pdf"
ALLOWED_CONTENT_TYPE = "application/pdf"


async def save_quotation_file(
    upload_file: UploadFile,
) -> tuple[str, str]:

    original_filename = Path(
        upload_file.filename or ""
    ).name

    extension = Path(original_filename).suffix.lower()

    if not original_filename or extension != ALLOWED_EXTENSION:
        raise ValueError("Only PDF documents are allowed.")

    if upload_file.content_type != ALLOWED_CONTENT_TYPE:
        raise ValueError("Invalid file content type.")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    unique_filename = f"{uuid.uuid4().hex}.pdf"

    file_path = UPLOAD_DIR / unique_filename

    total_size = 0
    first_chunk = True

    try:
        async with aiofiles.open(file_path, "wb") as file:

            while True:
                chunk = await upload_file.read(1024 * 1024)

                if not chunk:
                    break

                if first_chunk:
                    if not chunk.startswith(b"%PDF-"):
                        raise ValueError("Uploaded file is not a valid PDF.")
                    first_chunk = False

                total_size += len(chunk)

                if total_size > MAX_FILE_SIZE:
                    raise ValueError("File size must not exceed 10 MB.")

                await file.write(chunk)

        if total_size == 0:
            raise ValueError("Uploaded file is empty.")

        relative_path = str(
            Path("uploads") / "quotations" / unique_filename
        )

        logger.info(
            "Quotation document saved. filename=%s",
            unique_filename,
        )

        return relative_path, original_filename

    except Exception:
        if file_path.exists():
            file_path.unlink()

        raise

    finally:
        await upload_file.close()


def delete_quotation_file(document_path: str) -> None:

    file_path = (BASE_DIR / document_path).resolve()
    upload_root = UPLOAD_DIR.resolve()

    if upload_root not in file_path.parents:
        raise ValueError("Invalid quotation document path.")

    if file_path.exists():
        file_path.unlink()

        logger.info(
            "Quotation document deleted. filename=%s",
            file_path.name,
        )
