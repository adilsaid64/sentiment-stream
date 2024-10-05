from interface import DataFetcher
import praw
import datetime
import json
from dotenv import load_dotenv
import os

class RedditFetcher(DataFetcher):
    def __init__(self, client_id, client_secret, user_agent, subreddit):
        self.reddit = praw.Reddit(
            client_id = client_id,
            client_secret = client_secret,
            user_agent = user_agent
        )
        print('initiated!')
        self.subreddit = subreddit


    def fetch_data(self):
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


# def test_fetch_data(reddit_fetcher):
#     try:
#         for submission in reddit_fetcher.fetch_data():
#             print(json.dumps(submission, indent=2))
#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":

#     load_dotenv()
#     reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
#     reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
#     reddit_user_agent = os.getenv('REDDIT_USER_AGENT')

#     subreddit = "all"

#     reddit_fetcher = RedditFetcher(reddit_client_id, reddit_client_secret, reddit_user_agent, subreddit)
#     test_fetch_data(reddit_fetcher)