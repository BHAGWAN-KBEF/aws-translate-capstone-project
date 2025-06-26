import json
import boto3
import os
import uuid

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = os.environ['REQUEST_BUCKET']
    object_name = f"web_input_{uuid.uuid4()}.json"

    try:
        url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_name,
                'ContentType': 'application/json'
            },
            ExpiresIn=300  # 5 minutes
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'upload_url': url,
                'file_key': object_name
            }),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            }
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e)),
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            }
        }
