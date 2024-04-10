from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# database.py에서 생성한 Base import
from database import Base


# Base를 상속 받아 SQLAlchemy model 생성
class User(Base):
    # 해당 모델이 사용할 table 이름 지정
    __tablename__ = "users"

    # Model의 attribute(column) 생성 -> "="를 사용하여 속성을 정의
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # 다른 테이블과의 관계 생성
    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


from typing import List, Union

from pydantic import BaseModel


# pydantic 라이브러리의 BaseModel 클래스를 상속 받아 ItemBase 생성 -> ":"를 사용하여 속성을 정의
class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


# API에서 데이터를 읽을 때/반환할 때 사용될 모델
class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# UserBase 생성
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True

#..


from sqlalchemy.orm import Session

# 기존에 생성한 모델과 스키마 불러오기
import models, schema


# 데이터 읽기 - ID로 사용자 불러오기
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# 데이터 읽기 - Email로 사용자 불러오기
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# 데이터 읽기 - 여러 사용자 불러오기
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# 데이터 생성하기
def create_user(db: Session, user: schema.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"

    # SQLAlchemy 모델 인스턴스 만들기
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)  # DB에 해당 인스턴스 추가하기
    db.commit()  # DB의 변경 사항 저장하기
    db.refresh(db_user)  # 생성된 ID와 같은 DB의 새 데이터를 포함하도록 새로고침
    return db_user


# 데이터 읽기 - 여러 항목 읽어오기
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schema.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item