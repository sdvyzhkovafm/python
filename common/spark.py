from os import listdir, path
import json

import os
import sys
REPO_DIRNAME = os.path.abspath('')


# from pyspark import SparkConf, SparkContext
from pyspark import SparkConf, SparkContext
from typing import Optional, Tuple

# from common import logging


def start_spark(
        app_name: Optional['str'] = 'sample_homework_job',
        master: Optional['str'] = 'spark://localhost:7077',
        jar_packages=[],
        files=[],
        spark_config={}
) -> SparkContext:
    config = (SparkConf()
              .setAppName(app_name)
              .setMaster(master)
              )

    config.set('spark.jars.packages', ','.join(jar_packages))
    config.set('spark.files', ','.join(files))

    for k, v in spark_config.items():
        config.set(k, v)

    sc = SparkContext.getOrCreate(conf=config)

    return sc
