from app.database import init_db, recreate_db
import csv
from datetime import datetime
from app.utils import add_user

async def create_database_with_test_data(
        data: str,
        drop_database: bool = True,
        date_format: str = "%m/%d/%y"
    ) -> None:
    if drop_database:
        await recreate_db()
    else:
        await init_db()
    try:
        with open(data, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for n, row in enumerate(reader, 1):
                try:
                    row['salary'] = int(row['salary'])
                    row['promotion_date'] = datetime.strptime(row['promotion_date'], date_format)
                    await add_user(**row)
                except Exception as e:
                    raise ImportError(f"Error in row {n} ({row}): {e}")
    except Exception as e:
        raise ImportError(f"Cannot create database from table {data}: {e}")
    print(f"Data from {data} added into the database")