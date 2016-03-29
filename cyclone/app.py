import os
from logging import StreamHandler

from Crypto.PublicKey import RSA
from Crypto import Random
from flask.ext.migrate import Migrate
from flask import Flask
from sqlalchemy.exc import IntegrityError

from cyclone.db import db
from cyclone.api import api


def init_config(app):
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASS = os.environ.get('DB_PASS', '')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', 3306)
    DB_NAME = os.environ.get('DB_NAME', 'cyclone')
    # used for AES, must be 16 chars long
    SECRET_KEY = os.environ.get('SECRET_KEY', '540yaxc122lusQXW')
    DEBUG = os.environ.get('DEBUG') is not None
    app.config['DEBUG'] = DEBUG
    app.config['PROPAGATE_EXCEPTIONS'] = True

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://%s:%s@%s:%s/%s' % (
        DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
    )
    app.secret_key = SECRET_KEY
    app.logger.addHandler(StreamHandler())
    app.rsa_key = RSA.generate(8192, Random.new().read)


def create_app():
    app = Flask(__name__)
    init_config(app)
    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(api)

    @app.errorhandler(IntegrityError)
    def handle_invalid_usage(error):
        return 'Internal Error', 500

    return app
