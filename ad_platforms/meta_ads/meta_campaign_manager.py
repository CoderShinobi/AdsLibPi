# meta_ads_manager.py
import os
import logging
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from interfaces.ad_campaign_manager import AdCampaignManager

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration
class MetaAdsConfig:
    def __init__(self):
        self.access_token = os.getenv('META_ACCESS_TOKEN')
        self.account_id = os.getenv('META_ACCOUNT_ID')
        self.app_id = os.getenv('META_APP_ID')
        self.app_secret = os.getenv('META_APP_SECRET')

config = MetaAdsConfig()

# Logger setup
logger = logging.getLogger('MetaAdsManager')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# Response interfaces
class MetaError(Exception):
    def __init__(self, message, code=None):
        self.message = message
        self.code = code

class CampaignSuccessResponse:
    def __init__(self, success, id, platform_response):
        self.success = success
        self.id = id
        self.platform_response = platform_response

class CampaignErrorResponse:
    def __init__(self, success, id, platform_response):
        self.success = success
        self.id = id
        self.platform_response = platform_response

class DeleteResponse:
    def __init__(self, success):
        self.success = success

class MetaAdsManager(AdCampaignManager):
    def __init__(self, config):
        self.logger = logger
        self.logger.info('Initializing Meta Ads Manager')
        FacebookAdsApi.init(config.app_id, config.app_secret, config.access_token)
        self.ad_account = AdAccount(f'act_{config.account_id}')
        logger.info(self.ad_account.get_id())

    def create_campaign(self, data):
        self.logger.info(f'Creating campaign: {data["name"]}')

        meta_data = data
        if not meta_data:
            self.logger.error('Meta campaign data is missing')
            return CampaignErrorResponse(False, '', {'message': 'Meta campaign data is required'})

        if not data.get('name') or not data.get('status'):
            self.logger.error('Missing required campaign fields')
            return CampaignErrorResponse(False, '', {'message': 'Campaign name and status are required'})

        try:
            campaign = self.ad_account.create_campaign(
                fields=['id'],
                params={
                    'name': data['name'],
                    'status': data['status'],
                    'objective': meta_data['objective'],
                    'special_ad_categories': meta_data['specialAdCategories'],
                    'special_ad_category_country': meta_data['specialAdCategoryCountry'],
                    'date_preset': meta_data.get('date_preset'),
                    'time_range': meta_data.get('time_range'),
                    'lifetime_budget': meta_data.get('lifetime_budget'),
                    'bid_strategy': meta_data.get('bid_strategy'),
                    'start_time': meta_data.get('start_time'),
                    'stop_time': meta_data.get('stop_time'),
                    'created_time': meta_data.get('created_time'),
                    'updated_time': meta_data.get('updated_time'),
                    'buying_type': meta_data.get('buying_type', 'AUCTION')
                }
            )
            self.logger.info(f'Campaign created successfully: {campaign["id"]}')
            return CampaignSuccessResponse(True, campaign['id'], campaign)
        except Exception as error:
            self.logger.error(f'Error creating campaign: {str(error)}')
            return CampaignErrorResponse(False, '', {'message': str(error)})
        

    def update_campaign(self, campaign_id, meta_data):
        if not campaign_id:
            self.logger.error('Campaign ID is required')
            return CampaignErrorResponse(False, '', {'message': 'Campaign ID is required'})
    
        self.logger.info(f'Updating campaign: {campaign_id}')
    
        if not meta_data:
            self.logger.error('Meta campaign data is missing')
            return CampaignErrorResponse(False, campaign_id, {'message': 'Meta campaign data is required'})
    
        if not meta_data.get('name') or not meta_data.get('status'):
            self.logger.error('Missing required campaign fields')
            return CampaignErrorResponse(False, campaign_id, {'message': 'Campaign name and status are required'})
    
        try:
            campaign = Campaign(campaign_id)
            campaign.update({
                'name': meta_data['name'],
                'status': meta_data['status'],
                'objective': meta_data.get('objective'),
                'special_ad_categories': meta_data.get('special_ad_categories'),
                'special_ad_categories_country': meta_data.get('special_ad_categories_country'),
                'date_preset': meta_data.get('date_preset'),
                'time_range': meta_data.get('time_range'),
                'daily_budget': meta_data.get('daily_budget'),
                'lifetime_budget': meta_data.get('lifetime_budget'),
                'bid_strategy': meta_data.get('bid_strategy'),
                'buying_type': meta_data.get('buying_type')
            })
            self.logger.info(f'Campaign updated successfully: {campaign_id}')
            return CampaignSuccessResponse(True, campaign_id, campaign)
        except Exception as error:
            self.logger.error(f'Failed to update campaign: {str(error)}')
            return CampaignErrorResponse(False, campaign_id, {'message': str(error)})

    def delete_campaign(self, campaign_id):
        if not campaign_id:
            self.logger.error('Campaign ID is required for deletion')
            return DeleteResponse(False)

        try:
            campaign = Campaign(campaign_id)
            campaign.remote_delete()
            self.logger.info(f'Campaign deleted successfully: {campaign_id}')
            return DeleteResponse(True)
        except Exception as error:
            self.logger.error(f'Error deleting campaign: {str(error)}')
            return DeleteResponse(False)

    def get_campaigns(self):
        try:
            campaigns = self.ad_account.get_campaigns(fields=[Campaign.Field.id, Campaign.Field.name])
            return campaigns
        except Exception as error:
            self.logger.error(f'Error retrieving campaigns: {str(error)}')
            return CampaignErrorResponse(False, '', {'message': str(error)})