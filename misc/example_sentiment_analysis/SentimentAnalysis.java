//Author: Jake Johnson
//4/23/2019

import twitter4j.GeoLocation;
import twitter4j.Status;
import java.util.List;
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
	
	public GeoLocation extractLocation() {
		GeoLocation location = tweet.getGeoLocation();
		return location;
	}
}
