import logging

from .methodsMongoDb import MethodsCollection
from datetime import datetime, timedelta
from flask import Flask, request, abort

app = Flask(__name__)

mongoCollection = MethodsCollection()

date = "%Y-%m-%dT%X"


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
