import logging
import re
from datetime import timedelta

from django.utils.timezone import now

from games.models import Genre, SearchTerm, Game
from gt_igdb.django_client import get_client_from_settings

logger = logging.getLogger(__name__)


def get_or_create_genres(genre_names):
    for genre_name in genre_names:
        genre, created = Genre.objects.get_or_create(igdb_id=genre_name)
        yield genre


def fill_game_details(game):
    """
    Fetch a game's full details from igdb. Then, save it to the DB. If the game already has a `full_record` this does
    nothing, so it's safe to call with any `Game`.
    """
    if game.is_full_record:
        logger.warning(
            "'%s' is already a full record.",
            game.name,
        )
        return
    igdb_client = get_client_from_settings()
    game_details = igdb_client.get_by_id(game.id)
    game.name = game_details.name
    game.summary = game_details.summary
    game.url = game_details.url
    game.genres.clear()
    for genre in get_or_create_genres(game_details.genres):
        game.genres.add(genre)
    game.save()


def search_and_save(search):
    """
    Perform a search for search_term against the API, but only if it hasn't been searched in the past 24 hours. Save
    each result to the local DB as a partial record.
    """
    # Replace multiple spaces with single spaces, and lowercase the search
    normalized_search_term = re.sub(r"\s+", " ", search.lower())

    search_term, created = SearchTerm.objects.get_or_create(term=normalized_search_term)

    if not created and (search_term.last_search > now() - timedelta(days=1)):
        # Don't search as it has been searched recently
        logger.warning(
            "Search for '%s' was performed in the past 24 hours so not searching again.",
            normalized_search_term,
        )
        return

    igdb_client = get_client_from_settings()

    for igdb_game in igdb_client.search(search):
        logger.info("Saving game: '%s' / '%s'", igdb_game.name, igdb_game.id)
        game, created = Game.objects.get_or_create(
            id=igdb_game.id,
            defaults={
                "name": igdb_game.name,
                "summary": igdb_game.summary,
                "url": igdb_game.url,
                "genres": igdb_game.genres,
            },
        )

        if created:
            logger.info("Game created: '%s'", game.name)

    search_term.save()
