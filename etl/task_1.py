import re

from operator import add
from pyspark import SparkContext, RDD, SparkConf

from common.spark import start_spark


def load_max_co_count(counts: RDD) -> None:
    max_number = (
        counts
        .filter(lambda x: re.findall('^co', x[0]))
        .map(lambda x: (x[1], x[0]))
        .sortByKey(False)
        .map(lambda x: (x[1], x[0]))
        .take(1)
    )
    print(max_number)
