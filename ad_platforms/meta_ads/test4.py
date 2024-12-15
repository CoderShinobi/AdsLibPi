from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign

import ad_platforms.meta_ads.meta_campaign_manager as meta_c_manager

# Initialize the FacebookAdsApi with your access token


try:
    # Access the AdAccount
    c_manager = meta_c_manager.MetaAdsManager(meta_c_manager.config)


    # Retrieve campaigns
    campaigns = c_manager.get_campaigns()
    
    for campaign in campaigns:
        campaign_details = campaign
        if campaign_details:
            print(f"Campaign ID: {campaign_details[Campaign.Field.id]}, Campaign Name: {campaign_details[Campaign.Field.name]}")
    
except Exception as e:
    print(f"Failed to retrieve campaigns: {e}")