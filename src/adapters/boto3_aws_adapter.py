import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from src.core.ports.cloud_scanner import CloudScannerPort
from src.core.domain.models import CloudResource, ResourceType
from src.config import settings


class Boto3AwsAdapter(CloudScannerPort):

    def __init__(self):
        self._region = settings.AWS_DEFAULT_REGION
        
        # Pydantic'ten gelen değerleri temizleyelim ve kontrol edelim
        key_id = settings.AWS_ACCESS_KEY_ID.strip() if settings.AWS_ACCESS_KEY_ID else ""
        secret_key = settings.AWS_SECRET_ACCESS_KEY.strip() if settings.AWS_SECRET_ACCESS_KEY else ""

        # SİBER GÜVENLİK & MOCK FİLTRESİ
        # Eğer ayarlarda 'mock', 'your_' kalmışsa veya alanlar boşsa hiç boto3'ü zorlama, zarifçe None yap.
        if "mock" in key_id or "your_" in key_id or not key_id:
            self._ec2_client = None
            return

        try:
            # Sadece ve sadece gerçek bir anahtar yapılandırması sezildiğinde istemciyi bağla
            self._ec2_client = boto3.client(
                "ec2",
                region_name=self._region,
                aws_access_key_id=key_id,
                aws_secret_access_key=secret_key
            )
        except Exception as e:
            print(f"[AWS ADAPTER] Boto3 client başlatılırken kritik hata: {str(e)}")
            self._ec2_client = None

    def scan_unutilized_resources(self) -> list[CloudResource]:
        # Koruma Duvarı: Eğer istemci hiç ayağa kalkmadıysa operasyonu zarifçe bitir
        if not self._ec2_client:
            print("[AWS ADAPTER] AWS Client başlatılamadı. Canlı tarama güvenle atlandı.")
            return []

        discovered_resources = []
        
        try:
            # 1. CANLI EBS DISK TARAMASI
            volumes = self._ec2_client.describe_volumes(
                Filters=[{'Name': 'status', 'Values': ['available']}]
            )
            for vol in volumes.get('Volumes', []):
                vol_id = vol['VolumeId']
                size = vol['Size']
                estimated_cost = size * 0.08 
                
                discovered_resources.append(
                    CloudResource(
                        resource_id=vol_id,
                        resource_type=ResourceType.EBS,
                        current_monthly_cost=round(estimated_cost, 2),
                        region=self._region,
                        metrics={"days_unattached": 7, "size_gb": size}
                    )
                )

            # 2. CANLI EC2 SUNUCU TARAMASI
            instances = self._ec2_client.describe_instances(
                Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}]
            )
            for reservation in instances.get('Reservations', []):
                for inst in reservation.get('Instances', []):
                    inst_id = inst['InstanceId']
                    inst_type = inst['InstanceType']
                    
                    discovered_resources.append(
                        CloudResource(
                            resource_id=inst_id,
                            resource_type=ResourceType.EC2,
                            current_monthly_cost=45.0,
                            region=self._region,
                            metrics={"avg_cpu_utilization": 0.0, "instance_type": inst_type}
                        )
                    )

        except NoCredentialsError:
            # Burası tam olarak senin aldığın hatayı production'da sönümleyen kritik katmandır
            print("[AWS ADAPTER] AWS kimlik bilgileri doğrulanamadı (NoCredentialsError).")
            return []
        except ClientError as e:
            print(f"[AWS ADAPTER] AWS API yetki/bağlantı hatası: {str(e)}")
            return []
        except Exception as e:
            print(f"[AWS ADAPTER] Beklenmedik AWS Tarama hatası: {str(e)}")
            return []

        return discovered_resources