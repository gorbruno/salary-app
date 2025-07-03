import pytest
from app.database import recreate_db
import datetime
from app.utils import get_id_by_credentials, get_user_by_id, add_user, create_database_with_mockup_data

# тест функций взаимодецствия с пользователем
@pytest.mark.asyncio
async def test_user_utils():
    # сброс таблицы
    await recreate_db()

    user_data = {
        "username": "testuser",
        "password": "testpass",
        "salary": 1000,
        "promotion_date": datetime.datetime.strptime('12/15/25', '%m/%d/%y').date()
    }

    await add_user(**user_data)

    # проверка get_id_by_credentials
    user_id_dto = await get_id_by_credentials(user_data["username"], user_data["password"]) #type: ignore
    assert user_id_dto is not None
    assert user_id_dto.username == user_data["username"]

    # проверка get_user_by_id
    user_from_db = await get_user_by_id(user_id_dto.id) #type: ignore
    assert user_from_db is not None
    assert user_from_db.username == user_data["username"]
    assert user_from_db.password == user_data["password"]
    assert user_from_db.salary == user_data["salary"]
    assert user_from_db.promotion_date == user_data["promotion_date"]

# тест создания базы с данными
@pytest.mark.asyncio
async def test_database_with_mockup_data(tmp_path):
    csv_file = tmp_path / "test_data.csv"
    csv_content = (
        "username,password,salary,promotion_date\n"
        "user1,pass1,2000,01/01/23\n"
        "user2,pass2,3000,02/01/23\n"
    )
    csv_file.write_text(csv_content)

    await create_database_with_mockup_data(str(csv_file), drop_database=True, date_format="%m/%d/%y")

    user1 = await get_id_by_credentials("user1", "pass1") #type: ignore
    user2 = await get_id_by_credentials("user2", "pass2") #type: ignore

    assert user1 is not None
    assert user2 is not None

# тест неправильного пароля
@pytest.mark.asyncio
async def test_credentials_wrong_password():
    await recreate_db()

    user_data = {
        "username": "testuser",
        "password": "correctpass",
        "salary": 1000,
        "promotion_date": datetime.datetime.strptime('12/15/25', '%m/%d/%y').date()
    }
    await add_user(**user_data)

    user = await get_id_by_credentials(user_data["username"], "wrongpass") #type: ignore
    assert user is None

# тест неправильного id
@pytest.mark.asyncio
async def test_get_user_by_id_not_exist():
    await recreate_db()

    user = await get_user_by_id(99999) #type: ignore
    assert user is None