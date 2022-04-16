import logging

import requests

logger = logging.getLogger(__name__)

IGDB_API_URL = "https://api.igdb.com/v4/games"


class IgdbGame:
    """A simple class to represent game data coming back from Igdb and transform to Python types."""

    def __init__(self, data):
        """Data is the raw JSON/dict returned from OMDb"""
        self.data = data

    def check_for_detail_data_key(self, key):
        """Some keys are only in the detail response, raise an exception if the key is not found."""
        if key not in self.data:
            raise AttributeError(
                f"{key} is not in data, please make sure this is a detail response."
            )

    @property
    def igdb_id(self):
        return self.data["id"]

    @property
    def name(self):
        return self.data["name"]

    @property
    def summary(self):
        return self.data["summary"]

    @property
    def url(self):
        return self.data["url"]


    @property
    def genres(self):
        self.check_for_detail_data_key("Genre")

        return self.data["Genre"].split(", ")


class IgdbClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def make_request(self, params):
        """Make a GET request to the API, automatically adding the `apikey` to parameters."""
        params["apikey"] = self.api_key

        resp = requests.get(IGDB_API_URL, params=params)
        resp.raise_for_status()
        return resp

    def get_by_igdb_id(self, igdb_id):
        """Get a game by its IGDB ID"""
        logger.info("Fetching detail for IGDB ID %s", igdb_id)
        resp = self.make_request({"i": igdb_id})
        return IgdbGame(resp.json())

    def search(self, search):
        """Search for games by name/title. This is a generator so all results from all pages will be iterated across."""
        page = 1
        seen_results = 0
        total_results = None

        logger.info("Performing a search for '%s'", search)

        while True:
            logger.info("Fetching page %d", page)
            resp = self.make_request({"s": search, "type": "game", "page": str(page)})
            resp_body = resp.json()
            if total_results is None:
                total_results = int(resp_body["totalResults"])

            for game in resp_body["Search"]:
                seen_results += 1
                yield IgdbGame(game)

            if seen_results >= total_results:
                break

            page += 1
