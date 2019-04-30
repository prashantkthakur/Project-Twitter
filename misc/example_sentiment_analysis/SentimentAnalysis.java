//Author: Jake Johnson
//4/23/2019

import twitter4j.GeoLocation;
import twitter4j.Status;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.sentiment.SentimentCoreAnnotations;
import edu.stanford.nlp.util.CoreMap;

public class SentimentAnalysis{
	private Status tweet;
	
	public SentimentAnalysis(Status tweet) {
		this.tweet = tweet;
	}
	
	public int extractTextSentiment() {

		int sentiment = 0;
		Properties properties = new Properties();
		properties.setProperty("annotators", "tokenize, ssplit, pos, parse, sentiment");
		StanfordCoreNLP pipeline = new StanfordCoreNLP(properties);

		Annotation document = new Annotation(tweet.getText());
		pipeline.annotate(document);
		List<CoreMap> sentences = document.get(SentencesAnnotation.class);

		for(CoreMap sentence: sentences) {
			String sentimentWord = sentence.get(SentimentCoreAnnotations.SentimentClass.class);
			if(sentimentWord.contentEquals("Very Positive")) {
				sentiment += 2;
			} else if (sentimentWord.contentEquals("Positive")) {
				sentiment += 1;
			} else if (sentimentWord.contentEquals("Neutral")) {
				sentiment += 0;
			} else if (sentimentWord.contentEquals("Negative")) {
				sentiment += -1;
			} else if (sentimentWord.contentEquals("Very Negative")) {
				sentiment += -2;
			}
		}
		
		if(sentiment > 2) {
			sentiment = 2;
		} else if (sentiment < 2) {
			sentiment = -2;
		}
		
		return sentiment;
	}

	public int extractRetweet() {
		int retweets = tweet.getRetweetCount();	
		return retweets;
	}
	
	public int extractFavorite() {
		int favorites = tweet.getFavoriteCount();
		return favorites;
	}
	
	public String extractState() {
		String [] locationParts = tweet.getUser().getLocation().split(",| ");
		
		Map<String, String> states = new HashMap<String, String>();
		states.put("alabama","AL");
		states.put("alaska","AK");
		states.put("alberta","AB");
		states.put("american samoa","AS");
		states.put("arizona","AZ");
		states.put("arkansas","AR");
		states.put("armed forces (ae)","AE");
		states.put("armed forces americas","AA");
		states.put("armed forces pacific","AP");
		states.put("british columbia","BC");
		states.put("california","CA");
		states.put("colorado","CO");
		states.put("connecticut","CT");
		states.put("delaware","DE");
		states.put("district of columbia","DC");
		states.put("florida","FL");
		states.put("georgia","GA");
		states.put("guam","GU");
		states.put("hawaii","HI");
		states.put("idaho","ID");
		states.put("illinois","IL");
		states.put("indiana","IN");
		states.put("iowa","IA");
		states.put("kansas","KS");
		states.put("kentucky","KY");
		states.put("louisiana","LA");
		states.put("maine","ME");
		states.put("manitoba","MB");
		states.put("maryland","MD");
		states.put("massachusetts","MA");
		states.put("michigan","MI");
		states.put("minnesota","MN");
		states.put("mississippi","MS");
		states.put("missouri","MO");
		states.put("montana","MT");
		states.put("nebraska","NE");
		states.put("nevada","NV");
		states.put("new brunswick","NB");
		states.put("new hampshire","NH");
		states.put("new jersey","NJ");
		states.put("new mexico","NM");
		states.put("new york","NY");
		states.put("newfoundland","NF");
		states.put("north carolina","NC");
		states.put("north dakota","ND");
		states.put("northwest territories","NT");
		states.put("nova scotia","NS");
		states.put("nunavut","NU");
		states.put("ohio","OH");
		states.put("oklahoma","OK");
		states.put("ontario","ON");
		states.put("oregon","OR");
		states.put("pennsylvania","PA");
		states.put("prince edward island","PE");
		states.put("puerto rico","PR");
		states.put("quebec","QC");
		states.put("rhode island","RI");
		states.put("saskatchewan","SK");
		states.put("south carolina","SC");
		states.put("south dakota","SD");
		states.put("tennessee","TN");
		states.put("texas","TX");
		states.put("utah","UT");
		states.put("vermont","VT");
		states.put("virgin Islands","VI");
		states.put("virginia","VA");
		states.put("washington","WA");
		states.put("west Virginia","WV");
		states.put("wisconsin","WI");
		states.put("wyoming","WY");
		states.put("yukon territory","YT");
		
		if(states.containsKey(tweet.getUser().getLocation().toLowerCase()))
			return states.get(tweet.getUser().getLocation().toLowerCase());
		if(states.containsValue(tweet.getUser().getLocation().toUpperCase()))
			return tweet.getUser().getLocation().toUpperCase();
		
		for(String location: locationParts) {
			if(states.containsKey(location.toLowerCase()))
				return states.get(location.toLowerCase());
			if(states.containsValue(location.toUpperCase()))
				return location.toUpperCase();
			
		}
		return "USA";
	}
	
	public int extractFollowers() {
		return tweet.getUser().getFollowersCount();
	}
}
