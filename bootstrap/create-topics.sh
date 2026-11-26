#!/bin/sh
set -eu

KAFKA_BOOTSTRAP_SERVER="localhost:29092"
KAFKA_TOPICS="/opt/kafka/bin/kafka-topics.sh"

echo "Waiting for Kafka..."
until "$KAFKA_TOPICS" \
  --bootstrap-server "$KAFKA_BOOTSTRAP_SERVER" \
  --list >/dev/null 2>&1
do
  sleep 2
done

create_topic() {
  local topic="$1"
  local partitions="$2"
  local cleanup_policy="${3:-delete}"

  echo "Creating topic $topic"
  "$KAFKA_TOPICS" \
    --bootstrap-server "$KAFKA_BOOTSTRAP_SERVER" \
    --create \
    --if-not-exists \
    --topic "$topic" \
    --partitions "$partitions" \
    --replication-factor 1 \
    --config "cleanup.policy=$cleanup_policy"
}

create_topic "connect-configs" 1 compact
create_topic "connect-offsets" 25 compact
create_topic "connect-status" 5 compact

create_topic "socnet.entities.users" 1
create_topic "socnet.entities.posts" 1
create_topic "socnet.activity.follows" 1
create_topic "socnet.activity.likes" 1
create_topic "socnet.entities.comments" 1
