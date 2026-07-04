import uuid
from src.core.ports.cloud_scanner import CloudScannerPort
from src.core.ports.ai_service import AIServicePort
from src.core.ports.repository import RecommendationRepositoryPort
from src.core.domain.models import CloudResource, CostRecommendation, ResourceType, RecommendationStatus


class OptimizationService:
    def __init__(self, scanner: CloudScannerPort, ai_service: AIServicePort, repository: RecommendationRepositoryPort):
        self._scanner = scanner
        self._ai_service = ai_service
        self._repository = repository  # [YENİ]

    def generate_recommendations(self) -> list[CostRecommendation]:
        raw_resources = self._scanner.scan_unutilized_resources()
        processed_recommendations = []

        for resource in raw_resources:
            # 1. Önce bu kaynak için zaten kayıtlı bir aktif önerimiz var mı bak (Maliyet Bariyeri)
            existing_rec = self._repository.get_by_resource_id(resource.resource_id)
            if existing_rec:
                processed_recommendations.append(existing_rec)
                continue

            # 2. Eğer yoksa dinamik kural motorunu çalıştır
            recommendation = self._apply_dynamic_rules(resource)
            if recommendation:
                # 3. Yeni üretilen öneriyi kalıcı olarak veritabanına yaz
                saved_rec = self._repository.save(recommendation)
                processed_recommendations.append(saved_rec)

        return processed_recommendations

    def _apply_dynamic_rules(self, resource: CloudResource) -> CostRecommendation | None:
        action = None
        savings = 0.0
        metrics = resource.metrics

        if resource.resource_type == ResourceType.EC2:
            avg_cpu = metrics.get("avg_cpu_utilization", 100.0)
            if avg_cpu < 5.0:
                action = f"Stop Instance (Critical Low CPU: {avg_cpu}%)"
                savings = resource.current_monthly_cost
            else:
                return None

        elif resource.resource_type == ResourceType.EBS:
            days_unattached = metrics.get("days_unattached", 0)
            if days_unattached > 0:
                action = f"Delete Volume (Unattached for {days_unattached} days)"
                savings = resource.current_monthly_cost

        elif resource.resource_type == ResourceType.RDS:
            connections = metrics.get("active_connections", -1)
            if connections == 0:
                action = "Snapshot & Delete (Database has 0 active connections)"
                savings = resource.current_monthly_cost * 0.80

        if not action:
            return None

        # AI sadece yepyeni bir kaynak ilk defa keşfedildiğinde tetikleniyor! (Para kazandıran hamle)
        ai_summary = self._ai_service.analyze_recommendation(
            resource_type=resource.resource_type.value,
            action=action,
            cost=resource.current_monthly_cost,
            savings=savings
        )

        return CostRecommendation(
            id=str(uuid.uuid4()),
            resource=resource,
            potential_monthly_savings=savings,
            action_item=action,
            ai_analysis=ai_summary,
            status=RecommendationStatus.ACTIVE
        )