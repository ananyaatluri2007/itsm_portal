import uuid
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.ticket import Ticket, TicketComment, TicketActivityLog, SLA_HOURS
from app.models.user import User
from app.schemas.ticket import (
    TicketCreate, TicketOut, StatusUpdate, AssignUpdate,
    CommentCreate, CommentOut, ActivityOut,
)
from app.dependencies.auth import get_current_user, require_role

router = APIRouter(prefix="/api/tickets", tags=["tickets"])

VALID_STATUSES = {"open", "in_progress", "pending_user", "resolved", "closed"}


async def _next_ticket_number(db: AsyncSession) -> str:
    year = datetime.now(timezone.utc).year
    result = await db.execute(select(func.count()).select_from(Ticket))
    count = result.scalar_one() + 1
    return f"INC-{year}{count:04d}"


async def _log_activity(db: AsyncSession, ticket_id, actor_id, action, old_value=None, new_value=None):
    db.add(TicketActivityLog(
        ticket_id=ticket_id, actor_id=actor_id, action=action,
        old_value=old_value, new_value=new_value,
    ))


@router.get("", response_model=list[TicketOut])
async def list_tickets(
    status: str | None = None,
    priority: str | None = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    query = select(Ticket)
    if status:
        query = query.where(Ticket.status == status)
    if priority:
        query = query.where(Ticket.priority == priority)
    result = await db.execute(query.order_by(Ticket.created_at.desc()))
    return result.scalars().all()


@router.get("/my", response_model=list[TicketOut])
async def my_tickets(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Ticket).where(Ticket.reporter_id == user.id).order_by(Ticket.created_at.desc())
    )
    return result.scalars().all()


@router.get("/queue", response_model=list[TicketOut])
async def my_queue(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Ticket).where(Ticket.assigned_to == user.id).order_by(Ticket.sla_due_at.asc())
    )
    return result.scalars().all()


@router.post("", response_model=TicketOut)
async def create_ticket(
    payload: TicketCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    hours = SLA_HOURS.get(payload.priority, 24)
    ticket = Ticket(
        ticket_number=await _next_ticket_number(db),
        title=payload.title,
        description=payload.description,
        category_id=payload.category_id,
        priority=payload.priority,
        asset_id=payload.asset_id,
        reporter_id=user.id,
        sla_due_at=datetime.now(timezone.utc) + timedelta(hours=hours),
    )
    db.add(ticket)
    await db.flush()
    await _log_activity(db, ticket.id, user.id, "created", new_value=ticket.status)
    await db.commit()
    await db.refresh(ticket)
    return ticket


@router.get("/{ticket_id}", response_model=TicketOut)
async def get_ticket(
    ticket_id: uuid.UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.patch("/{ticket_id}/status", response_model=TicketOut)
async def update_status(
    ticket_id: uuid.UUID,
    payload: StatusUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("admin", "agent")),
):
    if payload.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {VALID_STATUSES}")
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    old_status = ticket.status
    ticket.status = payload.status
    if payload.status == "resolved":
        ticket.resolved_at = datetime.now(timezone.utc)
    if payload.status == "closed":
        ticket.closed_at = datetime.now(timezone.utc)

    await _log_activity(db, ticket.id, user.id, "status_change", old_status, payload.status)
    await db.commit()
    await db.refresh(ticket)
    return ticket


@router.patch("/{ticket_id}/assign", response_model=TicketOut)
async def assign_ticket(
    ticket_id: uuid.UUID,
    payload: AssignUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("admin", "agent")),
):
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    old_assignee = str(ticket.assigned_to) if ticket.assigned_to else None
    ticket.assigned_to = payload.assigned_to
    await _log_activity(db, ticket.id, user.id, "assignment", old_assignee, str(payload.assigned_to))
    await db.commit()
    await db.refresh(ticket)
    return ticket


@router.get("/{ticket_id}/comments", response_model=list[CommentOut])
async def get_comments(
    ticket_id: uuid.UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    query = select(TicketComment).where(TicketComment.ticket_id == ticket_id)
    if user.role == "user":
        query = query.where(TicketComment.is_internal == False)  # noqa: E712
    result = await db.execute(query.order_by(TicketComment.created_at.asc()))
    return result.scalars().all()


@router.post("/{ticket_id}/comments", response_model=CommentOut)
async def add_comment(
    ticket_id: uuid.UUID,
    payload: CommentCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    comment = TicketComment(
        ticket_id=ticket_id, author_id=user.id, body=payload.body,
        is_internal=payload.is_internal if user.role != "user" else False,
    )
    db.add(comment)
    await _log_activity(db, ticket_id, user.id, "comment")
    await db.commit()
    await db.refresh(comment)
    return comment


@router.get("/{ticket_id}/activity", response_model=list[ActivityOut])
async def get_activity(
    ticket_id: uuid.UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(TicketActivityLog)
        .where(TicketActivityLog.ticket_id == ticket_id)
        .order_by(TicketActivityLog.created_at.asc())
    )
    return result.scalars().all()
