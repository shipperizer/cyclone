from datetime import timedelta, datetime

from flask import current_app
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError


db = SQLAlchemy()


def db_commit():
    try:
        db.session.commit()
    except IntegrityError as e:
        current_app.logger.error(e)
        raise


class Page(db.Model):
    __tablename__ = 'page'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250), nullable=False)
    words = db.relationship('Word', backref='page')
    last_modified = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def is_old(self, time):
        if self.last_modified < time - timedelta(days=1):
            return True
        return False


class Word(db.Model):
    __tablename__ = 'word'

    id = db.Column(db.String(250), primary_key=True)
    hash = db.Column(db.Text, nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), primary_key=True)
    db.PrimaryKeyConstraint('id', 'page_id', name='word_pk')
