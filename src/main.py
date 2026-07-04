from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.config import settings
from src.adapters.db_models import Base
from src.adapters.mock_cloud_adapter import MockCloudAdapter
from src.adapters.openai_adapter import OpenAIAdapter
from src.adapters.sqlalchemy_repository import SQLAlchemyRecommendationRepository
from src.adapters.slack_adapter import SlackAdapter
from src.core.services.optimization import OptimizationService
from fastapi import FastAPI, Depends, HTTPException
from src.core.domain.models import RecommendationStatus
from src.adapters.boto3_aws_adapter import Boto3AwsAdapter

# SQLite yerel veritabanı bağlantısı (Prod'da burası postgresql://... olacak)
DATABASE_URL = "sqlite:///./data/cloudtrim.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tabloları uygulama başlarken otomatik oluştur (Ufak çaplı migration)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, version="1.1.0")


# Her HTTP isteğinde veritabanı oturumu açıp kapatan güvenli bağımlılık
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_optimization_service(db: Session = Depends(get_db)) -> OptimizationService:
    scanner_adapter = MockCloudAdapter()
    ai_adapter = OpenAIAdapter()
    repo_adapter = SQLAlchemyRecommendationRepository(db_session=db) # Enjeksiyon
    
    return OptimizationService(scanner=scanner_adapter, ai_service=ai_adapter, repository=repo_adapter)


def get_optimization_service(db: Session = Depends(get_db)) -> OptimizationService:
    # DEĞİŞEN SATIR: Artık sistemi canlı AWS motoruna bağlıyoruz!
    scanner_adapter = Boto3AwsAdapter() 
    ai_adapter = OpenAIAdapter()
    repo_adapter = SQLAlchemyRecommendationRepository(db_session=db)
    
    return OptimizationService(scanner=scanner_adapter, ai_service=ai_adapter, repository=repo_adapter)


@app.post("/api/v1/recommendations/{rec_id}/apply", tags=["FinOps Actions"])
def apply_recommendation(rec_id: str, db: Session = Depends(get_db)):
    """
    Belirli bir maliyet tasarruf önerisini 'applied' (uygulandı) durumuna getirir.
    Müşteri sunucuyu kapattığında bu uç nokta tetiklenir.
    """
    repo = SQLAlchemyRecommendationRepository(db_session=db)
    recommendation = repo.get_by_id(rec_id)
    
    if not recommendation:
        raise HTTPException(status_code=404, detail="Tasarruf önerisi bulunamadı.")
    updated_rec = recommendation.model_copy(update={"status": RecommendationStatus.APPLIED})
    repo.save(updated_rec)
    return {"success": True, "message": f"Öneri [{rec_id}] başarıyla uygulandı olarak işaretlendi."}


@app.post("/api/v1/recommendations/{rec_id}/dismiss", tags=["FinOps Actions"])
def dismiss_recommendation(rec_id: str, db: Session = Depends(get_db)):
    """
    Belirli bir maliyet tasarruf önerisini 'dismissed' (reddedildi/gizlendi) durumuna getirir.
    """
    repo = SQLAlchemyRecommendationRepository(db_session=db)
    recommendation = repo.get_by_id(rec_id)
    
    if not recommendation:
        raise HTTPException(status_code=404, detail="Tasarruf önerisi bulunamadı.")
        
    updated_rec = recommendation.model_copy(update={"status": RecommendationStatus.DISMISSED})
    repo.save(updated_rec)
    
    return {"success": True, "message": f"Öneri [{rec_id}] reddedildi ve panelden gizlendi."}


@app.get("/api/v1/optimize", tags=["FinOps Operations"])
def trigger_optimization(
    service: OptimizationService = Depends(get_optimization_service)
):
    recommendations = service.generate_recommendations()
    total_savings = sum(r.potential_monthly_savings for r in recommendations)
    
    slack_notifier = SlackAdapter()
    slack_notifier.send_savings_report(
        total_suggestions=len(recommendations),
        total_savings=total_savings,
        recommendations=recommendations
    )
    
    return {
        "success": True,
        "summary": {
            "total_suggestions_found": len(recommendations),
            "total_estimated_monthly_savings_usd": round(total_savings, 2)
        },
        "data": recommendations
    }
