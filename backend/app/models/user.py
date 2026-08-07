from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey)
    
from sqlalchemy.dialects.postgresql import ARRAY
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)

    org_id = Column(
        String,
        ForeignKey("organizations.id"),
        nullable=False,
    )

    name = Column(String)

    role = Column(String)

    department = Column(String)

    ceiling_level = Column(Integer)

    write_ceiling = Column(Integer)

    compliance_clearance = Column(ARRAY(String))

    status = Column(String)
