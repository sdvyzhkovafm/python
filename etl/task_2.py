"""
    Extract 100 pairs of unique pairs user-product
"""

import warnings
from operator import add
from typing import List

from pyspark import SparkContext, RDD
from pyspark.sql import SparkSession
from itertools import combinations
from common.helper import write_data_to_text, extract_csv_data

number_cores = 2
memory_gb = 4


def main():
    ss = (SparkSession
             .builder
             .appName('Reviews handler')
             .master(f"local[{2}]")
             .getOrCreate())
    ssc = ss.sparkContext

    input_path_dev = "../input/Sample.csv"
    input_path_prod = "../input/Reviews.csv"

    out_path = '../output/review_pairs'

    data = extract_csv_data(ss, input_path_dev)
    pairs = get_pairs_purchased_together(ssc, get_all_purchased_products_pairs(ssc, data))
    write_data_to_text(ssc.parallelize(pairs), out_path)

    ss.stop()


def get_all_purchased_products_pairs(ssc: SparkContext, csv_data: RDD):
    def complete_tuple(x, y) -> List:
        if (type(x) != list) and (type(y) != list):
            x = [x, y]

        elif (type(x) != list) and (type(y) == list):
            x = [x]
            for yitem in y:
                x.append(yitem)

        elif (type(x) == list) and (type(y) == list):
            for yitem in y:
                x.append(yitem)

        elif (type(x) == list) and (type(y) != list):
            if y not in x:
                x.append(y)
        return x

    def get_pairs(list: List):
        pairs = combinations(list, 2)
        return pairs

    def sort_pair(list):
        if list[0] > list[1]:
            (list[1], list[0])
            new_tuple = (list[1], list[0])
            return new_tuple
        else:
            return list

    pair_list = ssc.parallelize(csv_data) \
        .reduceByKey(lambda x, y: complete_tuple(x, y)) \
        .map(lambda row: row[1]) \
        .filter(lambda value: type(value) == list) \
        .map(lambda row: get_pairs(row)) \
        .flatMap(lambda pair: pair) \
        .map(lambda pair: sort_pair(pair)) \
        .collect()

    return pair_list


def get_pairs_purchased_together(ssc: SparkContext, pairs_list: RDD) -> RDD:
    count_pairs = ssc\
        .parallelize(pairs_list)\
        .map(lambda pair: (pair, 1))\
        .reduceByKey(add)\
        .map(lambda x: (x[1], x[0]))\
        .sortByKey(False)\
        .map(lambda x: (x[1], x[0]))\
        .take(100)

    return count_pairs


if __name__ == '__main__':
    main()
