from src.interface import FetchStrategy
import boto3
from botocore.client import BaseClient
import json

from typing import Optional, Dict, List

class S3Fetcher(FetchStrategy):
    def __init__(self, bucket_name: str, s3_client: BaseClient, prefix: Optional[str] = None):
        self._s3_client : BaseClient = s3_client
        self.bucket_name: str = bucket_name
        self.prefix: Optional[str] = prefix

    def fetch_data(self)->List[Dict[str, str]]:
        objects : List[Dict[str, str]] = []
        if self.prefix:
            response = self._s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=self.prefix)
        else:
            response = self._s3_client.list_objects_v2(Bucket=self.bucket_name)
        
        if "Contents" not in response: # empty resonse
            return objects
        
        for obj in response.get('Contents', []):
            key : str = obj['Key']
            file_obj = self._s3_client.get_object(Bucket=self.bucket_name, Key=key)
            file_content = file_obj['Body'].read().decode('utf-8')
            objects.append(json.loads(file_content))
            
        return objects
    