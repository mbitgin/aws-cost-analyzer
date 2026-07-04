from abc import ABC, abstractmethod
from src.core.domain.models import CostRecommendation


class RecommendationRepositoryPort(ABC):

    @abstractmethod
    def get_by_resource_id(self, resource_id: str) -> CostRecommendation | None:
        """Veritabanında ilgili kaynağa ait kayıtlı bir öneri olup olmadığına bakar."""
        pass

    @abstractmethod
    def save(self, recommendation: CostRecommendation) -> CostRecommendation:
        """Yeni bir öneriyi veritabanına kaydeder veya günceller."""
        pass

    @abstractmethod
    def get_all_active(self) -> list[CostRecommendation]:
        """Sistemdeki tüm aktif (applied veya dismissed olmamış) önerileri getirir."""
        pass

    @abstractmethod
    def get_by_id(self, recommendation_id: str) -> CostRecommendation | None:
        """ID üzerinden tekil bir öneriyi veritabanından getirir."""
        pass