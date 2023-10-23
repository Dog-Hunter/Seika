from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine("sqlite+aiosqlite:///base.db", echo=True)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)