from abc import ABC, abstractmethod
from src.core.domain.models import CloudResource


class CloudScannerPort(ABC):
    
    @abstractmethod
    def scan_unutilized_resources(self) -> list[CloudResource]:
        """
        Bulut ortamındaki tüm atıl ve gereksiz maliyet üreten kaynakları tarar.
        Herhangi bir bulut sağlayıcıya özel mantık içermez, generic domain modeli döner.
        """
        pass