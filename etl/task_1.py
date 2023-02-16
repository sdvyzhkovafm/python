"""
This task contains:
    counting all words which start from "co"
    counting all words which are met more than 80%
"""

import re

from pyspark import SparkContext
from pyspark import RDD
from common.spark import start_spark
from common.helper import *

def load_co(words: RDD) -> RDD:
    co_words = (
        words
        .filter(lambda x: re.findall('^co', x[0]))
        .map(lambda x: (x[1], x[0]))
        .sortByKey(False)
        .map(lambda x: (x[1], x[0]))
    )
    return co_words

def load_co_count(words: RDD) -> int:
    co_count = load_co(words).count()
    print("This is co words count: " + f'{co_count}')
    return co_count


def load_max_co_count(words: RDD) -> RDD:
    max_number = load_co(words).take(1)
    print("This co word are met the most: " + f'{max_number}')
    return max_number

def load_60_of_max(counts: RDD) -> RDD:
    max_number = (
        counts
        .filter(lambda x: x[0] != "with")
        .map(lambda x: (x[1], x[0]))
        .sortByKey(False)
        .first()
    )
    # here I took koef 60% because there are more than 2 thousand words "with"
    koef = max_number[0] * 0.6
    result = (
        counts
        .filter(lambda x: x[1] > koef)
        .sortByKey(False)
    )
    return result


spark = start_spark(
    app_name='Max Word Count',
    master="local[2]",
    spark_config={
        "spark.driver.host": "localhost"
    })
input_path = '../input/Iliad.txt'
out_path = '../output/numbers_60_of_max'
text = extract_text_data(spark, input_path)
words = transform_data(text)
co_count = load_co_count(words)
max_co_number = load_max_co_count(words)
write_data_to_text(load_60_of_max(words), out_path)
spark.stop()


