from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_db

router = APIRouter(
    prefix="/health",
    tags=["Health Check"]
)


@router.get("/")
async def health_check(db: AsyncSession = Depends(get_db)) -> dict[str, str]:

    try:
        # Check database connectivity
        await db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected"
        }

    except SQLAlchemyError as exc:
        # Do not expose internal database details
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "database": "disconnected"
            }
        ) from exc
    
