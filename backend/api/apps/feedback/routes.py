from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth.models import User
from core.dependencies import get_current_user, get_db
from .models import FeedbackResponse
from .schemas import FeedbackCreate, FeedbackResponseSchema

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post(
    "",
    response_model=FeedbackResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_feedback(
    payload: FeedbackCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> FeedbackResponse:
    feedback = FeedbackResponse(
        user_id=current_user.id,
        enjoyment=payload.enjoyment,
        comments=payload.comments.strip(),
        suggestions=payload.suggestions.strip() if payload.suggestions else None,
    )
    db.add(feedback)
    await db.commit()
    await db.refresh(feedback)
    return feedback
