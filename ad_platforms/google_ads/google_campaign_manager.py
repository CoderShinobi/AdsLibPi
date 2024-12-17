from interfaces.ad_campaign_manager import AdCampaignManager
from config.ad_campaign_data import GoogleAdsCampaign
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import datetime
import uuid
import os
import logging
from dotenv import load_dotenv
load_dotenv()

class GoogleCampaignManager(AdCampaignManager):
    def __init__(self, client=None):
        logging.basicConfig(level=logging.INFO)
        log = logging.getLogger(__name__)
        if client:
            self.client = client
        else:
            self.client = GoogleAdsClient.load_from_storage(version="v18")
            self.client.login_customer_id = os.getenv('GOOGLE_LOGIN_CUSTOMER_ID')
        self._DATE_FORMAT = "%Y%m%d"
        self.customer_id = os.getenv('GOOGLE_ADS_CUSTOMER_ID')
        log.info(f'Google Campaign Manager initialized with customer ID: {self.customer_id} and login customer ID: {self.client.login_customer_id}');
        
    def set_campaign_bidding_strategy(self, campaign, data):
        """Sets the bidding strategy for a campaign"""
        if data.bidding_strategy == "Target ROAS":
            campaign.bidding_strategy_type = (
                self.client.enums.BiddingStrategyTypeEnum.TARGET_ROAS
            )
            campaign.target_roas = self.client.get_type("TargetRoas")
            campaign.target_roas.target_roas = 3.5  # 350% ROAS target
            
        elif data.bidding_strategy == "Manual CPC":
            campaign.bidding_strategy_type = (
                self.client.enums.BiddingStrategyTypeEnum.MANUAL_CPC
            )
            campaign.manual_cpc = self.client.get_type("ManualCpc")
        else:
            raise ValueError(f"Unsupported bidding strategy: {data.bidding_strategy}")

    def create_campaign(self, data: GoogleAdsCampaign):
        """Creates a campaign with associated budget."""
        campaign_budget_service = self.client.get_service("CampaignBudgetService")
        campaign_service = self.client.get_service("CampaignService")

        # Create budget
        campaign_budget_operation = self.client.get_type("CampaignBudgetOperation")
        campaign_budget = campaign_budget_operation.create
        campaign_budget.name = f"{data.campaign_name} Budget {uuid.uuid4()}"
        campaign_budget.delivery_method = self.client.enums.BudgetDeliveryMethodEnum.STANDARD
        campaign_budget.amount_micros = data.budget * 1_000_000  # Convert to micros

        try:
            # Add budget
            budget_response = campaign_budget_service.mutate_campaign_budgets(
                customer_id=self.customer_id,
                operations=[campaign_budget_operation]
            )
            campaign_budget_resource_name = budget_response.results[0].resource_name

            # Create campaign
            campaign_operation = self.client.get_type("CampaignOperation")
            campaign = campaign_operation.create
            campaign.name = data.campaign_name

            # Map campaign_type to AdvertisingChannelTypeEnum
            channel_type_enum = self.client.enums.AdvertisingChannelTypeEnum
            campaign_type_mapping = {
                "Search": channel_type_enum.SEARCH,
                "Display": channel_type_enum.DISPLAY,
                "Shopping": channel_type_enum.SHOPPING,
                "Video": channel_type_enum.VIDEO,
                "App": channel_type_enum.MULTI_CHANNEL,
            }
            campaign.advertising_channel_type = campaign_type_mapping.get(
                data.campaign_type,
                channel_type_enum.SEARCH
            )

            # Set status
            status_mapping = {
                "ENABLED": self.client.enums.CampaignStatusEnum.ENABLED,
                "PAUSED": self.client.enums.CampaignStatusEnum.PAUSED,
                "REMOVED": self.client.enums.CampaignStatusEnum.REMOVED,
            }
            campaign.status = status_mapping.get(data.status, self.client.enums.CampaignStatusEnum.PAUSED)

            # Set bidding strategy
            self.set_campaign_bidding_strategy(campaign, data)
            #if data.bidding_strategy == "Manual CPC":
             #   campaign.manual_cpc.enhanced_cpc_enabled = True

            # Set budget
            campaign.campaign_budget = campaign_budget_resource_name

            if data.campaign_type != "Video":
                campaign.network_settings.target_google_search = True
            # Set network settings
            campaign.network_settings.target_google_search = "Search Network" in data.networks
            campaign.network_settings.target_search_network = "Search Partners" in data.networks
            campaign.network_settings.target_content_network = "Display Network" in data.networks
            campaign.network_settings.target_partner_search_network = False

            # Set dates
            if data.start_time:
                start_date = datetime.datetime.strptime(
                    data.start_time, "%Y-%m-%dT%H:%M:%S"
                ).strftime(self._DATE_FORMAT)
                campaign.start_date = start_date
            else:
                campaign.start_date = datetime.date.today().strftime(self._DATE_FORMAT)

            if data.stop_time:
                end_date = datetime.datetime.strptime(
                    data.stop_time, "%Y-%m-%dT%H:%M:%S"
                ).strftime(self._DATE_FORMAT)
                campaign.end_date = end_date

            # Add campaign
            campaign_response = campaign_service.mutate_campaigns(
                customer_id=self.customer_id,
                operations=[campaign_operation]
            )
            return campaign_response.results[0].resource_name

        except GoogleAdsException as ex:
            self._handle_googleads_exception(ex)
            raise

    def update_campaign(self, campaign_id: str, data: GoogleAdsCampaign):
        """Updates an existing campaign."""
        campaign_service = self.client.get_service("CampaignService")
        campaign_operation = self.client.get_type("CampaignOperation")
        campaign = campaign_operation.update
        campaign.resource_name = campaign_service.campaign_path(self.customer_id, campaign_id)

        if data.campaign_name:
            campaign.name = data.campaign_name

        if data.status:
            status_enum = self.client.enums.CampaignStatusEnum
            status_mapping = {
                "ENABLED": status_enum.ENABLED,
                "PAUSED": status_enum.PAUSED,
                "REMOVED": status_enum.REMOVED,
            }
            campaign.status = status_mapping.get(data.status, status_enum.PAUSED)

        # ... handle other fields as needed

        # Use FieldMask to specify fields to be updated
        field_mask = self.client.get_type("FieldMask")
        field_mask.paths.append("name")
        field_mask.paths.append("status")
        # ... add other fields to the mask

        campaign_operation.update_mask.CopyFrom(field_mask)

        try:
            campaign_response = campaign_service.mutate_campaigns(
                customer_id=self.customer_id,
                operations=[campaign_operation]
            )
            return campaign_response.results[0].resource_name
        except GoogleAdsException as ex:
            self._handle_googleads_exception(ex)
            raise

    def delete_campaign(self, campaign_id: str):
        """Deletes a campaign."""
        campaign_service = self.client.get_service("CampaignService")
        campaign_operation = self.client.get_type("CampaignOperation")
        campaign_operation.remove = campaign_service.campaign_path(self.customer_id, campaign_id)

        try:
            campaign_response = campaign_service.mutate_campaigns(
                customer_id=self.customer_id,
                operations=[campaign_operation]
            )
            return campaign_response.results[0].resource_name
        except GoogleAdsException as ex:
            self._handle_googleads_exception(ex)
            raise

    def _handle_googleads_exception(self, exception):
        """Handles Google Ads API exceptions."""
        print(
            f'Request with ID "{exception.request_id}" failed with status '
            f'"{exception.error.code().name}" and includes the following errors:'
        )
        for error in exception.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")