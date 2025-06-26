import json           # For reading and writing JSON
import boto3          # AWS SDK for Python
import uuid           # For unique filenames
from botocore.config import Config  # Needed for Transfer Acceleration

def translate_file(input_file, request_bucket, response_bucket):
    # Step 1: Load input JSON
    with open(input_file) as f:
        data = json.load(f)

    # Step 2: Create AWS clients with Transfer Acceleration enabled
    translate = boto3.client('translate')
    s3 = boto3.client('s3', config=Config(s3={'use_accelerate_endpoint': True}))

    # Step 3: Translate each string
    translated_texts = []
    for text in data['text_list']:
        result = translate.translate_text(
            Text=text,
            SourceLanguageCode=data['source_language_code'],
            TargetLanguageCode=data['target_language_code']
        )
        translated_texts.append(result['TranslatedText'])

    # Step 4: Prepare translated output
    output = {
        "source": data['source_language_code'],
        "target": data['target_language_code'],
        "original": data['text_list'],
        "translated": translated_texts
    }

    # Step 5: Save to local file
    output_file = f"translated_{uuid.uuid4()}.json"
    with open(output_file, 'w') as f:
        json.dump(output, f)

    # Step 6: Upload translated file to S3 response bucket
    s3.upload_file(output_file, response_bucket, output_file)
    print(f"✅ Translated output uploaded to S3 bucket: {response_bucket}/{output_file}")

# Replace with your updated Transfer Acceleration-enabled bucket names
request_bucket = "translate-request-bucket-311141533760"
response_bucket = "translate-response-bucket-311141533760"

# Call the function with your input file
translate_file("sample_input.json", request_bucket, response_bucket)
