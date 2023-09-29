CREATE TABLE IF NOT EXISTS users
(
uuid UUID, 
username String,
password String
) 
ENGINE = MergeTree 
ORDER BY uuid;

CREATE TABLE IF NOT EXISTS users_queue 
(
uuid UUID,
username String,
password String
)
ENGINE = Kafka('kafka-broker-1:9092', 'users', 'users_group',
            'JSONEachRow') settings kafka_thread_per_consumer = 0, kafka_num_consumers = 1;

CREATE MATERIALIZED VIEW IF NOT EXISTS
users_queue_mv TO users 
AS SELECT * FROM users_queue;
