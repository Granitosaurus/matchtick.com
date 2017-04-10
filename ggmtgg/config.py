# WTF_CSRF_ENABLED = True
from ggmt.matchticker import GosuTicker
from ggmt.tournament import EVENT_PAST, EVENT_FUTURE, EVENT_CURRENT

SECRET_KEY = 'very-secret'
REDIS_URL = "redis://:@localhost:6379/0"

# rate limiting
RATELIMIT_STORAGE_URL = "redis://:@localhost:6379/0"
RATELIMIT_HEADERS_ENABLED = True

# ggmt settings
GAMES = {
    'Dota 2': 'dota2',
    'CS:GO': 'counterstrike',
    'Hearthstone': 'hearthstone',
    'Heroes of the Storm': 'heroesofthestorm',
    'League of Legends': 'lol',
    'Overwatch': 'overwatch',
    'Starcraft 2': 'starcraft2',
    'All': 'all',
}
TOURNAMENT_TIMES = [t.lower() for t in [EVENT_PAST, EVENT_FUTURE, EVENT_CURRENT]]
