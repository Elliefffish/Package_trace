from ..configs.platform_config import platform_to_id
from .db import Database
from .parcel_table import ParcelTable
from .platform_table import PlatformTable
from .subscription_table import SubscriptionTable


def init_db():
    with Database() as db:
        platform_table = PlatformTable(db)
        platform_table.create_table()
        # Insert platform data
        for platform in platform_to_id.keys():
            platform_table.insert(platform)
        ParcelTable(db).create_table()
        SubscriptionTable(db).create_table()
