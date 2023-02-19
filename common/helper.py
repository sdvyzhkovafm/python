import argparse
import re
import shutil
import os

from operator import add

from pyspark import SparkContext, RDD
from pyspark.sql import DataFrame, SparkSession

__all__ = ['parse_args', 'extract_text_data', 'extract_csv_data', 'transform_data', 'write_data_to_text']


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Important job arguments')
    parser.add_argument('--input_path', type=str, required=True, dest='input_path',
                        help='Path to the input file for word count')

    return parser.parse_args()


def extract_text_data(spark: SparkContext, input_path: str) -> RDD:
    lines = spark.textFile(input_path)
    return lines


def extract_csv_data(ss: SparkSession, input_path: str):
    lines = ss.read.csv(input_path)\
        .withColumnRenamed("_c1", "product_id")\
        .withColumnRenamed("_c2", "user_id")
    csv_data = (
        lines
        .rdd
        .map(lambda row: (row[2], row[1]))
        .collect()
    )
    del csv_data[0]

    return csv_data


def transform_data(lines: RDD) -> RDD:
    counts = (
        lines
        .flatMap(lambda line: re.split('\W+', line.lower().strip()))
        .filter(lambda x: len(x) > 3)
        .map(lambda w: (w, 1))
        .reduceByKey(add)
    )
    return counts


def write_data_to_text(lines: RDD, out_path: str) -> None:
    if os.path.exists(out_path) and os.path.isdir(out_path):
        shutil.rmtree(out_path)
    lines.saveAsTextFile(out_path)
