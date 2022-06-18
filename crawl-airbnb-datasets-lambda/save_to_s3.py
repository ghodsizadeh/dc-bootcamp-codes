import boto3
import requests
from botocore.errorfactory import ClientError


def save_file(url: str)-> bool:
    """save file to S3 bucket
    it consider everything after `.com/` as file name
    Args:
        url (str): the url of the file to save

    Returns:
        bool: True if file was saved, False if file exists
    """
    content = requests.get(url).content
    file_name = url.split(".com/")[-1]

    bucket_name = "my-airbnb-csv"

    s3 = boto3.client("s3")

    try:
        s3.head_object(Bucket=bucket_name, Key=file_name)
        return False
    except ClientError:
        # Not found
        pass
    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).put_object(Key=file_name, Body=content)
    return True
