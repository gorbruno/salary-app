from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import create_access_token, get_current_user
from app.utils import get_id_by_credentials
from app.utils import create_database_with_mockup_data
from app.settings import settings
from datetime import timedelta
from app.models import UserDTO, UserIdDTO, UserPromotionDTO, UserSalaryDTO
import uvicorn
import asyncio
from typing import Optional

app = FastAPI()

@app.post("/auth/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user: Optional[UserIdDTO] = await get_id_by_credentials(form_data.username, form_data.password) #type: ignore
    if user is None or form_data.username != user.username:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(user, expires=timedelta(minutes=settings.TIME_EXPIRES))
    return {"access_token": token, "token_type": "bearer"}

@app.get("/salary")
def get_salary(current_user: UserDTO = Depends(get_current_user)) -> UserSalaryDTO:
    return UserSalaryDTO.model_validate(current_user)

@app.get("/promotion")
def get_promotion_date(current_user: UserDTO = Depends(get_current_user)) -> UserPromotionDTO:
    return UserPromotionDTO.model_validate(current_user)

if __name__ == "__main__":
    if settings.CREATE_TABLE:
        asyncio.run(create_database_with_mockup_data("tests/test_users.csv"))
    uvicorn.run("main:app", host=settings.SERVICE_HOST, port=settings.SERVICE_PORT, reload=True)