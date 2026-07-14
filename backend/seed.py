"""
Creates demo users and default incident categories.
Safe to re-run — skips anything that already exists.

Run after create_tables.py:
    python seed.py

Logins:
  Admin:  admin@itsm.com / Admin@123
  Agent:  agent@itsm.com / Agent@123
  User:   user@itsm.com  / User@123
"""
import asyncio
from sqlalchemy import select
from app.core.db import AsyncSessionLocal
from app.core.security import hash_password
from app.models.user import User
from app.models.category import Category

DEMO_USERS = [
    ("admin@itsm.com", "Admin User", "Admin@123", "admin"),
    ("agent@itsm.com", "Agent User", "Agent@123", "agent"),
    ("user@itsm.com", "End User", "User@123", "user"),
]

DEFAULT_CATEGORIES = [
    "Hardware Failure", "Software Issue", "Network Problem",
    "Access & Permissions", "Security Alert", "Service Request", "Other",
]


async def main():
    async with AsyncSessionLocal() as db:
        for email, name, password, role in DEMO_USERS:
            result = await db.execute(select(User).where(User.email == email))
            if result.scalar_one_or_none():
                print(f"Skipped (already exists): {email}")
                continue
            db.add(User(email=email, name=name, password_hash=hash_password(password), role=role))
            print(f"Created: {email} / {password}")

        for name in DEFAULT_CATEGORIES:
            result = await db.execute(select(Category).where(Category.name == name))
            if result.scalar_one_or_none():
                continue
            db.add(Category(name=name))

        await db.commit()
        print("Seeding complete.")


if __name__ == "__main__":
    asyncio.run(main())