"""
Nov 6 2017
streaming.py method was changed to handle Attribute Error.
line = buf.read_line().strip() complained when there is no line read from the buffer. try catch added to handle.

"""
import json
import time
from time import gmtime, strftime

import tweepy
from fetch_tweets.pylib import logger

import database

# Twitter application authentication info
access_token = "919589727753216007-nRN64Q10pctwl1getZSd3thOSLyx8Wt"
access_token_secret = "qiUgYOZ1LdMoiwNzRS78MdCKYCW97amgzp0wvCFI3vgkB"
consumer_key = "KEQt2LvIwFvfpngI9kYCazRwP"
consumer_secret = "pkVbufXuOI4paWdYVb4HPwqYJ0EPFwLagL21sGwllLPtQVqYJ7"

# Database info
tweet_db, tweet_db_host, tweet_db_port = ('log','localhost',27017)


class Listener(tweepy.StreamListener):
    """
    A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, *args, **kwargs):
        self.connect = False
        self.tweet_cnt = 0
        self.errors = {'connection_error': 0}
        self.db = database.get_db(tweet_db, tweet_db_host, tweet_db_port)
        super().__init__(*args, **kwargs)  # Include the inherited class constructor.

    def on_connect(self):
        self.connect = True

    def on_status(self, status):
        self.tweet_cnt += 1
        self.update_db(status._json)
        # return True

    def on_error(self, status):
        log.exception(status)
        raise Exception('Error received from tweeter.')

    def update_db(self, tweet):
        #try:
        db = self.db
        if tweet['lang']=="en":
            tweet['source'] = tweet['source'].replace("\"","'")
            with open("sdata.csv",'a') as fp:
                fp.write("{},{},{}\n".format(strftime("%Y-%m-%d %H:%M:%S", gmtime()),tweet["user"]["screen_name"],json.dumps(tweet["text"].replace("\"","\'"))))
            #usr = tweet['user']
            #if not db.users.find_one({'id': usr['id']}):
                #usr_id = db.users.insert(usr)
                #tweet['user'] = DBRef('users', usr_id, db.name)
                #tweet_id = db.tweets.insert(tweet)
                # if self.tweet_cnt % 1000 == 0:
                #log.warning('{} Adding User Id : {} Tweet Id : {}'.format(self.tweet_cnt,usr_id, tweet_id))
            #else:
                #usr_id = db.users.find_one({'id': usr['id']}, {'_id': 1})
                #tweet['user'] = DBRef('users', usr_id, db.name)
                #tweet_id = db.tweets.insert(tweet)
                # if self.tweet_cnt % 1000 == 0:
                #log.warning('{} Existing User Id : {} Tweet Id: {}'.format(self.tweet_cnt,usr_id, tweet_id))
        #except Exception as e:
         #   raise Exception("DBError:{}".format(str(e)))


if __name__ == '__main__':
    try:
        log = logger.set_logger('debug', 'streamer')
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        # api = tweepy.API(auth)
        my_listner = Listener()
        streamer = tweepy.Stream(auth, listener=my_listner, timeout=30000)
        streamer.sample()
    except KeyboardInterrupt:
        log.error("Received KeyboardInterrupt.")
        streamer.disconnect()  # Disconnect streamer if there is keyboard interrupt or any other error.
    except ConnectionResetError:
        my_listner.errors['connection_error'] += 1  # backoff if error is frequent
        log.error("Received ConnectionResetError.")
        streamer.disconnect()
        time.sleep(60*my_listner.errors['connection_error'])
        streamer.sample()
    except AttributeError:
        log.error("AttributeError. Starting the sampling")
        streamer.disconnect()
        time.sleep(10)
        streamer.sample()
    except Exception as e:
        log.exception(str(e))
        streamer.disconnect()

