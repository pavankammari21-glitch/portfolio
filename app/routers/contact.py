from typing import List
from fastapi import APIRouter, Depends, BackgroundTasks, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.contact import ContactMessage
from app.models.user import User
from app.schemas.contact import ContactCreate, ContactOut, ContactResponse
from app.schemas.common import StandardResponse
from app.services.email_service import send_contact_notification
from app.dependencies import get_client_ip, rate_limiter, get_current_admin
from app.exceptions import ResourceNotFoundException

router = APIRouter(prefix="/contact", tags=["Contact Inquiries & BackgroundTasks"])

@router.post(
    "",
    response_model=ContactResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit Contact Inquiry (Triggers Async BackgroundTasks)",
    description=(
        "Demonstrates FastAPI `BackgroundTasks` and Dependency Injection Rate Limiting. "
        "The message is persisted immediately in SQLite, and an asynchronous notification task "
        "is dispatched in the background without blocking the HTTP response."
    ),
    dependencies=[Depends(rate_limiter(max_requests=10, window_seconds=60))]
)
async def submit_contact_form(
    payload: ContactCreate,
    background_tasks: BackgroundTasks,
    client_ip: str = Depends(get_client_ip),
    db: Session = Depends(get_db)
):
    # 1. Persist to database
    contact_record = ContactMessage(
        name=payload.name,
        email=payload.email,
        subject=payload.subject,
        message=payload.message,
        client_ip=client_ip,
        is_read=False
    )
    db.add(contact_record)
    db.commit()
    db.refresh(contact_record)

    # 2. Enqueue asynchronous background task
    background_tasks.add_task(
        send_contact_notification,
        name=payload.name,
        email=payload.email,
        subject=payload.subject,
        message=payload.message,
        client_ip=client_ip
    )

    return ContactResponse(
        success=True,
        message=f"Thank you {payload.name}! Your message has been safely received. A background notification has been dispatched.",
        inquiry_id=contact_record.id,
        estimated_response_time="Within 24 hours"
    )

@router.get(
    "/inbox",
    response_model=StandardResponse[List[ContactOut]],
    summary="View Contact Submissions (Admin Only)",
    description="Protected admin endpoint to inspect all contact inquiries."
)
async def list_contact_messages(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    messages = db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).all()
    return StandardResponse(
        success=True,
        message=f"Total {len(messages)} inquiries found",
        data=[ContactOut.model_validate(m) for m in messages]
    )

@router.patch(
    "/inbox/{message_id}/read",
    response_model=StandardResponse[ContactOut],
    summary="Mark Message as Read (Admin Only)",
    description="Updates message status."
)
async def mark_message_as_read(
    message_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    msg = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not msg:
        raise ResourceNotFoundException("Contact Message", message_id)
        
    msg.is_read = True
    db.commit()
    db.refresh(msg)
    
    return StandardResponse(
        success=True,
        message="Message marked as read",
        data=ContactOut.model_validate(msg)
    )
