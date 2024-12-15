from ad_platforms.google_ads.google_campaign_manager import GoogleCampaignManager
from config.ad_campaign_data import GoogleAdsCampaign

def main():
    # Create an instance of GoogleCampaignManager
    campaign_manager = GoogleCampaignManager()

    # Create a sample GoogleAdsCampaign data object
    campaign_data = GoogleAdsCampaign(
        campaign_id='1',
        campaign_name="kutcoix",
        budget=100,  # Budget in the currency's smallest unit
        campaign_type="Video",
        locations=["United States","India"],
        languages=["English","Hindi"],
        status="PAUSED",
        bidding_strategy="Manual CPC",
        networks=["Google Search Network", "Google Display Network"],
        start_time="2025-01-01T00:00:00",
        stop_time="2025-12-31T23:59:59"
    )

    # Call the create_campaign method
    try:
        campaign_resource_name = campaign_manager.create_campaign(campaign_data)
        print(f"Campaign created with resource name: {campaign_resource_name}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()