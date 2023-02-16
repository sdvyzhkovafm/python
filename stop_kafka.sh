#!/usr/bin/env bash

SCRIPT_DIR=$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )
KAFKA_HOME="${SCRIPT_DIR}/kafka"

# So it works in Zsh :)

echo "Removing topic 'iot'..."
bash -c "${KAFKA_HOME}/bin/kafka-topics.sh --delete --bootstrap-server localhost:9092 --topic iot"
sleep 5
echo "Stopping Kafka broker..."
bash -c "${KAFKA_HOME}/bin/kafka-server-stop.sh"
sleep 5
echo "Stopping Zookeeper..."
bash -c "${KAFKA_HOME}/bin/zookeeper-server-stop.sh"
echo "Cleanup dirs"
rm -rf /tmp/kafka-logs /tmp/zookeeper ${HOME}/.ivy2