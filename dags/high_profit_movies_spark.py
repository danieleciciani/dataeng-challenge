import sys
import os
import logging
from pyspark.sql import SparkSession
from common.utils import get_imdb_data, get_wiki_data, write_output, get_high_profit_movies

"""
sys.argv[1] -> path imdb data
sys.argv[2] -> path wiki data
sys.argv[3] -> full output filename
"""

spark = SparkSession \
    .builder \
    .appName("truefilm_pipe") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel('WARN')

# reading imdb_data data
df_imdb = get_imdb_data(sys.argv[1])

# get high profit movies calculating ration between revenue to budget
df_imdb = get_high_profit_movies(df_imdb)
                 
# read wiki data
df_wiki = get_wiki_data(sys.argv[2])

# left join df_imdb with df_wiki
df_joined = df_imdb.join(df_wiki,  ['title'], "left")

# write results to output location in alphabetic order
write_output(df_joined, sys.argv[3])


spark.stop()