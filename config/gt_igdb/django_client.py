from django.conf import settings

from gt_igdb.client import IgdbClient


def get_client_from_settings():
    """Create an instance of an IgdbClient using the IGDB_KEY from the Django settings."""
    return IgdbClient(settings.IGDB_KEY)
