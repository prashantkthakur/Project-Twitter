import logging
import time
import pymongo

db_name = "research"
db_username = "csu"
db_password = "re$earch-c$u"


def get_db(dbname, machine='localhost', port=27017,conn=None, username=None, password=None ):
    if conn is None:
        conn = pymongo.MongoClient(machine,port,connect=False)
    db = conn[dbname]
    if username:
        db.authenticate(username, password)
    return db


def get_research(conn=None):
    """ authenticate the mongo makalu DB
        with username and password
    """
    return get_db(db_name, conn, db_username, db_password)


def wait_and_get_db(app):
    """
    """
    while True:
        try:
            db = get_research()
            return db
        except pymongo.errors.AutoReconnect:
            logging.warning("%s; waiting for mongodb" % app)
            time.sleep(10)


def add_user(admin, db_name, username, password):
    logging.info("Adding user '%s' in db '%s'.", username, db_name)
    # admin is allowed to access all database
    db = admin.connection[db_name]
    db.remove_user(username)
    db.add_user(username, password)
    return db


def main():
    """insert the mongo db users
        for security and further authentication.
    """
    db = get_db(db_name)
    add_user(db, db_name, db_username, db_password)
