import argparse
import json
import multiprocessing
import sys
import time

import pymongo
import tweepy
from bson.dbref import DBRef
from fetch_tweets.pylib import logger

import database


def load_credentials_file(credentialsFile):
    try:
        with open(credentialsFile, 'r') as inFile:
            credentials = json.load(inFile)
            if len(credentials) < 1:
                log.error("Error: credentials file {} must contain at least one set of credentials!".format(credentialsFile))
                exit(-1)
            else:
                for credential in credentials:
                    if 'CONSUMER_KEY' not in credential or 'CONSUMER_SECRET' not in credential:
                        log.error("Error: malformed credential file %s!" % credentialsFile)
                        exit(-1)
    except IOError as e:
        print("Error while opening credentials file: {}".format(str(e)))
        exit(-1)
    return credentials


def remaining_requests(api):
    return api.rate_limit_status()


def scraping_thread(dburi, dbname, credentials, queue):
    # Create MongoDB connection
    print("Scraping thread...queue={}".format(queue))
    db_info = dburi.split(':')
    db_store = database.get_db(dbname, db_info[0], int(db_info[1]))
    # dbclient = pymongo.MongoClient('mongodb://%s/' % dburi)
    # tweeter_collection = dbclient[dbname][dbcollection]
    # user_collection = dbclient[dbname][USERDB]
    # Authenticate with Twitter API
    auth = tweepy.AppAuthHandler(credentials.get("CONSUMER_KEY"), credentials.get("CONSUMER_SECRET"))
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # request_limit = remaining_requests(api)

    while True:
        #requested_tmline = 0
        # TO-DO : Stop scrapping when there is no requests left for the tweeter.
        # rqst_rate_lmt = request_limit['resources']['application']['/application/rate_limit_status']['remaining']
        # rqst_refresh_time = request_limit['resources']['application']['/application/rate_limit_status']['reset']
        # tmline_lmt = request_limit['resources']['statuses']['/statuses/user_timeline']['remaining']
        # tmline_refresh_time = request_limit['resources']['statuses']['/statuses/user_timeline']['reset']
        # log.debug("Request rate limit/refresh time = {}/{}; User timeline limit/refresh time= {}/{} ".format(
        #     rqst_rate_lmt,rqst_refresh_time,tmline_lmt,tmline_refresh_time))
        # if requested_tmline >= tmline_lmt and time.time() < tmline_refresh_time:
        #     stime = tmline_refresh_time - time.time()+5
        #     log.warning("Sleeping for {}".format(stime))
        #     time.sleep(stime)  # Sleep for extra 5 seconds.
        #     # Might not need request check.
        #     if rqst_rate_lmt > 0 or time.time() > rqst_refresh_time:
        #         request_limit = remaining_requests(api)
        #     else:
        #         time.sleep(rqst_refresh_time - time.time())  # Sleep till request status is available.
        #         request_limit = remaining_requests(api)
        # else:
        uid = queue.get()
        log.warning("Extracted from queue. uid={}".format(uid))
        if uid == -1:
            queue.task_done()
            raise Exception("-1 added in queue.")
            # break
        tweets = tweepy.Cursor(api.user_timeline, user_id=uid, count=200).items()
        # requested_tmline += 1
        while True:
            try:
                tweet = tweets.next()
                update_db(tweet._json, db_store)
            except StopIteration:
                log.error("StopIteration encountered.")
                break
            except tweepy.error.TweepError as e:
                log.exception("TweepError encountered. Status Code={}".format(e.response.status_code))
                # Store user ID which has protected tweets and can't attach to their timeline.
                if uid != -1:
                    db_store.failed_users.insert_one({'uid': uid, 'status_code': e.response.status_code})
                break
            # request_limit = remaining_requests(api)
        queue.task_done()


def update_db(tweet,db):
    try:
        usr = tweet['user']
        if not db.users.find_one({'id_str': usr['id_str']}):
            usr_id = db.users.insert(usr)
            tweet['user'] = DBRef('users', usr_id, db.name)
            try:
                tweet_id = db.tweets.insert_one(tweet)
                log.debug('Adding User Id : %s Tweet Id : %s', usr_id, tweet_id.inserted_id)

            # Handle the exception if the duplicate tweets are seen.
            except pymongo.errors.DuplicateKeyError:
                pass

        else:
            usr_id = db.users.find_one({'id_str': usr['id_str']}, {'_id': 1})['_id']
            tweet['user'] = DBRef('users', usr_id, db.name)
            try:
                tweet_id = db.tweets.insert_one(tweet)
                log.debug('Update User Id : %s Tweet Id : %s', usr_id, tweet_id.inserted_id)

            # Handle the exception if the duplicate tweets are seen.
            except pymongo.errors.DuplicateKeyError:
                pass
    except Exception as e:
        log.exception("Error operating to the DB. Error={}".format(str(e)))


def index_db(mongouri, dbname):
    db_info = mongouri.split(':')
    db_store = database.get_db(dbname, db_info[0], int(db_info[1]))
    # Create index so that tweets are unique and users are searchable with given index.
    db_store.tweets.create_index('id_str', unique=True)
    db_store.users.create_index('id_str', unique=True)


def update_queue(db_usr,q,num_threads):
    try:
        cursor = db_usr.users.find({},{'id_str': 1, '_id': 0}, no_cursor_timeout=True)
        for usr in cursor.batch_size(60):
            uid = usr['id_str']
            log.warning("Adding user id in queue. uid={}".format(uid))
            q.put(uid)
    except Exception as e:
        log.exception("Error adding user id to queue. Exception:{}".format(str(e)))

    finally:
        for _ in range(num_threads):
            q.put(-1)
        cursor.close()


def history_scrap():
    try:
        argparser = argparse.ArgumentParser(description="Scrape tweets of a random set of Twitter users")
        argparser.add_argument('-c', '--credentials-file',
                               help='JSON file with credentials information',
                               action='store', default='credentials.json')
        argparser.add_argument('-t', '--num-threads', type=int,
                               help='Maximum number of threads to create (default: 8)',
                               action='store', default=8)
        argparser.add_argument('-m', '--mongodb-uri',
                               help='URI of MongoDB instance (default: localhost:27017',
                               action='store', default='localhost:27017')
        argparser.add_argument('-d', '--database',
                               help='Name of MongoDB database for tweet storage (default: history)',
                               action='store', default='history')
        # argparser.add_argument('-o', '--collection',
        #                        help='Name of database collection for tweet storage (default: tweets)',
        #                        action='store', default='tweets')
        argparser.add_argument('-n', '--num-users', type=int,
                               help='Number of users to scrape (default: 1)',
                               action='store', default=1)
        args = argparser.parse_args()
        credentials = load_credentials_file(args.credentials_file)

        num_threads = min(len(credentials), args.num_threads)
        q = multiprocessing.JoinableQueue(100)
        index_db(args.mongodb_uri,args.database)
        # q = queue.Queue()
        threads = [multiprocessing.Process(target=scraping_thread,
                                           args=(args.mongodb_uri, args.database, credentials[i], q))
                   for i in range(num_threads)]
        for t in threads:
            t.start()
        log.warning("%s -- Threads started" % time.strftime('%l:%M%p %Z on %b %d, %Y'))
        while True:
            try:
                db_usr = database.get_db('research', 'localhost', 27777)
                update_queue(db_usr, q, num_threads)
            except:
                log.exception("Breaking out of queue update loop")
                raise UserWarning("Error updating queue")
        q.join()
        for t in threads:
            t.join()
        log.warning("%s -- All done!", time.strftime('%l:%M%p %Z on %b %d, %Y'))
    except Exception as e:
        log.exception("Exception in history_scrapper: {}".format(str(e)))
        q.join()
        for t in threads:
            t.join()
        sys.exit(1)


if __name__ == '__main__':
    log = logger.set_logger('info', 'history_scraper')
    history_scrap()
