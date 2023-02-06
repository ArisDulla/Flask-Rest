from .graph import MethodsGraph
from .methodsMongoDb import MethodsCollection
from .factoryBackgroundThread import BackgroundThreadFactory

from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import os
import logging
import signal

logging.basicConfig(level=logging.INFO, force=True)

app = Flask(__name__)

mongoCollection = MethodsCollection()

graph = MethodsGraph()

graph.get_all_collections()

date = "%Y-%m-%dT%X"
#
# STREAMS MONGODB
#
# Background Thread
#
thread = BackgroundThreadFactory.create(graph)
# this condition is needed to prevent creating duplicated thread in Flask debug mode
if not (app.debug or os.environ.get('FLASK_ENV') == 'development') or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':

    for thread in thread:
        thread.start()

    original_handler = signal.getsignal(signal.SIGINT)


    def sigint_handler(signum, frame):
        thread.stop()

        # wait until thread is finished
        if thread.is_alive():
            thread.join()

        original_handler(signum, frame)


    try:
        signal.signal(signal.SIGINT, sigint_handler)
    except ValueError as e:
        logging.error(f'{e}. Continuing execution...')


#
# RECOMMEND ARTICLE
#
@app.route('/recommend', methods=['POST', 'GET'])
def recommend():
    id_rec = request.form.get("id")
    if not id_rec:
        return "msg Missing parameters"

    article = graph.getArticle()

    return article


#
# ADD NEW USER
#
@app.route('/add_new_user', methods=['POST', 'GET'])
def add_new_user():
    keyword = request.form.get("keyword")
    city = request.form.get("city")
    email = request.form.get("email")

    logging.info("REQUEST = /add_new_user  ,,  DATE TIME  = " + datetime.now().strftime(date))

    if not keyword or not city or not email:
        return "msg Missing parameters"

    else:
        msg = mongoCollection.join_in_table(keyword, city, email)

    return msg


#
# GET ARTICLES
#
@app.route('/get_article', methods=['GET'])
def get_articles():
    args = request.args
    keyword = args.get('keyword')

    logging.info("REQUEST = /get_article ,,  DATE TIME  = " + datetime.now().strftime(date))

    if not keyword:
        return "msg Missing keyword parameter"

    else:
        msg = mongoCollection.get_articles(keyword)

    return msg


#
# UPDATE PUT
#
@app.route('/make_update', methods=['PUT'])
def make_update():
    keyword = request.form.get("keyword")
    email = request.form.get("email")

    logging.info("REQUEST = /make_update ,,  DATE TIME  = " + datetime.now().strftime(date))

    if not keyword or not email:
        return "msg Missing keyword parameter"

    else:
        msg = mongoCollection.make_changes(email, keyword)

    return msg


#
# DELETE
#
@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    email = request.form.get("email")

    logging.info("REQUEST = /delete_user ,,  DATE TIME  = " + datetime.now().strftime(date))

    if not email:
        return "msg Missing keyword parameter"

    else:
        msg = mongoCollection.delete_user(email)

    return msg
