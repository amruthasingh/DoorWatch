import json
import boto3
import datetime
import time
import subprocess
def lambda_handler(event, context):

    s3 = boto3.client('s3')
    
    bucket_name = 'test-sort'
    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
    
    objs = s3.list_objects_v2(Bucket=bucket_name)['Contents']
    val = [obj['Key'] for obj in sorted(objs, key=get_last_modified, reverse=True)]
    
    bucket_location = boto3.client('s3').get_bucket_location(Bucket=bucket_name)
    
    object_url = "https://s3.amazonaws.com/{0}/{1}".format(bucket_name, val[0])
    print object_url  
    string = '<img src="'+object_url+'">'
    encoded_string = string.encode("utf-8")

    bucket_name = "test-sort"
    file_name = "index.html"
    s3_path = file_name

    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Done!')
    }
