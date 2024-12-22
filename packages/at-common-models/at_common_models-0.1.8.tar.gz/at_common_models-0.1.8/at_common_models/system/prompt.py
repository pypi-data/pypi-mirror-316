from sqlalchemy import Column, String, JSON
from at_common_models.base import BaseModel

class PromptModel(BaseModel):
    __tablename__ = "system_prompt"

    name = Column(String(255), primary_key=True, index=True)
    sys_tpl = Column(JSON, nullable=False)
    usr_tpl = Column(JSON, nullable=False)