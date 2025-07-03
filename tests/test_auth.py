import pytest
import datetime
from jose import jwt
from fastapi import HTTPException
from app.auth import create_access_token, get_current_user
from app.settings import settings
from app.models import UserDTO, UserIdDTO
from unittest.mock import patch, AsyncMock

@pytest.fixture
def user_id_dto():
    return UserIdDTO(id=123, username="testuser")

# проверка создания токена
def test_create_access_token(user_id_dto):
    token = create_access_token(user_id_dto)
    assert isinstance(token, str)
    payload = jwt.decode(token, settings.SECRET_TOKEN, algorithms=[settings.ENCRYPTION_ALGORITHM])
    assert payload["id"] == user_id_dto.id
    assert "exp" in payload

# тест валидации токена — валидный
@pytest.mark.asyncio
async def test_get_current_user_valid_token(user_id_dto):
    token = create_access_token(user_id_dto)

    test_user = UserDTO(username="testuser", password="testpwd", salary=1000, promotion_date=datetime.datetime.strptime('01/01/24', '%m/%d/%y').date())

    with patch("app.auth.get_user_by_id", new=AsyncMock(return_value=test_user)):
        user = await get_current_user(token=token)
        assert user is not None
        assert user.username == "testuser"
        assert user.password == "testpwd"
        assert user.salary == 1000
        assert user.promotion_date == datetime.datetime.strptime('01/01/24', '%m/%d/%y').date()

# тест валидации токена — инвалидный
@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    invalid_token = "bad.token.value"
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=invalid_token)
    assert excinfo.value.status_code == 401

# тест неправильного пользовтеля
@pytest.mark.asyncio
async def test_get_current_user_no_user_found(user_id_dto):
    token = create_access_token(user_id_dto)
    # мокаем get_user_by_id
    with patch("app.auth.get_user_by_id", new=AsyncMock(return_value=None)):
        with pytest.raises(HTTPException) as excinfo:
            await get_current_user(token=token)
        assert excinfo.value.status_code == 401

# тест пользовтеля без айди
@pytest.mark.asyncio
async def test_get_current_user_token_without_id():
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15)
    token = jwt.encode({"exp": expire}, settings.SECRET_TOKEN, algorithm=settings.ENCRYPTION_ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)
    assert excinfo.value.status_code == 401