# ad_platform_manager.py
from abc import ABC, abstractmethod
from config.ad_campaign_data import AdCampaign

class AdCampaignManager(ABC):
    @abstractmethod
    def create_campaign(self, data: AdCampaign):
        pass

    @abstractmethod
    def update_campaign(self, campaign_id: str, data: AdCampaign):
        pass

    @abstractmethod
    def delete_campaign(self, campaign_id: str):
        pass