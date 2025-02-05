from .interface import FetchStrategy
import praw
import datetime
import json
from dotenv import load_dotenv
import os
from typing import TypedDict, Generator

class RedditPost(TypedDict):
    title: str
    id: str
    url: str
    created_utc: float
    selftext: str
    now_time: float

class RedditFetcher(FetchStrategy):
    def __init__(self, client_id:str, client_secret:str, user_agent:str, subreddit:str):
        self.reddit = praw.Reddit(
            client_id = client_id,
            client_secret = client_secret,
            user_agent = user_agent
        )
        self.subreddit = subreddit


    def fetch_data(self)->Generator[RedditPost, None, None]:
        subreddit = self.reddit.subreddit(self.subreddit)
        for submission in subreddit.stream.submissions(skip_existing = True):
            yield{
                'title':submission.title,
                'id':submission.id,
                'url':submission.url,
                'created_utc':submission.created_utc,
                'selftext':submission.selftext,
                'now_time':datetime.datetime.now().timestamp()
            }