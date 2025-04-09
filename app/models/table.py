from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    seats = Column(Integer, nullable=False)
    location = Column(String, nullable=True)

    reservations = relationship("Reservation", back_populates="table", cascade="all, delete-orphan")
