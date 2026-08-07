from sqlalchemy import Column, String
from app.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    segment = Column(String)
    config = Column(String)