import json

from flask import render_template, request, redirect, url_for, g, session, abort

from ggmtgg import app, redis, config


@app.before_first_request
def make_session_permanent():
    session.permanent = True


@app.route('/')
def index():
    return json.dumps({'foo': 'bar'})


@app.route('/tick/<string:game>')
def post(game):
    if game not in config.GAMES:
        return json.dumps({'error': f'unknown_game;choose from:{config.GAMES}'})
    return json.dumps(redis.hgetall(f'ggmt_tick_{game}'), ensure_ascii=False)


