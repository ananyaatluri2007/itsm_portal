import uuid
from datetime import date
from pydantic import BaseModel


class AssetCreate(BaseModel):
    asset_tag: str
    name: str
    asset_type: str
    manufacturer: str | None = None
    model: str | None = None
    serial_number: str | None = None
    purchase_date: date | None = None
    warranty_expiry: date | None = None
    location: str | None = None
    assigned_to: uuid.UUID | None = None


class AssetOut(AssetCreate):
    id: uuid.UUID
    status: str

    class Config:
        from_attributes = True
