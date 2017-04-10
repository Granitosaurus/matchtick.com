import json

from ggmt.matchticker import GosuTicker
from ggmt.tournament import LiquidBracketDownloader, EVENT_CURRENT, EVENT_FUTURE, EVENT_PAST
from redis import Redis

from ggmtgg import app


@app.cli.command('update-matchticker')
def update_matchticker():
    r = Redis()
    for game in GosuTicker.games:
        print(f'updating matchticker {game}')
        g = GosuTicker(game)
        value = list(g.download_matches())
        r.delete(f'ggmt_tick_{game}')
        r.set(f'ggmt_tick_{game}', json.dumps(value))


@app.cli.command('update-tournaments')
def update_tournaments():
    r = Redis()
    for cat in [EVENT_FUTURE, EVENT_CURRENT, EVENT_PAST]:
        for game in LiquidBracketDownloader.games:
            print(f'updating tournament {game}_{cat.lower()}')
            dl = LiquidBracketDownloader(game)
            value = dl.find_tournaments(cat)
            r.delete(f'ggmt_tournament_{game}_{cat.lower()}')
            r.set(f'ggmt_tournament_{game}_{cat.lower()}', json.dumps(value))


if __name__ == '__main__':
    update_tournaments()
    update_matchticker()
