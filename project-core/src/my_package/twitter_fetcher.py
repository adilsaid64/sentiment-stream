# We wont be using the real twitter api here,but mock streaming data from a csv
# This is to provide an illustration of how we could have multiple data sources.

from src.my_package.interface import FetchStrategy
from src.my_package.proj_logger import logger

import pandas as pd
import datetime
import uuid
from typing import TypedDict, Generator

class TwitterPost(TypedDict):
    id: str
    username: str
    comment: str
    time: float

class TwitterFetcher(FetchStrategy):
    def __init__(self, df:pd.DataFrame):
        self.df : pd.DataFrame = df.sample(frac =1) # this shuffles the data
        
    def fetch_data(self)->Generator[TwitterPost, None, None]:
        while True:   
            for index, row in self.df.iterrows():
                yield {
                    'id' : str(uuid.uuid4()),
                    'username': row['Username'],
                    'comment' : row['Text'],
                    'time' : datetime.datetime.now().timestamp()
                }