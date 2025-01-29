import os
from typing import Optional, Dict, List
import time

from s3_fetcher import S3Fetcher
from context import  DataFetcher

from dotenv import load_dotenv
import boto3

if __name__ == "__main__":
    load_dotenv()

    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")


    BUCKET_NAME : str = ""
    PREFIX : Optional[str] = None

    s3_client = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY)
    
    s3_fetcher = DataFetcher(S3Fetcher(s3_client = s3_client,
                           bucket_name = BUCKET_NAME,
                           prefix = PREFIX))
    
    output : List[Dict[str, str]] = s3_fetcher.fetch()


