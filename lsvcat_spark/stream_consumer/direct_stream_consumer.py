# Standard library imports
import os
import configparser
import argparse
import json 


# Third party imports
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkConf
from pyspark import SparkFiles


def init_logger(spark_context, app_name):
    global logger
    logger = spark_context._jvm.org.apache.log4j
    logger = logger.LogManager.getLogger(app_name)


def read_configuration():
    # Extract configuration file dir abs path
    #root = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    
    # Read configuration
    global config
    config = configparser.ConfigParser()
    config.read(os.path.join(SparkFiles.getRootDirectory(), 'config.ini'))



def parse_arguments():
    parser = argparse.ArgumentParser(description='Processing arguments related to spark stream consumer module.')
    parser.add_argument('--app_name',  type=str, help='Spark application name', 
                            default='default_stream_consumer_app')
    parser.add_argument('--kservers',  type=str, help='Kafka bootstrap servers urls separated by comma. Default value used is one specified within config.', 
                            default=f'{config["STREAM"]["bootstrap_servers"]}')
    parser.add_argument('--ktopics',  type=str, help='Kafka topics to subscribe to, separated by comma. Default value used is one specified within config.', 
                            default=f'{config["STREAM"]["default_topic"]}')

    args = parser.parse_args
    return args


if __name__ == "__main__":
    #os.environ['PYSPARK_SUBMIT_ARGS'] = "--packages=org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.5 pyspark-shell"
    sconf = SparkConf()
    #sconf.setMaster('spark://localhost:7077')
    #sc = SparkContext(appName=args.app_name, conf=sconf)
    app_name = 'default_stream_consumer_app'
    sc = SparkContext(appName=app_name, conf=sconf)
    ssc = StreamingContext(sc, 2)

    
    
    read_configuration()
    init_logger(sc, app_name)

    env_key = 'default'

    #args = parse_arguments()
    broker_topics = [config[env_key]["default_topic"]]
    broker_list = config[env_key]["bootstrap_servers"]


    #broker_topics = ['ts_obects_and_weather']
    if ',' in args.ktopics:
        broker_topics = args.ktopics.split(',')
    else:
        broker_topics.append(args.ktopics)

    #kvs = KafkaUtils.createDirectStream(ssc, broker_topics, 
    #    {"metadata.broker.list":args.kservers})

    kvs = KafkaUtils.createDirectStream(ssc, broker_topics, 
        #{"metadata.broker.list":"localhost:9092"})
        {"metadata.broker.list":"localhost:9092,broker:29092"})

    # def store_data(rdd):
    #     if not rdd.isEmpty():
    #         rdd.toDF
    sc.sparkSession
    try:
        parsed = kvs.map(lambda v: json.loads(v[1]))
        parsed.pprint()
    except:
        logger.error('Error loading message')
    #print(parsed)
    

    ssc.start()
    ssc.awaitTermination()
