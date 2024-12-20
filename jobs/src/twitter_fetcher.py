from src.interface import FetchStrategy
import pandas as pd
import datetime
import uuid
# We wont be using the real twitter api here,but mock streaming data from a csv
# This is to provide an illustration of how we could have multiple data sources.
from src.proj_logger import logger

class TwitterFetcher(FetchStrategy):
    def __init__(self, df:pd.DataFrame):
        self.df = df.sample(frac =1) # this shuffles the data
        
    def fetch_data(self):
        while True:   
            for index, row in self.df.iterrows():
                yield {
                    'id' : str(uuid.uuid4()),
                    'username': row['Username'],
                    'comment' : row['Text'],
                    'time' : datetime.datetime.now().timestamp()
                }