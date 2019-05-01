import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;


public class TweetParser {
    private String id;
    private int retweetCount;
    private String userId;
    private String stateInfo;
    private int sentimentScore;
    private String text;
    private int followersCount;
    private int friendsCount;
    private int favoriteCount;
    private boolean sensitive;
    private String location;
    private String replyCountStr;
    private String quoteCountStr;
    private boolean isQuoted;
    double popularityScore;
    double viralScore; 
    private String inResponseToID;


    public void setPopularityScore(double popularityScore) {
        this.popularityScore = popularityScore;
    }


    public TweetParser(String tweet) throws ParseException {
/*        JSONParser parser = new JSONParser();
        JSONObject jsonTweet = (JSONObject) parser.parse(tweet);
        this.id = (String) jsonTweet.get("id_str");
        this.text = (String) jsonTweet.get("text");
        String dataRetweet = (String) jsonTweet.get("retweeted_status");
        JSONObject retweetJson = (JSONObject) parser.parse(dataRetweet);
        this.retweetCount = Integer.parseInt((String)retweetJson.get("retweet_count"));
        this.replyCountStr = (String)retweetJson.get("reply_count");
        this.quoteCountStr = (String)retweetJson.get("quote_count");
        this.favoriteCount = Integer.parseInt((String)retweetJson.get("favorite_count"));
        this.sensitive = Boolean.parseBoolean((String)retweetJson.get("possibly_sensitive"));
        this.isQuoted = Boolean.parseBoolean((String)retweetJson.get("is_quote_status"));
        String infoUser = (String) jsonTweet.get("user");
        JSONObject userJson = (JSONObject) parser.parse(infoUser);
        this.userId = (String) userJson.get("id_str");
        this.followersCount = Integer.parseInt((String) userJson.get("followers_count"));
        this.friendsCount = Integer.parseInt((String) userJson.get("friends_count"));
        this.stateInfo = (String) jsonTweet.get("location");

*/
				JSONParser parser = new JSONParser();
        JSONObject jsonTweet = (JSONObject) parser.parse(tweet);
        this.id = jsonTweet.get("id_str").toString();
	if (jsonTweet.get("in_reply_to_status_id_str") != null) {
		this.inResponseToID = jsonTweet.get("in_reply_to_status_id_str").toString();
	}
        this.text = jsonTweet.get("text").toString();
        if (jsonTweet.containsKey("retweeted_status")) {
            String dataRetweet = jsonTweet.get("retweeted_status").toString();
            JSONObject retweetJson = (JSONObject) parser.parse(dataRetweet);
            this.retweetCount = Integer.parseInt(retweetJson.get("retweet_count").toString());
            this.replyCountStr = retweetJson.get("reply_count").toString();
            this.quoteCountStr = retweetJson.get("quote_count").toString();
            this.favoriteCount = Integer.parseInt(retweetJson.get("favorite_count").toString());
            this.sensitive = Boolean.parseBoolean(retweetJson.get("favorite_count").toString());
            this.isQuoted = Boolean.parseBoolean(retweetJson.get("is_quote_status").toString());
        }
        String infoUser = jsonTweet.get("user").toString();
        JSONObject userJson = (JSONObject) parser.parse(infoUser);
        this.userId = userJson.get("id_str").toString();
        this.followersCount = Integer.parseInt(userJson.get("followers_count").toString());
        this.friendsCount = Integer.parseInt(userJson.get("friends_count").toString());
        computeSentiment();
        setLocation();
        this.popularityScore = computePopularityScore();
	this.viralScore = computeViralScore();
    }

    private void computeSentiment() {
        // Implement
        // Use this.text to get tweet.
    	SentimentAnalysis analysis = new SentimentAnalysis();
    	
        this.sentimentScore = analysis.extractTextSentiment(this.text);
    }

    private void setLocation(){
        // Set location to
    	SentimentAnalysis analysis = new SentimentAnalysis();
    	
        this.location = analysis.extractState(this.stateInfo);
    }

    private double computePopularityScore() {
        double likeToFollowerRatio = (double)getFavoriteCount() / (double)getFollowersCount();
        return likeToFollowerRatio;
    }

	private double computeViralScore() {
        	double rtToFollowerRatio = (double)getRetweetCount() / (double)getFollowersCount();
		return rtToFollowerRatio;
	}

        public String getId() {
            return id;
        }

        public int getRetweetCount() {
            return retweetCount;
        }

        public String getUserId() {
            return userId;
        }

        public String getStateInfo() {
            return stateInfo;
        }

        public double getSentimentScore() {
            return sentimentScore;
        }

        public String getText() {
            return text;
        }

        public int getFollowersCount() {
            return followersCount;
        }

        public int getFriendsCount() {
            return friendsCount;
        }

        public int getFavoriteCount() {
            return favoriteCount;
        }

        public boolean isSensitive() {
            return sensitive;
        }

        public String getLocation() {
            return location;
        }

        public String getReplyCountStr() {
            return replyCountStr;
        }

        public String getQuoteCountStr() {
            return quoteCountStr;
        }

        public boolean isQuoted() {
            return isQuoted;
        }
        public double getPopularityScore() {
            return popularityScore;
        }

	public String getInResponseToID() {
		return inResponseToID;
	}

	public double getViralScore() {
		return viralScore;
	}


}
