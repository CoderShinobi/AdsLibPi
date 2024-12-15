import sys
#sys.path.append('/opt/homebrew/lib/python2.7/site-packages') # Replace this with the place you installed facebookads using pip
#sys.path.append('/opt/homebrew/lib/python2.7/site-packages/facebook_business-3.0.0-py2.7.egg-info') # same as above

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
import ad_platforms.meta_ads.meta_campaign_manager as meta_c_manager

try:
    c_manager = meta_c_manager.MetaAdsManager(meta_c_manager.config)
    campaign_id = '120212429829270678'
    c_manager.delete_campaign(campaign_id)
except Exception as e:
    print(f"An error occurred: {e}")