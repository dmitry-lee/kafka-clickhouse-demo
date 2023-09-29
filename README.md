# kafka-clickhouse-demo

### Requirements
- Python 3
- Docker
---
### How to run demo
Go to docker-compose directory:
```
cd docker-compose
```
Deploy kafka cluster:
```
docker-compose -f common.yml -f kafka_cluster.yml up -d
```
If containers fail to start change owner of volumes directory:
```
sudo chown -hR <username> volumes/
```
Deploy clickhouse:
```
docker-compose -f common.yml -f clickhouse.yml up -d
```
Create kafka topic:
```
docker-compose -f common.yml -f init_kafka.yml up
```

Generate data and produce to kafka topic:
```
cd ..

pip install -r requirements.txt

python3 generate_users_ndjson.py

python3 kafka_producer.py users.config.ini
```

Create clickhouse tables:
```
sh create_tables.sh
```
or
```
sudo docker exec -it clickhouse clickhouse-client --queries-file sql/create_tables.sql
```
Run clickhouse client:
```
sudo docker exec -it clickhouse clickhouse-client
```
Do some queries:
```
SELECT * FROM users
```