import enum
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base


class UserRole(str, enum.Enum):
    ADMIN = 'admin'
    COMPANY = 'company'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, unique=True, nullable=False)
    role = Column(Enum(UserRole, native_enum=False), nullable=False, default=UserRole.COMPANY.value)

    reservations = relationship('Reservation', back_populates='user')