from sqlalchemy import Column, String, JSON
from at_common_models.base import Base

class Task(Base):
    __tablename__ = "system_tasks"

    name = Column(String(255), primary_key=True, index=True)
    data = Column(JSON, nullable=False)