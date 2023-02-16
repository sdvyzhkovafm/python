#!/usr/bin/env bash

Help()
{
    echo "Download Kafka"
    echo
    echo "Syntax: get_kafka.sh [-d]"
    echo "options:"
    echo "d     (Optional) if you want to delete and re-download"
    echo
}

while getopts ":d" option; do
    case $option in
        d)
            CLEAN_DOWNLOAD="yes";;
        \?)
            echo "Invalid option."
            Help
            exit;;
    esac
done

KAFKA_VERSION=3.4.0
SCALA_VERSION=2.13
SCRIPT_DIR=$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )
KAFKA_HOME="${SCRIPT_DIR}/kafka"

if [[ $CLEAN_DOWNLOAD || ! -d $KAFKA_HOME ]]; then
    if [[ -d $KAFKA_HOME ]]; then rm -rf ${KAFKA_HOME}; fi
    mkdir -p ${KAFKA_HOME};
    echo "Downloading Kafka ${KAFKA_VERSION}..."
    curl "https://downloads.apache.org/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz" |\
        tar -xz -C ${KAFKA_HOME} --strip=1
fi