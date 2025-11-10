from base_model import BaseModel
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Integer, Numeric


class BaseModel(DeclarativeBase):
    pass
