import uuid
from datetime import datetime
from pydantic import BaseModel


class TicketCreate(BaseModel):
    title: str
    description: str
    category_id: int | None = None
    priority: str = "P3"
    asset_id: uuid.UUID | None = None


class TicketOut(BaseModel):
    id: uuid.UUID
    ticket_number: str
    title: str
    description: str
    category_id: int | None
    priority: str
    status: str
    reporter_id: uuid.UUID
    assigned_to: uuid.UUID | None
    asset_id: uuid.UUID | None
    sla_due_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True


class StatusUpdate(BaseModel):
    status: str  # open, in_progress, pending_user, resolved, closed


class AssignUpdate(BaseModel):
    assigned_to: uuid.UUID


class CommentCreate(BaseModel):
    body: str
    is_internal: bool = False


class CommentOut(BaseModel):
    id: uuid.UUID
    author_id: uuid.UUID
    body: str
    is_internal: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ActivityOut(BaseModel):
    id: uuid.UUID
    actor_id: uuid.UUID | None
    action: str
    old_value: str | None
    new_value: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
