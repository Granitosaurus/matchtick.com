from ggmt.matchticker import GosuTicker
from redis import Redis


def update_matchticker():
    r = Redis()
    for game in GosuTicker.games:
        print(f'updating {game}')
        g = GosuTicker(game)
        value = list(g.download_matches())
        r.delete(f'ggmt_tick_{game}')
        r.hmset(f'ggmt_tick_{game}', {'data': value})


if __name__ == '__main__':
    update_matchticker()
