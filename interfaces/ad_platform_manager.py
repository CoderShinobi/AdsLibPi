# ad_platform_manager.py
from abc import ABC, abstractmethod
from interfaces.ad_campaign_data import AdCampaignData

class AdPlatformManager(ABC):
    @abstractmethod
    def create_campaign(self, data: AdCampaignData):
        pass

    @abstractmethod
    def update_campaign(self, campaign_id: str, data: AdCampaignData):
        pass

    @abstractmethod
    def delete_campaign(self, campaign_id: str):
        pass