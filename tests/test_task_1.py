import unittest

from pyspark import SparkConf, SparkContext
from etl.task_1 import load_60_of_max, load_co_count, load_max_co_count
from common.helper import transform_data


class MaxWordCountTests(unittest.TestCase):

    def setUp(self):
        config = (SparkConf()
                  .setAppName("Unit tests")
                  .setMaster('spark://localhost:7077')
                  )
        config.set("spark.driver.host", "localhost")
        self.spark = SparkContext.getOrCreate(conf=config)
        # As we have a single test we can probably have it in the test itself :)
        self.input_co_max = ["Lorem Lorem Lorem count Lorem ipsum count  ipsum ipsum count dolor sit amet, consectetur adipiscing elit elit consectetur."]
        self.input60 = ["""Lorem Lorem Lorem Lorem ipsum  ipsum  ipsum  ipsum  ipsum  ipsum  
                        dolor sit amet consectetur adipiscing elit eiusmod eiusmod eiusmod eiusmod eiusmod eiusmod eiusmod 
                        tempor incididunt labore labore labore labore labore dolore 
                        magna aliqua """]

    def test_load_60_of_max(self):
        ### Arrange
        input_rdd = transform_data(self.spark.parallelize(self.input60))
        expected = self.spark.parallelize([("ipsum", 6), ("labore", 6), ("Lorem", 4), ("eiusmod", 7)])

        ### Act
        actual = load_60_of_max(input_rdd)

        ### Assert
        expected_result = expected.sortBy(lambda x: x[1], ascending=False).collect()
        result = actual.sortBy(lambda x: x[1], ascending=False).collect()
        self.assertTrue([wordCount in expected_result for wordCount in result])
        self.assertEqual(expected_result[0][1], result[0][1])

    def test_load_co_count(self):
        ### Arrange
        input_rdd = transform_data(self.spark.parallelize(self.input_co_max))
        expected = self.spark.parallelize([("count", 3), ("consectetur", 2)]).count()

        ### Act
        actual = load_co_count(input_rdd)

        ### Assert
        self.assertEqual(expected, actual)

    def test_load_max_co_count(self):
        ### Arrange
        input_rdd = transform_data(self.spark.parallelize(self.input_co_max))
        expected = self.spark.parallelize([("count", 3)]).collect()

        ### Act
        actual = load_max_co_count(input_rdd)

        ### Assert
        self.assertTrue([wordCount in expected for wordCount in actual])
        self.assertEqual(expected[0][1], actual[0][1])

    def tearDown(self):
        self.spark.stop()


if __name__ == '__main__':
    unittest.main()