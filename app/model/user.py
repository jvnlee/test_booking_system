import enum
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base


class RoleEnum(str, enum.Enum):
    admin = 'admin'
    company = 'company'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, unique=True, nullable=False)
    role = Column(Enum(RoleEnum, native_enum=False), nullable=False, default=RoleEnum.company.value)

    reservations = relationship('Reservation', back_populates='user')