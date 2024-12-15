#!/usr/bin/env python
import argparse
import datetime
import os
import uuid

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from dotenv import load_dotenv
load_dotenv()

class GoogleAdsConfig:
    def __init__(self):
        self.GOOGLE_LOGIN_CUSTOMER_ID = os.getenv('GOOGLE_LOGIN_CUSTOMER_ID')
        self.GOOGLE_ADS_CUSTOMER_ID = os.getenv('GOOGLE_ADS_CUSTOMER_ID')

env = GoogleAdsConfig()

class GoogleAdsManager:
    def __init__(self):
        self.client = GoogleAdsClient.load_from_storage(version="v18")
        self.client.login_customer_id = env.GOOGLE_LOGIN_CUSTOMER_ID
        self._DATE_FORMAT = "%Y%m%d"

    def create_campaign_with_budget(self):
        """Creates a campaign with associated budget."""
        customer_id = env.GOOGLE_ADS_CUSTOMER_ID
        campaign_budget_service = self.client.get_service("CampaignBudgetService")
        campaign_service = self.client.get_service("CampaignService")



        # Create budget
        campaign_budget_operation = self.client.get_type("CampaignBudgetOperation")
        campaign_budget = campaign_budget_operation.create
        campaign_budget.name = f"Test Budget {uuid.uuid4()}"
        campaign_budget.delivery_method = self.client.enums.BudgetDeliveryMethodEnum.STANDARD
        campaign_budget.amount_micros = 500000

        try:
            # Add budget
            budget_response = campaign_budget_service.mutate_campaign_budgets(
                customer_id=customer_id,
                operations=[campaign_budget_operation]
            )
            
            # Create campaign
            campaign_operation = self.client.get_type("CampaignOperation")
            campaign = campaign_operation.create
            campaign.name = f"Test Campaign {uuid.uuid4()}"
            campaign.advertising_channel_type = (
                self.client.enums.AdvertisingChannelTypeEnum.SEARCH
            )
            campaign.status = self.client.enums.CampaignStatusEnum.PAUSED
            campaign.manual_cpc.enhanced_cpc_enabled = True
            campaign.campaign_budget = budget_response.results[0].resource_name

            # Set network settings
            campaign.network_settings.target_google_search = True
            campaign.network_settings.target_search_network = True
            campaign.network_settings.target_partner_search_network = False
            campaign.network_settings.target_content_network = True

            # Set dates
            start_time = datetime.date.today() + datetime.timedelta(days=1)
            campaign.start_date = datetime.date.strftime(start_time, self._DATE_FORMAT)
            end_time = start_time + datetime.timedelta(weeks=4)
            campaign.end_date = datetime.date.strftime(end_time, self._DATE_FORMAT)

            # Add campaign
            campaign_response = campaign_service.mutate_campaigns(
                customer_id=customer_id,
                operations=[campaign_operation]
            )
            
            return {
                'budget_id': budget_response.results[0].resource_name,
                'campaign_id': campaign_response.results[0].resource_name
            }

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

def main():
    #parser = argparse.ArgumentParser(description="Create Google Ads campaign with budget")
    #parser.add_argument("-c", "--customer_id", type=str, required=True,
    #                   help="The Google Ads customer ID")
    #args = parser.parse_args()

    manager = GoogleAdsManager()
    result = manager.create_campaign_with_budget()
    print(f"Created budget: {result['budget_id']}")
    print(f"Created campaign: {result['campaign_id']}")

if __name__ == "__main__":
    main()