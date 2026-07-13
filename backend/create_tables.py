"""
Quick way to create all tables without setting up Alembic migrations yet.
Run this once after your PostgreSQL database is created:

    python create_tables.py

Once you're comfortable, switch to Alembic migrations (see README) for
proper version-controlled schema changes — required for production apps.
"""
import asyncio
from app.core.db import engine, Base
from app.models import User, Asset  # noqa: F401  (import so tables register)


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully.")


if __name__ == "__main__":
    asyncio.run(main())
