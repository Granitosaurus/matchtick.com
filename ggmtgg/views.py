import json

from flask import render_template, request, redirect, url_for, g, session, abort
from jinja2 import TemplateNotFound

from ggmtgg import app, redis, config, limiter
from ggmt.tournament import LiquidBracketDownloader
from ggmt.matchticker import GosuTicker


def error(reason, suggestion=None):
    data = {
        'error': reason,
        'suggestion': suggestion or ''
    }
    return json.dumps(data)


api_limit = limiter.shared_limit("100/hour", "api", error_message=error('Exceeded 100/hour api call limit'))


@app.before_first_request
def make_session_permanent():
    session.permanent = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tick/<string:game>')
def tick(game):
    data = redis.get(f'ggmt_tick_{game}')
    data = json.loads(data)
    return render_template('tick.html', data=data)


@app.route('/api/tick/<string:game>')
@api_limit
def api_tick(game):
    if game not in GosuTicker.games:
        return error(f'unknown_game;choose from: {GosuTicker.games}')
    return redis.get(f'ggmt_tick_{game}')


@app.route('/api/tournament/<string:game>/<string:time>')
@app.route('/api/tournament/<string:game>', defaults={'time': 'all'})
@app.route('/api/tournament', defaults={'time': None, 'game': None})
@api_limit
def api_tournament(game, time):
    if game not in LiquidBracketDownloader.games:
        return error(f'unknown_game;choose from: {LiquidBracketDownloader.games}',
                     suggestion='/tournament/game')
    times = config.TOURNAMENT_TIMES + ['all']
    if time not in times:
        return error(f'unknown_time;choose from: {times}')
    if time != 'all':
        return redis.get(f'ggmt_tournament_{game}_{time}')
    else:
        items = [json.loads(redis.get(f'ggmt_tournament_{game}_{i}')) for i in config.TOURNAMENT_TIMES]
        items = [tour for time in items for tour in time]
        return json.dumps(items, ensure_ascii=False)


@app.route('/<string:page_name>')
def static_page(page_name):
    try:
        return render_template('{}.html'.format(page_name))
    except TemplateNotFound:
        return abort(404)
