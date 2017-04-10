from flask import Flask
from flask_redis import FlaskRedis
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config.from_pyfile('config.py')
redis = FlaskRedis(app, decode_responses=True)
limiter = Limiter(app, key_func=get_remote_address)



import ggmtgg.views
import ggmtgg.updater
