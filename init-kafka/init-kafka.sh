#!/bin/bash

echo "Waiting for Kafka to be ready..."
sleep 10

kafka-topics \
    --bootstrap-server broker:29092 \
    --create \
    --if-not-exists \
    --topic reddit \
    --replication-factor 1 \
    --partitions 2 \
    --config cleanup.policy=delete \
    --config retention.ms=604800000


kafka-topics \
    --bootstrap-server broker:29092 \
    --create \
    --if-not-exists \
    --topic twitter \
    --replication-factor 1 \
    --partitions 2 \
    --config cleanup.policy=delete \
    --config retention.ms=604800000


kafka-topics \
    --bootstrap-server broker:29092 \
    --create \
    --if-not-exists \
    --topic processed-data \
    --replication-factor 1 \
    --partitions 2 \
    --config cleanup.policy=delete \
    --config retention.ms=604800000

echo "Successfully created topics:"

kafka-topics --bootstrap-server broker:29092 --list