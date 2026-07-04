from sqlalchemy.orm import Session
from src.core.ports.repository import RecommendationRepositoryPort
from src.core.domain.models import CostRecommendation, CloudResource, ResourceType, RecommendationStatus
from src.adapters.db_models import DBRecommendation


class SQLAlchemyRecommendationRepository(RecommendationRepositoryPort):

    def __init__(self, db_session: Session):
        self._session = db_session

    def get_by_resource_id(self, resource_id: str) -> CostRecommendation | None:
        db_rec = self._session.query(DBRecommendation).filter(DBRecommendation.resource_id == resource_id).first()
        if not db_rec:
            return None
        return self._to_domain(db_rec)

    def save(self, recommendation: CostRecommendation) -> CostRecommendation:
        # Önce mevcut kayıt var mı kontrol et (Upsert mantığı)
        db_rec = self._session.query(DBRecommendation).filter(DBRecommendation.id == recommendation.id).first()
        
        if not db_rec:
            db_rec = DBRecommendation(
                id=recommendation.id,
                resource_id=recommendation.resource.resource_id,
                resource_type=recommendation.resource.resource_type.value,
                current_monthly_cost=recommendation.resource.current_monthly_cost,
                region=recommendation.resource.region,
                potential_monthly_savings=recommendation.potential_monthly_savings,
                action_item=recommendation.action_item,
                ai_analysis=recommendation.ai_analysis,
                status=recommendation.status.value,
                created_at=recommendation.created_at
            )
            self._session.add(db_rec)
        else:
            db_rec.status = recommendation.status.value
            db_rec.ai_analysis = recommendation.ai_analysis

        self._session.commit()
        return self._to_domain(db_rec)

    def get_all_active(self) -> list[CostRecommendation]:
        db_recs = self._session.query(DBRecommendation).filter(DBRecommendation.status == "active").all()
        return [self._to_domain(r) for r in db_recs]

    def _to_domain(self, db_rec: DBRecommendation) -> CostRecommendation:
        # DB Verisini temiz Domain Nesnesine dönüştüren yardımcı metod (Data Mapper)
        return CostRecommendation(
            id=db_rec.id,
            resource=CloudResource(
                resource_id=db_rec.resource_id,
                resource_type=ResourceType(db_rec.resource_type),
                current_monthly_cost=db_rec.current_monthly_cost,
                region=db_rec.region
            ),
            potential_monthly_savings=db_rec.potential_monthly_savings,
            action_item=db_rec.action_item,
            ai_analysis=db_rec.ai_analysis,
            status=RecommendationStatus(db_rec.status),
            created_at=db_rec.created_at
        )
    
    def get_by_id(self, recommendation_id: str) -> CostRecommendation | None:
        db_rec = self._session.query(DBRecommendation).filter(DBRecommendation.id == recommendation_id).first()
        if not db_rec:
            return None
        return self._to_domain(db_rec)