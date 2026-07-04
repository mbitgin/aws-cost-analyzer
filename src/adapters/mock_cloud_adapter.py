from src.core.ports.cloud_scanner import CloudScannerPort
from src.core.domain.models import CloudResource, ResourceType


class MockCloudAdapter(CloudScannerPort):
    
    def scan_unutilized_resources(self) -> list[CloudResource]:
        return [
            # 1. ATIL EC2 (CPU çok düşük, kesin aksiyon alınmalı)
            CloudResource(
                resource_id="i-0fa123456789abcdf",
                resource_type=ResourceType.EC2,
                current_monthly_cost=150.0,
                region="us-east-1",
                metrics={"avg_cpu_utilization": 2.1, "instance_type": "t3.large"}
            ),
            # 2. AKTİF EC2 (CPU yüksek, BU KAYNAK ATLANMALI)
            CloudResource(
                resource_id="i-0active987654321",
                resource_type=ResourceType.EC2,
                current_monthly_cost=300.0,
                region="us-east-1",
                metrics={"avg_cpu_utilization": 78.5, "instance_type": "m5.xlarge"}
            ),
            # 3. ATIL EBS DISK (12 gündür boşa dönüyor)
            CloudResource(
                resource_id="vol-0123456789voldisk",
                resource_type=ResourceType.EBS,
                current_monthly_cost=45.5,
                region="us-east-1",
                metrics={"days_unattached": 12, "size_gb": 100}
            ),
            # 4. ATIL RDS VERİTABANI (Bağlantı sayısı sıfır)
            CloudResource(
                resource_id="db-master-rds-cluster",
                resource_type=ResourceType.RDS,
                current_monthly_cost=450.0,
                region="eu-central-1",
                metrics={"active_connections": 0, "storage_type": "gp3"}
            )
        ]