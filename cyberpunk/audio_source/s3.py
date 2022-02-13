
import boto3

def get_buckets():
    s3 = boto3.resource('s3')
    return s3.get_buckets.all()