import tweepy
import pandas as pd
import time


def fetch_hashtags(fp,count):
    CONSUMER_KEY = 'kCsDMPpNVCZW2fq2d1MvibduN'
    CONSUMER_SECRET = '6qmVMBIJyGLjA6AYDmEA22ILPOYuHcAGclCZlWBuLFVm6orAbt'
    ACCESS_KEY = '919589727753216007-nRN64Q10pctwl1getZSd3thOSLyx8Wt'
    ACCESS_SECRET = 'qiUgYOZ1LdMoiwNzRS78MdCKYCW97amgzp0wvCFI3vgkB'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    search_texts = ["#Food", "#Recipe", "#foodrecipe", "#recipefood", "#cook", "#delicious", "#cooking"]
    print("Count...%d"%count)
    for search_text in search_texts:
        search_result = api.search(search_text, rpp=100, lang='en')
        for i in search_result:
            # print(i)
            if not i._json.get('retweeted_status'):
                # Encode the text as ASCII and remove characters that can't be encoded.
                # Decoded with utf-8 to remove b before string. eg. b'string...'
                # If error of encoding. First decode by UTF-8 and than do encoding.
                fp.write('%s,"%s"\n' % (i.id, i.text.encode('ascii', errors='ignore').decode('utf-8')))
        time.sleep(5)



def prepare_dataset(filename):
    df_tmp = pd.read_csv(filename, names=['id', 'text'])
    df = df_tmp.replace({r'\n+': ''}, regex=True)
    df['text'] = df['text'].str.replace(r"http\S+", "")  # Remove URL
    df['text'] = df['text'].str.replace(r"@\S+", "")  # Remove @words
    df['text'] = '<SOT>' + df['text'].astype(str)+'<EOT>'
    final = df[df['text'].str.split().str.len() > 15]
    # Shuffle the tweets so similar tweets are not trained at the same time.
    out = final.sample(frac=1).reset_index(drop=True)['text']
    # Save file with string length greater than 80 characters for future use
    out = out.drop_duplicates()
    out.to_csv('train_generator.txt', index=False)


def main():
    filename = 'tweets_hashtag.csv'
    fp = open(filename, 'a')
    count = 1
    for i in range(5000):
        fetch_hashtags(fp,count)
        count += 1
    prepare_dataset(filename)


if __name__ == '__main__':
    #main()
    prepare_dataset('tweets_hashtag.csv')
