from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class ResourceType(str, Enum):
    EC2 = "EC2"
    RDS = "RDS"
    EBS = "EBS"
    ELB = "ELB"


class RecommendationStatus(str, Enum):
    ACTIVE = "active"
    APPLIED = "applied"
    DISMISSED = "dismissed"


class CloudResource(BaseModel):
    model_config = ConfigDict(frozen=True)

    resource_id: str = Field(..., min_length=1, description="AWS Resource ARN or ID")
    resource_type: ResourceType
    current_monthly_cost: float = Field(..., ge=0.0)
    region: str
    # [YENİ] Esnek metrik sözlüğü (Örn: {"avg_cpu": 2.4, "days_unattached": 14})
    metrics: dict[str, float | int | str] = Field(default_factory=dict)


class CostRecommendation(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    id: str
    resource: CloudResource
    potential_monthly_savings: float = Field(..., ge=0.0)
    action_item: str = Field(..., description="Technical action like: Stop, Downsize, Delete")
    ai_analysis: str | None = None
    status: RecommendationStatus = RecommendationStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)