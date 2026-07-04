from abc import ABC, abstractmethod


class AIServicePort(ABC):

    @abstractmethod
    def analyze_recommendation(self, resource_type: str, action: str, cost: float, savings: float) -> str:
        """
        Kural motorundan gelen verileri analiz ederek insan tarafından okunabilir stratejik bir özet üretir.
        """
        pass