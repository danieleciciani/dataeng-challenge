import sys
import os
sys.path.append('/opt/airflow/dags/common/')

from utils import get_imdb_data, get_wiki_data, get_high_profit_movies

import pandas as pd
import pytest

#vars

IMDB_DATA_PATH = '/opt/airflow/data/movies_metadata.csv'
WIKI_DATA_PATH = '/opt/airflow/data/enwiki-latest-abstract.xml.gz'
 
# test if the func get_imdb_data return the expected imdb columns
@pytest.mark.columns_validator
def test_imdb_cols(spark, imdb_cols):
    df = get_imdb_data(IMDB_DATA_PATH)

    assert df.columns == imdb_cols

# test if the func get_wiki_data return the expected wiki columns
@pytest.mark.columns_validator
def test_wiki_cols(spark, wiki_cols):
    df = get_wiki_data(WIKI_DATA_PATH)

    assert df.columns == wiki_cols


# test if the func join of imbd + wiki return the expected columns 
@pytest.mark.columns_validator
def test_high_profit_cols(spark, high_profit_movie_cols):
    df_imdb = get_high_profit_movies(get_imdb_data(IMDB_DATA_PATH))
    df_wiki = get_wiki_data(WIKI_DATA_PATH)
    df_joined = df_imdb.join(df_wiki,  ['title'], "left")

    assert df_joined.columns == high_profit_movie_cols


# test if result contains the most high profit movies
@pytest.mark.data_check
def test_high_profit_movies(spark, high_profit_movies):
    df_imdb = get_high_profit_movies(get_imdb_data(IMDB_DATA_PATH))

    assert set(high_profit_movies).issubset(list(df_imdb.select('title').toPandas()['title']))
