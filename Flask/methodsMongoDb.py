import logging

from Flask.client import ClientMongo
from datetime import datetime


class MethodsCollection:

    def __init__(self):
        self.client = ClientMongo()

    # -------------------------------
    # CREATE NEW USER
    #
    def join_in_table(self, keywords, city, email):
        client = self.client
        client = client.mongoClient
        db = client["Collections"]
        collection = db["users"]

        print(db)
        new_user = {"info": {"_id": email, "keyword": keywords, "city": city,
                             "timestamp": datetime.now().strftime("%Y-%m-%dT%X")}}

        info = new_user["info"]

        try:

            collection.insert_one(info)
            logging.info("The user added successfully" + str(info))
            return "The user added successfully"

        except Exception as a:
            logging.warning("Exception" + str(a))
            return "An exception occurred " + str(a)

    # -------------------------------
    # GET ARTICLE
    #
    def get_articles(self, key):
        client = self.client
        client = client.mongoClient
        db = client["Collections"]
        wiki = db["wiki"]

        query = {"title": key}

        try:

            result = wiki.find(query)
            logging.info("find query + " + str(query))

        except Exception as a:
            logging.warning("Exception" + str(a))
            return "An exception occurred " + str(a)

        for i in result:
            if i['extract'] != "":
                logging.info("This article have context ")
                return i['extract']

        logging.info("This article does not exist ")
        return '''<p> This article does not exist </p>'''

    # ------------------------------
    # UPDATE INFO USER
    #
    def make_changes(self, email, keyword):
        client = self.client
        client = client.mongoClient
        db = client["Collections"]
        collection = db["users"]

        query = {"_id": email}
        new_value = {"$set": {"keyword": keyword}}

        try:
            result = collection.update_one(query, new_value)

        except Exception as a:
            logging.warning("Exception" + str(a))
            return "An exception occurred " + str(a)

        if result.matched_count != 0:
            logging.info("Ηas been successfully updated " + str(query))
            return "Ηas been successfully updated  "

        else:
            logging.info("NOT EXIST ID" + str(query))
            return "NOT EXIST ID = " + email

    # -----------------------------
    # DELETE USER
    #
    def delete_user(self, email):
        client = self.client
        client = client.mongoClient
        db = client["Collections"]
        collection = db["users"]

        query = {"_id": email}

        try:
            result = collection.delete_one(query)

        except Exception as a:
            logging.warning("Exception" + str(a))
            return "An exception occurred " + str(a)

        if result.deleted_count != 0:
            logging.info("The user has been deleted successfully" + str(query))
            return "The user has been deleted successfully "
        else:
            logging.info("NOT EXIST ID = " + str(query))
            return "NOT EXIST ID = " + email
