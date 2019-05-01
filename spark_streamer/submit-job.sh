#!/usr/local/bin/bash

# Need to run the publisher
#python ../codes/push_tweets.py

#spark-submit --packages org.apache.spark:spark-streaming-kafka-0-10_2.11:2.3.0,com.googlecode.json-simple:json-simple:1.1.1 --class SparkConsumer build/libs/kafka-spark-streamer-1.0.jar

spark-submit --packages edu.stanford.nlp:stanford-corenlp:3.9.2,org.twitter4j:twitter4j-core:4.0.7,org.apache.spark:spark-streaming-kafka-0-10_2.11:2.3.0,com.googlecode.json-simple:json-simple:1.1.1 --class SparkConsumer build/libs/kafka-spark-streamer-1.0.jar
