import os
from typing import Optional, Dict, List
import time
from datetime import datetime

from src.s3_fetcher import S3Fetcher
from src.context import  DataFetcher

from src.proj_logger import logger


from dotenv import load_dotenv
import boto3

import pandas as pd

if __name__ == "__main__":
    load_dotenv()

    MINO_ENDPOINT : str = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
    MINIO_ACCESS_KEY : str = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY : str = os.getenv("MINIO_SECRET_KEY")

    SOURCE_BUCKET : str = "processed-data"
    SOURCE_PREFIX : Optional[str] = "output/json_data"

    current_time = datetime.now()
    timestamp_path = f"year={current_time.strftime('%Y')}/month={current_time.strftime('%m')}/day={current_time.strftime('%d')}/hour={current_time.strftime('%H')}/minute={current_time.strftime('%M')}/second={current_time.strftime('%S')}/ms={current_time.strftime('%f')[:-3]}.csv"
    DESTINATION_BUCKET : str = "processed-data"
    DESTINATION_KEY : str = f"output/aggregated_data/{timestamp_path}"

    s3_client = boto3.client(
        "s3",
        endpoint_url=MINO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY)

    s3_fetcher = DataFetcher(S3Fetcher(s3_client = s3_client,
                           bucket_name = SOURCE_BUCKET,
                           prefix = SOURCE_PREFIX))
    
    output : List[Dict[str, str]] = s3_fetcher.fetch()

    csv_buffer = pd.DataFrame(output).to_csv(index=False).encode()

    s3_client.put_object(
        Bucket=SOURCE_BUCKET,
        Key=DESTINATION_KEY,
        Body=csv_buffer
    )

    logger.info("Stored Data")