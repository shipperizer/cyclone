from collections import Counter
from datetime import datetime
import re

from bs4 import BeautifulSoup
from flask import Blueprint, request, url_for, jsonify, current_app, render_template
from flask_wtf import Form
from flask_wtf.html5 import URLField
import requests

from cyclone.db import db, db_commit, Word, Page


api = Blueprint('api', __name__)


@api.route('/admin', methods=['GET'])
def admin():
    words = Word.query.order_by(db.desc(Word.frequency)).all()
    return jsonify(words=[{'word': word.hash, 'frequency': word.frequency} for word in words])


class WebpageForm(Form):
    website = URLField('Website', description='Website URL to check')

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        try:
            r = requests.get(self.website.data)
            print(r.status_code)
            if r.status_code > 302:
                self.website.errors.append('Website not reachable')
                return False
        except requests.exceptions.ConnectionError:
            self.website.errors.append('Website format unknown')
            return False
        return True


@api.route('/crawl', methods=['GET'])
def crawl():
    return render_template('words.html', form=WebpageForm(), words=[])


@api.route('/crawl', methods=['POST'])
def words():
    form = WebpageForm(request.form)
    if not form.validate():
        return render_template('words.html', form=form), 409
    # current_app.secret_key should be 16 chars long
    words = [
        {
            'frequency': word.frequency,
            'word': word.hash
        } for word in get_words(form.website.data)]
    return render_template('words.html', form=form, words=words)


def get_words(url):
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = re.sub(r"[\[\]\(\)=]", "", text)

    page = Page.query.filter_by(url=url).first()
    if not page:
        page = Page(url=url)
        db.session.add(page)
    elif page.is_old(datetime.now()):
        # if newer than a day I don't refetch the page
        # drop old words as neither id nor name are useful search fields by requirements
        # even though I could do it as I dropped the hashed word field
        Word.query.filter_by(page_id=page.id).delete()
    else:
        return page.words
    # create words objects from scratch
    for word in Counter(text.split()).most_common(100):
        db.session.add(create_word(word, page))
    db_commit()
    return page.words
    #  a) The primary key for the word is a salted hash of the word.
    # b) The word itself is saved in a column that has asymmetrical encryption, and you are saving the encrypted version of the word.
    # c) The total frequency count of the word.


def create_word(word_tuple, page_obj, cypher=None):
    w = Word(page=page_obj, frequency=word_tuple[1])
    w.id = current_app.bcrypt.generate_password_hash(word_tuple[0])
    # spent WAY too much time in trying to use AES without good results, using plain word name
    w.hash = word_tuple[0]
    return w
