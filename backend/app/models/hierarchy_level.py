from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from app.database import Base


class HierarchyLevel(Base):
    __tablename__ = "hierarchy_levels"

    id = Column(String, primary_key=True)
    org_id = Column(String, ForeignKey("organizations.id"), nullable=False)

    level_number = Column(Integer, nullable=False)
    level_name = Column(String, nullable=False)
    department = Column(String)

    parent_ids = Column(ARRAY(String))

    zone = Column(Integer)
