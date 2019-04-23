import json
import time
import tweepy
import sys
import os

class Listener(tweepy.StreamListener):
    """
    A listener handles tweets that are received from the stream.
    """
    def __init__(self, num_tweets, tweet_id_to_watch, *args, **kwargs):
        self.connect = False
        self.tweet_cnt = 0
        self.tweet_limit = int(num_tweets)
        self.errors = {'connection_error': 0}
        self.outfile_name = "tweets"
        self.tweets_arr = list()
        self.tweet_id_to_watch = tweet_id_to_watch
        super().__init__(*args, **kwargs)  # Include the inherited class constructor.

    def on_connect(self):
        self.connect = True

    def on_status(self, status):
        self.write_tweet(status._json)
 
    def on_error(self, status):
        raise Exception('Error received from tweeter.' + str(status))

    def find_available_filename(self, outfile_name):
            counter = 0
            filename = self.tweet_id_to_watch + outfile_name + str(counter) + '.json'
            while os.path.isfile(filename):
                counter += 1
                filename = self.tweet_id_to_watch + outfile_name + str(counter) + '.json'
            return filename

    def write_tweet(self, tweet):
        # add tweet to list if it is a reply to the tweet we are watching
        if self.tweet_cnt < self.tweet_limit:
            if tweet['lang'] == "en" and tweet['in_reply_to_status_id_str'] == self.tweet_id_to_watch:
                self.tweet_cnt += 1
                print(tweet['text'] + '\n')
                self.tweets_arr.append(tweet)
        # write output
        else: 
            filename = self.find_available_filename('replies')
           # write file and reset count
            with open(filename,'w') as fp:
                fp.write(json.dumps(self.tweets_arr))
                self.tweets_arr.clear()
                self.tweet_cnt = 0

if __name__ == '__main__':
    try:
        # authenticate and setup api
        auth = tweepy.OAuthHandler('g83Pgpo62RNdGE4K74908vnkO', 'b7i2VnIgqazNdperwevjDUzONDVBJACEhbffEHYwh1OILAHQvI')
        auth.set_access_token('2377704086-Jf6k8y6KTy99qpvDIWZLpQFbm19ika3JrtZKF4q', 'I7T4H5H23MnS4SpXv5B2p5nUMHmaDQJ5fYxOmHCuuFmug')
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
       
        #  parse program args
        if len(sys.argv) is 3:
            num_tweets_to_read = sys.argv[1]
            original_tweet_id = sys.argv[2]
        else:
            print('usage: python3 stream_tweets.py <num_tweets_per_file> <original tweet id>')
            exit()
 
        # get user who wrote original tweet
        status_json = api.get_status(original_tweet_id)._json
        original_author = status_json['user']['screen_name']
        
        # prepare for streaming 
        my_listner = Listener(num_tweets_to_read, original_tweet_id)

        # write original tweet
        orig_tweet_filename = my_listner.find_available_filename('original_tweet')
        with open(orig_tweet_filename, 'w') as fp:
            fp.write(json.dumps(status_json))

        # stream tweets
        streamer = tweepy.Stream(auth, listener=my_listner, timeout=30000)
        streamer.filter(track=['@' + original_author])
        streamer.sample()
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

