import pytest
from pyspark.sql import SparkSession

# Spark session to be used across all of  unit tests.
# Spark session locally with one worker to avoid overhead connections.
@pytest.fixture(scope="session")
def spark():
    spark = (
        SparkSession.builder\
                    .master("local[1]")
                    .getOrCreate()
    )
    return spark


@pytest.fixture()
def imdb_cols():
    return ['id',
            'title',
            'budget',
            'release_date',
            'revenue',
            'vote_average',
            'production_companies',
            ]


@pytest.fixture()
def wiki_cols():
    return ['title',
            'abstract',
            'url']


@pytest.fixture()
def high_profit_movie_cols():
    return ['title',
            'id',
            'budget',
            'release_date',
            'revenue',
            'vote_average',
            'production_companies',
            'ratio_rev_bud',
            'abstract',
            'url'
            ]


# 10 highest profit movies based on online resources
@pytest.fixture()
def high_profit_movies():
       return  ['Paranormal Activity',
                'Mad Max',
                'Super Size Me',
                'The Blair Witch Project',
                'Rocky',
                'Halloween',
                'American Graffiti',
                'Once',
                'Open Water',
                'Gone with the Wind'
                ]