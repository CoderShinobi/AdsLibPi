import sys
#sys.path.append('/opt/homebrew/lib/python2.7/site-packages') # Replace this with the place you installed facebookads using pip
#sys.path.append('/opt/homebrew/lib/python2.7/site-packages/facebook_business-3.0.0-py2.7.egg-info') # same as above

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

my_app_id = '1077998460788718'
my_app_secret = '8cfc023c3d0df8b906abf949a8698512'
my_access_token = 'EAAPUbxNS3ZB4BO2P0NCaAYgDVsnuhW5lfw5Kbg9zqcA9uAxmnuZCZCZCdglvdZBZAueVqgpZBlmI0ziR5LeoItUWnbVezQ6XJAU8cSuHY4msZA0Xu6jGaQmCgXPF5LyfZAI5TVr8sXRbqZCY536SxSSqIZBVj2kWAYEyaAYlXF7TDemtTrn5FujuOIqvTZA1heLZBJn0rPm0FFeWo';
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token);
try:
    my_account = AdAccount('act_1982957785521633')
    campaigns = my_account.create_campaign( );

    if not campaigns:
        print("No campaigns found.")
    else:
        print(campaigns)
except Exception as e:
    print(f"An error occurred: {e}")