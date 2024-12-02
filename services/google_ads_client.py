# services/google_ads_client.py
from google.ads.googleads.client import GoogleAdsClient

def get_google_ads_client():
    client = GoogleAdsClient.load_from_storage(version="v18")
    client.login_customer_id = "1381653354"
    return client