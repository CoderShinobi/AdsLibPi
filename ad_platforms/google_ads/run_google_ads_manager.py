# run_google_ads_manager.py
from ad_platforms.google_ads.google_ads_manager import GoogleAdsManager
from interfaces.ad_campaign_data import AdCampaignData
from datetime import date

def main():
    # Create an instance of AdCampaignData with the necessary attributes

    # Create an instance of GoogleAdsManager
    manager = GoogleAdsManager()

    # Call the create_campaign method
    manager.create_campaign()

if __name__ == "__main__":
    main()