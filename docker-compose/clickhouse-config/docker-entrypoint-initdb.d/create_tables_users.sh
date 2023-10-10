#!/bin/bash
set -e
clickhouse client -n <<-EOSQL
CREATE TABLE IF NOT EXISTS users
(
gender LowCardinality(String),
name Tuple(title String, first String, last String),
location Tuple(street Tuple(number UInt32, name String), city String, state String, country String, postcode String, coorditanes Tuple(latitude String, longitude String), timezone Tuple(offset String, description String)),
email String,
login Tuple(uuid UUID, username String, password String, salt String, md5 String, sha1 String, sha256 String),
dob Tuple(date String, age UInt32),
registered Tuple(date String, age UInt32),
phone String,
cell String,
id Tuple(name LowCardinality(String), value String),
picture Tuple(large String, medium String, thumbnail String),
nat LowCardinality(String) 
) 
ENGINE = MergeTree 
ORDER BY name;

CREATE TABLE IF NOT EXISTS users_queue 
(
gender LowCardinality(String),
name Tuple(title String, first String, last String),
location Tuple(street Tuple(number UInt32, name String), city String, state String, country String, postcode String, coorditanes Tuple(latitude String, longitude String), timezone Tuple(offset String, description String)),
email String,
login Tuple(uuid UUID, username String, password String, salt String, md5 String, sha1 String, sha256 String),
dob Tuple(date String, age UInt8),
registered Tuple(date String, age UInt8),
phone String,
cell String,
id Tuple(name LowCardinality(String), value String),
picture Tuple(large String, medium String, thumbnail String),
nat LowCardinality(String) 
)
ENGINE = Kafka('kafka-broker-1:9092', 'users', 'users_group',
            'JSONEachRow') settings kafka_thread_per_consumer = 0, kafka_num_consumers = 1;

CREATE MATERIALIZED VIEW IF NOT EXISTS
users_queue_mv TO users 
AS SELECT * FROM users_queue;

CREATE TABLE IF NOT EXISTS users_flat
(
first_name String,
last_name String,
city String,
country LowCardinality(String),
username String,
password String,
date_of_birth Date32,
date_registered DateTime64
)
ENGINE = MergeTree
ORDER BY first_name;

CREATE MATERIALIZED VIEW IF NOT EXISTS
users_flat_mv TO users_flat
AS SELECT
tupleElement(name, 'first') AS first_name,
tupleElement(name, 'last') AS last_name,
tupleElement(location, 'city') AS city,
tupleElement(location, 'country') AS country,
tupleElement(login, 'username') AS username,
tupleElement(login, 'password') AS password,
toDate32(parseDateTime64BestEffort(tupleElement(dob, 'date'))) AS date_of_birth,
parseDateTime64BestEffortOrNull(tupleElement(registered, 'date')) AS date_registered
FROM users_queue;
EOSQL