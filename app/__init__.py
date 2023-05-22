from flask import Flask

from flask_login import LoginManager
import os
from datetime import timedelta
#from config import Config
#SESSION_TYPE = 'memcache'

app = Flask(__name__)
#app.config.from_object(Config)
app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.secret_key = os.urandom(24).hex()
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import routes


if __name__ == "__main__":
    app.run()
