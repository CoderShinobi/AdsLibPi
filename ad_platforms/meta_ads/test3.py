import sys
#sys.path.append('/opt/homebrew/lib/python2.7/site-packages') # Replace this with the place you installed facebookads using pip
#sys.path.append('/opt/homebrew/lib/python2.7/site-packages/facebook_business-3.0.0-py2.7.egg-info') # same as above

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
import ad_platforms.meta_ads.meta_campaign_manager as meta_c_manager

try:
    c_manager = meta_c_manager.MetaAdsManager(meta_c_manager.config)
    campaign_id = '120212430479090678'


    data = {
        'name': 'My Meta Campaign',  # campaign_name in MetaCampaign
        'status': 'PAUSED',
        'objective': 'OUTCOME_TRAFFIC',
        'specialAdCategories': ['NONE'],
        'specialAdCategoryCountry': ['IN'],
        'date_preset': 'last_30d',
        'time_range': {'since': '2024-01-01', 'until': '2024-01-31'},
        'daily_budget': 100,
        'lifetime_budget': 10000,
        'bid_strategy': 'LOWEST_COST_WITHOUT_CAP',
        'start_time': '2024-01-01T00:00:00',
        'stop_time': '2024-12-31T23:59:59',
        'created_time': '2023-01-01T00:00:00',
        'updated_time': '2023-12-01T00:00:00',
        'buying_type': 'AUCTION'
    }


    c_manager.update_campaign(campaign_id,data);
except Exception as e:
    print(f"An error occurred: {e}")