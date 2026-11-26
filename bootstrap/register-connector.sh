#!/bin/sh
set -eu

CONNECT_REST_URL="http://localhost:8083"
CONNECTOR_NAME="pg-social-network-connector"
CONNECTOR_CONFIG_FILE="/postgres-connector.json"

echo "Waiting for Kafka Connect..."
until curl -sf "$CONNECT_REST_URL/connectors" >/dev/null 2>&1
do
  sleep 2
done

echo "Registering connector $CONNECTOR_NAME"
curl -sf -X PUT \
  -H "Content-Type: application/json" \
  --data @"$CONNECTOR_CONFIG_FILE" \
  "$CONNECT_REST_URL/connectors/$CONNECTOR_NAME/config"
