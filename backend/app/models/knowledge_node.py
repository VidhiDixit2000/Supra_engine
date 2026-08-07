from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Text,
    ForeignKey,
    DateTime
)
from sqlalchemy.dialects.postgresql import ARRAY
from app.database import Base

class KnowledgeNode(Base):
    __tablename__ = "knowledge_nodes"

    id = Column(String, primary_key=True)

    org_id = Column(String, ForeignKey("organizations.id"), nullable=False)

    hierarchy_level_id = Column(
        String,
        ForeignKey("hierarchy_levels.id"),
        nullable=False,
    )

    type = Column(String)
    title = Column(String)
    content = Column(Text)

    importance = Column(Float)
    zone = Column(Integer)

    status = Column(String)

    derivability_score = Column(Float)

    compliance_tags = Column(ARRAY(String))

    superseded_by = Column(String)

    department = Column(String)

    valid_until = Column(DateTime, nullable=True)