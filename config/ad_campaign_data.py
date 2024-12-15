class AdCampaign:
    def __init__(self, campaign_id, campaign_name,status, start_time, stop_time, created_time, updated_time):
        self.campaign_id = campaign_id
        self.campaign_name = campaign_name
        self.status = status
        self.start_time = start_time
        self.stop_time = stop_time
        self.created_time = created_time
        self.updated_time = updated_time

    def __repr__(self):
        return f"AdCampaign({self.campaign_id}, {self.campaign_name}, {self.start_time}, {self.stop_time}, {self.created_time}, {self.updated_time})"

class MetaCampaign(AdCampaign):
    def __init__(self, campaign_id, campaign_name, objective, status, special_ad_categories,special_ad_categories_country, date_preset=None, time_range=None, daily_budget=None, lifetime_budget=None, bid_strategy=None, start_time=None, stop_time=None, created_time=None, updated_time=None, buying_type="AUCTION"):
        super().__init__(campaign_id, campaign_name,status, start_time, stop_time, created_time, updated_time)
        self.objective = objective
        self.special_ad_categories = special_ad_categories
        self.special_ad_categories_country = special_ad_categories_country
        self.date_preset = date_preset
        self.time_range = time_range
        self.daily_budget = daily_budget
        self.lifetime_budget = lifetime_budget
        self.bid_strategy = bid_strategy
        self.buying_type = buying_type

    def __repr__(self):
        base_repr = super().__repr__()
        return f"{base_repr}, MetaCampaign({self.objective}, {self.status}, {self.special_ad_categories}, {self.date_preset}, {self.time_range}, {self.daily_budget}, {self.lifetime_budget}, {self.bid_strategy}, {self.buying_type}, {self.budget_rebalance_flag})"

class GoogleAdsCampaign(AdCampaign):
    def __init__(self, campaign_id, campaign_name,status, campaign_type, networks, locations, languages, bidding_strategy, budget,devices= None, ad_assets=None, additional_settings=None, start_time=None, stop_time=None, created_time=None, updated_time=None):
        super().__init__(campaign_id, campaign_name,status, start_time, stop_time, created_time, updated_time)
        self.campaign_type = campaign_type
        self.networks = networks
        self.devices = devices
        self.locations = locations
        self.languages = languages
        self.bidding_strategy = bidding_strategy
        self.budget = budget
        self.ad_assets = ad_assets if ad_assets is not None else []
        self.additional_settings = additional_settings if additional_settings is not None else {}

    def __repr__(self):
        base_repr = super().__repr__()
        return f"{base_repr}, GoogleAdsCampaign({self.campaign_type}, {self.networks}, {self.devices}, {self.locations}, {self.languages}, {self.bidding_strategy}, {self.budget}, {self.ad_assets}, {self.additional_settings})"

# Example usage
meta_campaign = MetaCampaign(
    campaign_id="123456789",
    campaign_name="My Meta Campaign",
    objective="OUTCOME_TRAFFIC",
    status="PAUSED",
    special_ad_categories=["NONE"],
    special_ad_categories_country=["IN"],
    date_preset="last_30d",
    time_range={'since': '2024-01-01', 'until': '2024-01-31'},
    daily_budget=1000,
    lifetime_budget=10000,
    bid_strategy="LOWEST_COST_WITHOUT_CAP",
    start_time="2024-01-01T00:00:00",
    stop_time="2024-12-31T23:59:59",
    created_time="2023-01-01T00:00:00",
    updated_time="2023-12-01T00:00:00",
    buying_type="AUCTION"
)

google_campaign = GoogleAdsCampaign(
    campaign_id="987654321",
    campaign_name="My Google Ads Campaign",
    status="PAUSED",
    campaign_type="Search Network",
    networks=["Google Search Network", "Search Partners"],
    devices=["Desktops", "Tablets", "Mobile Devices"],
    locations=["United States", "Canada"],
    languages=["English"],
    bidding_strategy="Manual CPC",
    budget=5000,
    ad_assets=["Location Information", "Links to Pages", "Phone Number"],
    additional_settings={
        "schedule": {"start_date": "2024-01-01", "end_date": "2024-12-31"},
        "ad_scheduling": {"days": ["Monday", "Tuesday"], "hours": ["9:00 AM - 5:00 PM"]},
        "ad_delivery": "Standard"
    },
    start_time="2024-01-01T00:00:00",
    stop_time="2024-12-31T23:59:59",
    created_time="2023-01-01T00:00:00",
    updated_time="2023-12-01T00:00:00"
)

print(google_campaign)