from sqlalchemy import Column, Integer, func, DateTime

from app.infrastructures.database.database_infrastructure import Base

class AbstractModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)