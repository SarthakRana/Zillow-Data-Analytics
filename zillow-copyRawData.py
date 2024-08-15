import json
import boto3

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    target_bucket = 'zillow-intermediate-bucket'
    copy_source = {'Bucket': source_bucket, 'Key': object_key}
    
    waiter = s3_client.get_waiter('object_exists')
    # a waiter waits for file to be completed loaded on s3 before doing any operations on it coz a file may be big in size and lambda might get triggered on incomplete file
    waiter.wait(Bucket=source_bucket, Key=object_key)
    s3_client.copy_object(Bucket=target_bucket, Key=object_key, CopySource=copy_source)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
