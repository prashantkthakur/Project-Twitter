import java.util.*;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.spark.SparkConf;

import org.apache.spark.streaming.Durations;
import org.apache.spark.streaming.api.java.*;


import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.streaming.kafka010.ConsumerStrategies;
import org.apache.spark.streaming.kafka010.KafkaUtils;
import org.apache.spark.streaming.kafka010.LocationStrategies;
import scala.Tuple2;


public class SparkConsumer {


    public static void main(String[] args) throws InterruptedException {
        SparkConf conf = new SparkConf().setMaster("local").setAppName("Kafka");

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

        JavaPairDStream<String, String> results = messages
                .mapToPair(
                        record -> new Tuple2<>(record.key(), record.value())
                );
        JavaDStream<String> lines = results
                .map(
                        tuple2 -> tuple2._2()
                );
//        JavaDStream<String> words = lines
//                .flatMap(
//                        x -> Arrays.asList(x.split("\\s+")).iterator()
//                );
//        JavaPairDStream<String, Integer> wordCounts = words
//                .mapToPair(
//                        s -> new Tuple2<>(s, 1)
//                ).reduceByKey(
//                        (i1, i2) -> i1 + i2
//                );

        lines.foreachRDD( x-> x.collect().stream().forEach(n-> System.out.println("item of list: "+n)));

        ssc.start();
        ssc.awaitTermination();


    }

}