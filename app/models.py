from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer, Date, UniqueConstraint
from pydantic import BaseModel, ConfigDict
import datetime
#делает атрибуты модели доступными для вызова
class Base(AsyncAttrs, DeclarativeBase):
    pass

# добавляет возможность валидировать модель orm в dto, переводит числа в текст
class CustomBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, coerce_numbers_to_str=True)

class UserORM(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint('username', 'password', name='unique_credentials'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)
    promotion_date = Column(Date, nullable=False)

    def __repr__(self) -> str:
        return f"<UserORM(id={self.id}, username={self.username}, password={self.password}, salary={self.salary}, promotion_date={self.promotion_date})>"
    

class UserDTO(CustomBaseModel):
    username: str
    password: str
    salary: float
    promotion_date: datetime.date

class UserIdDTO(CustomBaseModel):
    id: int
    username: str

class UserSalaryDTO(CustomBaseModel):
    username: str
    salary: int

class UserPromotionDTO(CustomBaseModel):
    username: str
    promotion_date: datetime.date