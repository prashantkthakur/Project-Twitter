import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import twitter4j.Status;
import twitter4j.TwitterException;
import twitter4j.TwitterObjectFactory;

public class SentimentTester {

	public static void main(String[] args) throws Exception{
		BufferedReader reader = new BufferedReader(new FileReader(args[0]));
		
		String objs = "";
		String st;
		while((st = reader.readLine()) != null) {
			objs += st;
		}
		
		ArrayList<Status> statuses = new ArrayList<>();
		
		try {
			JSONParser parser = new JSONParser();
			JSONArray jArray = (JSONArray)parser.parse(objs);
			
			for(int i = 0; i < jArray.size(); i++) {
				Status tweet = TwitterObjectFactory.createStatus((String) jArray.get(i));
				statuses.add(tweet);
			}
		} catch(Exception e) {
			
		} 
		
		for(Status tweet: statuses) {
			SentimentAnalysis analysis = new SentimentAnalysis(tweet);
			System.out.println("Text Sentiment: " + analysis.extractTextSentiment());
			System.out.println("Favorite Sentiment: " + analysis.extractFavorite());
			System.out.println("Retweet Sentiment: " + analysis.extractRetweet());

		}
	}

}
