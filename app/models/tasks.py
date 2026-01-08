from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database.database import Base  # наш declarative_base
from sqlalchemy import BigInteger

class Task(Base):
    """ ORM-модель задачи.

        Представляет задачу пользователя в базе данных.
        Используется SQLAlchemy declarative mapping.
        """
    __tablename__ = "tasks"

    id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    user_id = Column(BigInteger, index=True)  # Telegram ID пользователя
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="pending")  # pending / in_progress / done
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())