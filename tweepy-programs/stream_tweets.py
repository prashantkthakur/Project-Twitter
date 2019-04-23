import json
import time
import tweepy
import sys
import os

class Listener(tweepy.StreamListener):
    """
    A listener handles tweets that are received from the stream.
    """
    def __init__(self, num_tweets, *args, **kwargs):
        self.connect = False
        self.tweet_cnt = 0
        self.tweet_limit = int(num_tweets)
        self.errors = {'connection_error': 0}
        self.outfile_name = "tweets"
        self.tweets_arr = list()
        super().__init__(*args, **kwargs)  # Include the inherited class constructor.

    def on_connect(self):
        self.connect = True

    def on_status(self, status):
        self.write_tweet(status._json)
 
    def on_error(self, status):
        raise Exception('Error received from tweeter.' + str(status))

    def write_tweet(self, tweet):
        # add tweet to list
        if self.tweet_cnt < self.tweet_limit:
            if tweet['lang']=="en":
                self.tweet_cnt += 1
                self.tweets_arr.append(tweet)
        # write output
        else:
            # find available filename
            counter = 0
            filename = self.outfile_name + str(counter) + '.json'
            while os.path.isfile(filename):
                counter += 1
                filename = self.outfile_name + str(counter) + '.json'

            # write file 
            with open(filename,'w') as fp:
                fp.write(json.dumps(self.tweets_arr))
                exit()

if __name__ == '__main__':
    try:
        # authenticate and setup api
        auth = tweepy.OAuthHandler('g83Pgpo62RNdGE4K74908vnkO', 'b7i2VnIgqazNdperwevjDUzONDVBJACEhbffEHYwh1OILAHQvI')
        auth.set_access_token('2377704086-Jf6k8y6KTy99qpvDIWZLpQFbm19ika3JrtZKF4q', 'I7T4H5H23MnS4SpXv5B2p5nUMHmaDQJ5fYxOmHCuuFmug')
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
       
        # stream the given number of tweets (default is 20) 
        if len(sys.argv) is 2:
            num_tweets_to_read = sys.argv[1]
        else:
            num_tweets_to_read = 20

        my_listner = Listener(num_tweets_to_read)
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


