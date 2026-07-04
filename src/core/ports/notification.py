from abc import ABC, abstractmethod


class NotificationPort(ABC):

    @abstractmethod
    def send_savings_report(self, total_suggestions: int, total_savings: float, recommendations: list) -> bool:
        """
        Şirketin iletişim kanalına (Slack/Teams) haftalık/anlık maliyet raporunu fırlatır.
        """
        pass