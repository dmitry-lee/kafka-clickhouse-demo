#!/usr/bin/env python

import sys
import json
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from kafka import KafkaProducer


def read_file(file, num_messages):
    d = 0
    while d != num_messages:
        with open(file, "r") as data_file:
            for line in data_file:
                doc = json.loads(line)
                d += 1
                yield doc
                if d == num_messages:
                    return
        if num_messages == -1:
            num_messages = d


def filter(doc, fields):
    if len(filter_fields) == 0:
        return doc
    for field in fields:
        if field in doc:
            del doc[field]
    return doc


if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    args = parser.parse_args()

    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])
 
    conf = config
    topic = conf['output.topic']
    num_messages = int(conf['output.num_messages'])
    input_file = conf['input.file']
    filter_fields = []
    if 'input.filter_fields' in conf:
        filter_fields = conf['input.filter_fields'].split(',')
    
    producer = KafkaProducer(bootstrap_servers = conf['bootstrap.servers'],
                             value_serializer = lambda m : json.dumps(m).encode('utf-8'))
    delivered_records = 0
    
    def on_send_success(record_metadata):
        global delivered_records
        delivered_records += 1
        print("Produced event to topic {topic}: partition = {partition} offset = {offset}".format(
                topic=record_metadata.topic, partition=record_metadata.partition, offset=record_metadata.offset))


    def on_send_error(excp):
        print('ERROR: Message failed delivery: {}'.format(excp))
 

    # Produce data
    i = 0
    for doc in read_file(input_file, num_messages):
        doc = filter(doc, filter_fields)
        producer.send(topic, doc).add_callback(on_send_success).add_errback(on_send_error)

    # Block until the messages are sent.
    producer.flush()
    print("{} messages were produced to topic {}!".format(delivered_records, topic))