import os
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

def check_credentials():
    # First verify the config file exists
    if not os.path.exists("google_ads.yaml"):
        print("Error: google_ads.yaml file not found")
        return False
        
    try:
        # Initialize the Google Ads client
        client = GoogleAdsClient.load_from_storage(version="v18")
        
        # Verify client configuration
        if not client.login_customer_id:
            print("Error: login_customer_id not set in google_ads.yaml")
            return False

        # Get the CustomerService
        customer_service = client.get_service("CustomerService")

        # Make a simple API call to list accessible customers
        accessible_customers = customer_service.list_accessible_customers()

        result_total = len(accessible_customers.resource_names)
        print(f"Total results: {result_total}")

        print("Credentials are valid. Accessible customers:")
        for resource_name in accessible_customers.resource_names:
            print(resource_name)
        return True

    except GoogleAdsException as ex:
        print(f"Google Ads API Error:")
        print(f"Code: {ex.error.code().name}")
        print(f"Message: {ex.error.message}")
        print(f"Request ID: {ex.request_id}")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    check_credentials()