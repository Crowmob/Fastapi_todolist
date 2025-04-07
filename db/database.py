import dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
import os

dotenv.load_dotenv()
db_url = os.getenv("DATABASE_URL")

engine = create_async_engine(db_url, echo=True)
async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Close session
async def disconnect_db():
    async with async_session_maker() as session:
        await session.close()
