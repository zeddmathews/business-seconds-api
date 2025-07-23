from datetime import date
import asyncio
import asyncpg
from app.utils.holiday_utils import seed_public_holidays
from app.config import DB_URL


async def run_seed():
    conn = await asyncpg.connect(DB_URL)
    try:
        await seed_public_holidays(conn, year_start=date.today().year, years=10)
        print("Holidays seeded")
    except asyncpg.exceptions.PostgresError as e:
        print(f"Database error occured: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(run_seed())
