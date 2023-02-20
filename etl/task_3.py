'''
    Find all critical periods of time when it is possible to improve capacity
'''

import os
import shutil
import warnings

from pyspark import RDD
from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.functions import *
from pyspark.sql.types import StructField, LongType, FloatType

warnings.filterwarnings('ignore')


def main():
    number_cores = 2
    memory_gb = 4

    ss = (SparkSession
          .builder
          .appName('Bike Rent')
          .master(f'local[{number_cores}]')
          .config('spark.driver.memory', f'{memory_gb}g')
          .config('spark.driver.host', 'localhost')
          .getOrCreate())
    ssc = ss.sparkContext

    stations_input = '../input/stations.csv'
    register_input = '../input/register.csv'
    out_path = '../output/new_test_file'

    stations = extract_data(ss, stations_input)
    register = extract_data(ss, register_input)

    criticality = compute_criticality(ssc, register)
    output_data = load_output_data(ssc, stations, criticality, 0.15)

    if os.path.exists(out_path) and os.path.isdir(out_path):
        shutil.rmtree(out_path)
    output_data.write.csv(out_path)

    ss.stop()


def load_output_data(ssc: SparkContext, stations: DataFrame, criticality: RDD, coef: float) -> DataFrame:
    filtered_crit = criticality.filter(lambda row: row[3] > coef).collect()
    schema = StructType([
        StructField("station", StringType(), nullable=True),
        StructField("weekday", StringType(), nullable=True),
        StructField("hour", StringType(), nullable=True),
        StructField("criticality", FloatType(), nullable=True)
    ])
    crit_df = SQLContext(ssc).createDataFrame(filtered_crit, schema)

    joined_tables = crit_df.join(stations, crit_df.station == stations.id, 'inner')\
        .select( 'station', 'longitude', 'latitude', 'name', 'weekday', 'hour', 'criticality')\
        .orderBy(desc(crit_df.criticality), crit_df.station, crit_df.weekday, crit_df.hour)

    return joined_tables


def compute_criticality(ssc: SparkContext, register_df: DataFrame) -> RDD:
    total_row_numbers = register_df\
        .selectExpr('station', 'date_format(timestamp,"EE") as weekday', 'hour(timestamp) as hour')\
        .groupby('station', 'weekday', 'hour')\
        .count()\
        .withColumnRenamed('count', 'total_count')\
        .na.drop()
    invalid_count = register_df\
        .selectExpr('station', 'date_format(timestamp,"EE") as weekday', 'hour(timestamp) as hour') \
        .filter('used_slots == 0 and free_slots == 0') \
        .groupby('station', 'weekday', 'hour') \
        .count()\
        .withColumnRenamed('count', 'invalid_count')\
        .na.drop()

    cond = [total_row_numbers.station == invalid_count.station,
            total_row_numbers.weekday == invalid_count.weekday,
            total_row_numbers.hour == invalid_count.hour]
    valid_count_rdd = total_row_numbers.join(invalid_count, cond, 'left').collect()

    def calc(num1, num2):
        if num2 is not None:
            return num1 - num2
        else:
            return num1

    valid_count = ssc.parallelize(valid_count_rdd)\
        .map(lambda row: [row['station'], row['weekday'], row['hour'], calc(row['total_count'], row['invalid_count'])])\
        .collect()
    schema = StructType([
        StructField("station", StringType(), nullable=True),
        StructField("weekday", StringType(), nullable=True),
        StructField("hour", StringType(), nullable=True),
        StructField("valid_count", LongType(), nullable=True)
    ])
    valid_count_df = SQLContext(ssc).createDataFrame(valid_count, schema)

    empty_free_slots_total = register_df.filter(register_df.free_slots == 0)
    empty_free_slots_valid_count = empty_free_slots_total\
        .filter(empty_free_slots_total.used_slots != 0)\
        .selectExpr('station', 'date_format(timestamp,"EE") as weekday', 'hour(timestamp) as hour')\
        .groupby('station', 'weekday', 'hour') \
        .count()\
        .withColumnRenamed('count', 'empty_count')

    cond = [empty_free_slots_valid_count.station == valid_count_df.station,
            empty_free_slots_valid_count.weekday == valid_count_df.weekday,
            empty_free_slots_valid_count.hour == valid_count_df.hour]
    crit_rdd = valid_count_df.join(empty_free_slots_valid_count, cond, 'left').collect()

    def divide_calc(num1, num2):
        if num1 is None or num1 == 0:
            return 0
        elif num1 != 0 and num2 != 0:
            return num1/num2
        elif num1 != 0 and num2 == 0:
            return 1

    crit = ssc.parallelize(crit_rdd)\
        .map(lambda row: (row['station'], row['weekday'], row['hour'], divide_calc(row['empty_count'], row['valid_count'])))

    return crit


def extract_data(spark: SparkSession, inputpath: str) -> DataFrame:
    csv_data = spark\
        .read\
        .option('header', True)\
        .option('delimiter', '\t')\
        .csv(inputpath)

    return csv_data


if __name__ == '__main__':
    main()
