# ad_campaign_data.py
from pydantic import BaseModel
from enum import Enum
from typing import List, Dict, Any
from datetime import datetime

class Platform(str, Enum):
    GOOGLE = 'google'
    META = 'meta'

class AdCampaignData(BaseModel):
    name: str
    status: str
    budget: float
    start_date: datetime
    end_date: datetime
    platforms: List[Platform]
    platform_specific_data: Dict[Platform, Dict[str, Any]]