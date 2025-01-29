import os
from typing import Optional, Dict, List
import time

from src.s3_fetcher import S3Fetcher
from src.context import  DataFetcher

from dotenv import load_dotenv
import boto3

if __name__ == "__main__":
    load_dotenv()

    MINO_ENDPOINT : str = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
    MINIO_ACCESS_KEY : str = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY : str = os.getenv("MINIO_SECRET_KEY")


    BUCKET_NAME : str = "processed-data"
    PREFIX : Optional[str] = "output/json_data"

    s3_client = boto3.client(
        "s3",
        endpoint_url=MINO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY)
    
    s3_fetcher = DataFetcher(S3Fetcher(s3_client = s3_client,
                           bucket_name = BUCKET_NAME,
                           prefix = PREFIX))
    
    output : List[Dict[str, str]] = s3_fetcher.fetch()


    print(output)
