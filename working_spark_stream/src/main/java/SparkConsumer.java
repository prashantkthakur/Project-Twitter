import java.util.*;

import org.apache.spark.SparkContext;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.sql.*;
import org.apache.spark.sql.Dataset;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.spark.SparkConf;

//import org.apache.spark.sql.SQLContext;
import org.apache.spark.streaming.Durations;
import org.apache.spark.streaming.api.java.*;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.streaming.kafka010.ConsumerStrategies;
import org.apache.spark.streaming.kafka010.KafkaUtils;
import org.apache.spark.streaming.kafka010.LocationStrategies;
import scala.Tuple2;
import org.apache.log4j.Logger;
import org.apache.log4j.Level;


public class SparkConsumer {


    public static void main(String[] args) throws InterruptedException {
        SparkConf conf = new SparkConf().setMaster("local").setAppName("Kafka");
        Logger.getLogger("org").setLevel(Level.OFF);
        Logger.getLogger("akka").setLevel(Level.OFF);
        JavaSparkContext sc = new JavaSparkContext(conf);
        JavaStreamingContext ssc = new JavaStreamingContext(sc, Durations.seconds(10));

        Map<String, Object> kafkaParams = new HashMap<>();
        kafkaParams.put("bootstrap.servers", "acorn:9092");
        kafkaParams.put("key.deserializer", StringDeserializer.class);
        kafkaParams.put("value.deserializer", StringDeserializer.class);
        kafkaParams.put("group.id", "GOT-gid");
        kafkaParams.put("auto.offset.reset", "latest");
        kafkaParams.put("enable.auto.commit", false);
        Set<String> topics = Collections.singleton("GOT");
        //    Collection<String> topics = Arrays.asList("GOT", "topicB");
        JavaInputDStream<ConsumerRecord<String, String>> messages =
                KafkaUtils.createDirectStream(
                        ssc,
                        LocationStrategies.PreferConsistent(),
                        ConsumerStrategies.<String, String> Subscribe(topics, kafkaParams));

        JavaPairDStream<String, String> tweets = messages
                .mapToPair(record -> new Tuple2<>(record.key(), record.value()));


        taskExecutor(tweets);


//        JavaDStream<TweetParser> tweetObj = tweets.map(tuple2 -> {
//            TweetParser obj = new TweetParser(tuple2._2());
//            return obj;
//        });


//        JavaDStream<String> words = lines
//                .flatMap(x -> Arrays.asList(x.split("\\s+")).iterator());
//        JavaPairDStream<String, Integer> wordCounts = words
//                .mapToPair(s -> new Tuple2<>(s, 1)).reduceByKey((i1, i2) -> i1 + i2);
//        lines.foreachRDD( x-> x.collect().stream().forEach(n-> System.out.println("item of list: "+n)));



//        Dataset<Row> rankTable = sc.createDataFrame(out, HelperClass.PageRank.class).cache();

        ssc.start();
        ssc.awaitTermination();


    }



    private static void taskExecutor(JavaPairDStream<String, String> tweets){
        JavaDStream<TweetParser> tweetObj = tweets.map(tuple2 -> {
            TweetParser obj = new TweetParser(tuple2._2());
            return obj;
        });

        tweetObj.foreachRDD(rdd->{
            SQLContext sqlContext = JavaSQLContextSingleton.getInstance(rdd.context());
            Dataset<Row> tweetDS = sqlContext.createDataFrame(rdd, TweetParser.class);
            tweetDS.createOrReplaceTempView("tweet");
	    Dataset<Row> top = sqlContext.sql("SELECT id,retweetCount FROM tweet");
            top.show();
	    showReplies(sqlContext);
        });
    }

	private static void showReplies(SQLContext sqlContext) {
		Dataset<Row> top = sqlContext.sql("SELECT id,inResponseToID FROM tweet WHERE inResponseToID IS NOT NULL");
		Dataset<Row> top2 = sqlContext.sql("SELECT id,viralScore,popularityScore FROM tweet");
		Dataset<Row> avgSentiment = sqlContext.sql("SELECT COUNT(location) AS NumberAtLocation, AVG(sentimentScore) AS AverageSentiment, location FROM tweet GROUP BY location");
		Dataset<Row> mostPopular = sqlContext.sql("SELECT MAX(popularityScore) AS MostPopular, First(sentimentScore) AS Sentiment, First(location) AS Location FROM tweet");
		Dataset<Row> maxRetweets = sqlContext.sql("SELECT MAX(retweetCount) AS NumberRetweets, First(sentimentScore) AS Sentiment, First(location) AS Location FROM tweet");
		Dataset<Row> maxFaves = sqlContext.sql("SELECT MAX(favoriteCount) AS NumberFavorites, First(sentimentScore) AS Sentiment, First(location) AS Location FROM tweet");
		Dataset<Row> negativeCount = sqlContext.sql("SELECT COUNT(sentimentScore) AS NumberNegative, location FROM tweet WHERE sentimentScore=-1 OR sentimentScore=-2 GROUP BY location");
		top.show();
		top2.show();
		avgSentiment.show();
		mostPopular.show();
		maxRetweets.show();
		maxFaves.show();
		negativeCount.show();
	}

}


class JavaSQLContextSingleton {
    static private transient SQLContext instance = null;

    static public SQLContext getInstance(SparkContext sparkContext) {
        if (instance == null) {
            instance = new SQLContext(sparkContext);
        }
        return instance;
    }
}
