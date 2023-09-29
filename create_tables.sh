echo "Creating tables..."
sudo docker exec -it clickhouse clickhouse-client --queries-file sql/create_tables.sql
echo "Done."
