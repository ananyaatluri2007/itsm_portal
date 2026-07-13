"""
Creates one demo admin user so you can log in immediately.
Run after create_tables.py:

    python seed.py

Login with: admin@itsm.com / Admin@123
"""
import asyncio
from app.core.db import AsyncSessionLocal
from app.core.security import hash_password
from app.models.user import User


async def main():
    async with AsyncSessionLocal() as db:
        admin = User(
            email="admin@itsm.com",
            name="Admin User",
            password_hash=hash_password("Admin@123"),
            role="admin",
        )
        db.add(admin)
        await db.commit()
        print("Demo admin created: admin@itsm.com / Admin@123")


if __name__ == "__main__":
    asyncio.run(main())
