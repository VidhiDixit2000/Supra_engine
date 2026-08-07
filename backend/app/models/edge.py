from sqlalchemy import (
    Column,
    String,
    Float,
    ForeignKey
)
from app.database import Base


class Edge(Base):
    __tablename__ = "edges"

    id = Column(String, primary_key=True)

    source_id = Column(
        String,
        ForeignKey("knowledge_nodes.id"),
        nullable=False,
    )

    target_id = Column(
        String,
        ForeignKey("knowledge_nodes.id"),
        nullable=False,
    )

    edge_type = Column(String)

    confidence = Column(Float)
