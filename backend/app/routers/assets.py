import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.asset import Asset
from app.models.user import User
from app.schemas.asset import AssetCreate, AssetOut
from app.dependencies.auth import get_current_user, require_role

router = APIRouter(prefix="/api/assets", tags=["assets"])


@router.get("", response_model=list[AssetOut])
async def list_assets(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(select(Asset))
    return result.scalars().all()


@router.post("", response_model=AssetOut)
async def create_asset(
    payload: AssetCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("admin", "agent")),
):
    asset = Asset(**payload.model_dump())
    db.add(asset)
    await db.commit()
    await db.refresh(asset)
    return asset


@router.get("/{asset_id}", response_model=AssetOut)
async def get_asset(
    asset_id: uuid.UUID, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    result = await db.execute(select(Asset).where(Asset.id == asset_id))
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.delete("/{asset_id}")
async def retire_asset(
    asset_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("admin")),
):
    result = await db.execute(select(Asset).where(Asset.id == asset_id))
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    asset.status = "retired"
    await db.commit()
    return {"message": "Asset retired"}
