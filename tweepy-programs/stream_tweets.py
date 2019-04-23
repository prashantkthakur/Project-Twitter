import json
import time
from time import strftime, gmtime
import tweepy

class Listener(tweepy.StreamListener):
    """
    A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, *args, **kwargs):
        self.connect = False
        self.tweet_cnt = 0
        self.errors = {'connection_error': 0}
        super().__init__(*args, **kwargs)  # Include the inherited class constructor.

    def on_connect(self):
        self.connect = True

    def on_status(self, status):
        self.tweet_cnt += 1
        self.update_db(status._json)

    def on_error(self, status):
        raise Exception('Error received from tweeter.' + str(status))

    def update_db(self, tweet):
        if tweet['lang']=="en":
            tweet['source'] = tweet['source'].replace("\"","'")
            with open("sdata.csv",'a') as fp:
                fp.write("{},{},{}\n".format(strftime("%Y-%m-%d %H:%M:%S", gmtime()),tweet["user"]["screen_name"],json.dumps(tweet["text"].replace("\"","\'"))))

if __name__ == '__main__':
    try:
        # authenticate and setup api
        auth = tweepy.OAuthHandler('g83Pgpo62RNdGE4K74908vnkO', 'b7i2VnIgqazNdperwevjDUzONDVBJACEhbffEHYwh1OILAHQvI')
        auth.set_access_token('2377704086-Jf6k8y6KTy99qpvDIWZLpQFbm19ika3JrtZKF4q', 'I7T4H5H23MnS4SpXv5B2p5nUMHmaDQJ5fYxOmHCuuFmug')
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        my_listner = Listener()
        streamer = tweepy.Stream(auth, listener=my_listner, timeout=30000)
        streamer.sample()
        print('streamed')
    except KeyboardInterrupt:
        print('keyboard interrupt')
        streamer.disconnect()  # Disconnect streamer if there is keyboard interrupt or any other error.
    except ConnectionResetError:
        streamer.disconnect()
        print('connection reset')
        time.sleep(60*my_listner.errors['connection_error'])
        streamer.sample()
    except AttributeError:
        streamer.disconnect()       
        print('attr error')
        time.sleep(10)
        streamer.sample()
    except Exception as e:
        print(e)
        streamer.disconnect()


