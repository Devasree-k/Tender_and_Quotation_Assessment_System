
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from app.database.base import Base

from app.models import (
    User,
    Vendor,
    Tender,
    Quotation,
    Evaluation,
    Sanction,
    RefreshToken,
)


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def create_test_tables():
    async with test_engine.begin() as connection:
        await connection.run_sync(
            Base.metadata.create_all
        )


async def drop_test_tables():
    async with test_engine.begin() as connection:
        await connection.run_sync(
            Base.metadata.drop_all
        )

