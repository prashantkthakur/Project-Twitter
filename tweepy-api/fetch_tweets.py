import tweepy
import json
import pandas as pd


def load_credentials_file(cred_file):
    try:
        with open(cred_file, 'r') as fp:
            credentials = json.load(fp)
            if len(credentials) < 1:
                print("Error: credentials file {} must contain at least one set of credentials!".format(cred_file))
                exit(-1)
            else:
                for credential in credentials:
                    if 'CONSUMER_KEY' not in credential or 'CONSUMER_SECRET' not in credential:
                        print("Error: malformed credential file %s!" % cred_file)
                        exit(-1)
    except IOError as e:
        print("Error while opening credentials file: {}".format(str(e)))
        exit(-1)
    return credentials


def fetch_tweets(screen_list,save=False,filepath=None):
    """Fetch the tweets from the timeline of provided screen_name.
    Returns pandas dataframe with 'id','text' of the tweets."""

    credentials = load_credentials_file('credentials.json')[0]
    auth = tweepy.AppAuthHandler(credentials.get("CONSUMER_KEY"), credentials.get("CONSUMER_SECRET"))
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    tweets_id = []
    tweets_text = []
    for sname in screen_list:
        print("Fetching timeline of %s"%sname)
        tweets = tweepy.Cursor(api.user_timeline, screen_name=sname, count=200).items()
        for t in tweets:
            tweet = t._json
            # Filter re-tweets.
            if tweet.get('text').startswith('RT') or tweet.get('text').startswith(' RT') or tweet.get('text').startswith('RT '):
                continue
            tweets_id.append(tweet.get('id_str'))
            tweets_text.append(tweet.get('text'))

    df = pd.DataFrame(tweets_id,columns=['id'])
    df["text"] = pd.DataFrame(tweets_text)
    if save:
        df.to_csv(filepath,index=False)
        return

    return df


def main():
    # screen name for world-war-2, education, books, religion, weather.
    screen_list = ['WW2Facts', 'WWarII', 'ABCReligion', 'usedgov', 'nationalbook', 'ReviewReligions', 'bbcweather', 'breakingweather', 'weatherchannel']
    fetch_tweets(screen_list,save=True,filepath='other_tweets.csv')


if __name__ == '__main__':
    main()
