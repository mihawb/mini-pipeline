#!/bin/bash
set -euo pipefail

KAFKA_BOOTSTRAP_SERVER="kafka:29092"
KAFKA_TOPICS=""

for kafka_topics_candidate in \
  "/kafka/bin/kafka-topics.sh" \
  "/opt/kafka/bin/kafka-topics.sh"
do
  if [ -x "$kafka_topics_candidate" ]; then
    KAFKA_TOPICS="$kafka_topics_candidate"
    break
  fi
done

if [ -z "$KAFKA_TOPICS" ]; then
  echo "Kafka topics CLI was not found in the bootstrap image" >&2
  exit 1
fi

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
