from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class DBRecommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String, primary_key=True, index=True)
    resource_id = Column(String, unique=True, index=True, nullable=False)
    resource_type = Column(String, nullable=False)
    current_monthly_cost = Column(Float, nullable=False)
    region = Column(String, nullable=False)
    potential_monthly_savings = Column(Float, nullable=False)
    action_item = Column(String, nullable=False)
    ai_analysis = Column(String, nullable=True)
    status = Column(String, default="active", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)