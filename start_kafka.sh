#!/usr/bin/env bash

SCRIPT_DIR=$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )
KAFKA_HOME="${SCRIPT_DIR}/kafka"
#echo ${KAFKA_HOME}
#echo ${SCRIPT_DIR}

# So it works in Zsh :)

echo "Starting Zookeeper..."
bash -c "${KAFKA_HOME}/bin/zookeeper-server-start.sh -daemon ${KAFKA_HOME}/config/zookeeper.properties"
sleep 5
echo "Starting Kafka broker..."
bash -c "${KAFKA_HOME}/bin/kafka-server-start.sh -daemon ${SCRIPT_DIR}/mac.properties"
sleep 5
echo "Creating topic 'iot'..."
bash -c "${KAFKA_HOME}/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --topic iot"
