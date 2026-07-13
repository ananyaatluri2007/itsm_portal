import uuid
from datetime import date, datetime
from sqlalchemy import String, Date, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_tag: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    asset_type: Mapped[str] = mapped_column(String, nullable=False)  # Laptop, Server, etc.
    manufacturer: Mapped[str] = mapped_column(String, nullable=True)
    model: Mapped[str] = mapped_column(String, nullable=True)
    serial_number: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    purchase_date: Mapped[date] = mapped_column(Date, nullable=True)
    warranty_expiry: Mapped[date] = mapped_column(Date, nullable=True)
    location: Mapped[str] = mapped_column(String, nullable=True)
    assigned_to: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
