import json
import boto3
import os

translate = boto3.client('translate')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the S3 bucket and object (file) key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Read the input file from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    data = json.loads(response['Body'].read())

    # Translate each line
    translated_texts = []
    for text in data['text_list']:
        result = translate.translate_text(
            Text=text,
            SourceLanguageCode=data['source_language_code'],
            TargetLanguageCode=data['target_language_code']
        )
        translated_texts.append(result['TranslatedText'])

    # Build output structure
    output = {
        "source": data['source_language_code'],
        "target": data['target_language_code'],
        "original": data['text_list'],
        "translated": translated_texts
    }

    # Save result to response bucket
    output_key = key.replace(".json", "_translated.json")
    response_bucket = os.environ['RESPONSE_BUCKET']
    s3.put_object(Bucket=response_bucket, Key=output_key, Body=json.dumps(output))

    return {
        'statusCode': 200,
        'body': json.dumps(f'Translation saved to {response_bucket}/{output_key}')
    }
