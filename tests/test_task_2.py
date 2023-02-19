import unittest

from pyspark import SparkConf, SparkContext, RDD
from pyspark.sql import SparkSession, DataFrame
# from etl import task_2
from etl.task_2 import get_all_purchased_products_pairs, get_pairs_purchased_together
import warnings



class ProductPairCounterTests(unittest.TestCase):
    def setUp(self):
        config = (SparkConf()
                  .setAppName("Unit tests Reviews")
                  .setMaster('spark://localhost:7077')
                  )
        config.set("spark.driver.host", "localhost")
        self.spark = SparkContext.getOrCreate(conf=config)
        warnings.filterwarnings(action='ignore', category=ResourceWarning)
        # As we have a single test we can probably have it in the test itself :)
        self.input = [
            ('A3SGXH7AUHU8GW', 'B001E4KFG0'), ('A1D87F6ZCVE5NK', 'B00813GRG4'), ('ABXLMWJIXXAIN', 'B000LQOCH0'),
            ('A3SGXH7AUHU8GW', 'B000UA0QIQ'), ('A3SGXH7AUHU8GW', 'B006K2ZZ7K'), ('ADT0SRK1MGOEU', 'B006K2ZZ7K'),
            ('A1SP2KVKFXXRU1', 'B006K2ZZ7K'), ('A327PCT23YH90', 'B006K2ZZ7K'), ('A1MZYO9TZK0BBI', 'B000E7L2R4'),
            ('A21BT40VZCCYT4', 'B00171APVA'), ('A3HDKO7OW0QNK4', 'B0001PB9FE'), ('A1SP2KVKFXXRU1', 'B0009XLVG0'),
            ('A327PCT23YH90', 'B0009XLVG0'), ('A18ECVX2RJ7HUE', 'B001GVISJM'), ('A2MUGFV2TDQ47K', 'B001GVISJM'),
            ('A1CZX3CP8IKQIJ', 'B001GVISJM'), ('A3KLWF6WQ5BNYO', 'B001GVISJM'), ('AFKW14U97Z6QO', 'B001GVISJM'),
            ('A2A9X58G2GTBLP', 'B001GVISJM'), ('A3IV7CL2C13K2U', 'B001GVISJM'), ('A1WO0KGLPR5PV6', 'B001GVISJM'),
            ('AZOF9E17RGZH8', 'B001GVISJM'), ('A31OQO709M20Y7', 'B001GVISJM'), ('AJ613OLZZUG7V', 'B001GVISJM'),
            ('A22P2J09NJ9HKE', 'B001GVISJM'), ('A3FONPR03H3PJS', 'B001GVISJM'), ('A3RXAU2N8KV45G', 'B001GVISJM'),
            ('AAAS38B98HMIK', 'B001GVISJM'), ('A2F4LZVGFLD1OB', 'B00144C10S'), ('A3HDKO7OW0QNK4', 'B0001PB9FY'),
            ('A1CZX3CP8IKQIJ', 'B003F6UO7K'), ('A31OQO709M20Y7', 'B003F6UO7K'), ('A1CZX3CP8IKQIJ', 'B001EO5QW8'),
            ('A3PMM0NFVEJGK9', 'B001EO5QW8'), ('A2EB6OGOWCRU5H', 'B001EO5QW8'), ('A31OQO709M20Y7', 'B001EO5QW8'),
            ('A1MYS9LFFBIYKM', 'B001EO5QW8'), ('A3MGP2E1ZZ6GRB', 'B001EO5QW8'), ('A2GHZ2UTV2B0CD', 'B001EO5QW8'),
            ('AO80AC8313NIZ', 'B001EO5QW8')]

        self.input_pairs = [
            ('B001GVISJM', 'B003F6UO7K'), ('B001EO5QW8', 'B001GVISJM'), ('B001EO5QW8', 'B003F6UO7K'),
            ('B000UA0QIQ', 'B001E4KFG0'), ('B001E4KFG0', 'B006K2ZZ7K'), ('B000UA0QIQ', 'B006K2ZZ7K'),
            ('B001GVISJM', 'B003F6UO7K'), ('B001EO5QW8', 'B001GVISJM'), ('B001EO5QW8', 'B003F6UO7K'),
            ('B0009XLVG0', 'B006K2ZZ7K'), ('B0009XLVG0', 'B006K2ZZ7K'), ('B0001PB9FE', 'B0001PB9FY')]


    def test_get_pairs_purchased_together(self):
        ### Arrange
        expected = self.spark.parallelize([
            (('B001GVISJM', 'B003F6UO7K'), 2), (('B001EO5QW8', 'B001GVISJM'), 2), (('B001EO5QW8', 'B003F6UO7K'), 2),
            (('B000UA0QIQ', 'B001E4KFG0'), 1), (('B001E4KFG0', 'B006K2ZZ7K'), 1), (('B000UA0QIQ', 'B006K2ZZ7K'), 1),
            (('B0009XLVG0', 'B006K2ZZ7K'), 2), (('B0001PB9FE', 'B0001PB9FY'), 1)
        ]).sortByKey().collect()

        ### Act
        actual = get_pairs_purchased_together(self.spark, self.input_pairs)
        actual_result = self.spark.parallelize(actual).sortByKey().collect()
        ### Assert
        self.assertEqual(expected[0][1], actual_result[0][1])

    def test_get_all_purchased_products_pairs(self):
        ### Arrange
        expected = self.spark.parallelize([
            ('B001GVISJM', 'B003F6UO7K'), ('B001EO5QW8', 'B001GVISJM'), ('B001EO5QW8', 'B003F6UO7K'),
            ('B000UA0QIQ', 'B001E4KFG0'), ('B001E4KFG0', 'B006K2ZZ7K'), ('B000UA0QIQ', 'B006K2ZZ7K'),
            ('B001GVISJM', 'B003F6UO7K'), ('B001EO5QW8', 'B001GVISJM'), ('B001EO5QW8', 'B003F6UO7K'),
            ('B0009XLVG0', 'B006K2ZZ7K'), ('B0009XLVG0', 'B006K2ZZ7K'), ('B0001PB9FE', 'B0001PB9FY'),
        ]).collect()

        ### Act
        actual = get_all_purchased_products_pairs(self.spark, self.input)


        ### Assert
        self.assertEqual(len(expected), len(actual))

        for expected_item in expected:
            if expected_item in actual:
                actual.remove(expected_item)

        self.assertEqual(0, len(actual))

    def tearDown(self):
        self.spark.stop()


if __name__ == '__main__':
    unittest.main()
