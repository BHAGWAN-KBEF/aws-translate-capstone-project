🌍 AWS Translate Capstone Project

A fully serverless, multi-language translation application powered by AWS Translate,Lambda, S3, and API Gateway. Users can submit text from a browser and receive translated results in real time — supporting English, French, Spanish, Chinese, and Swahili.

> 🔗 **Live Demo**: [http://translate-web-kubernetes.s3-website-us-east-1.amazonaws.com](http://translate-web-kubernetes.s3-website-us-east-1.amazonaws.com)

Screenshot
<img width="925" alt="image" src="https://github.com/user-attachments/assets/7c4c1566-50c0-456e-a247-a9534d5f6532" />
<img width="925" alt="image" src="https://github.com/user-attachments/assets/7c4c1566-50c0-456e-a247-a9534d5f6532" />

Features
- 🌐 Translate between English,French, Spanish,Chinese, and Swahili
- 🖥️ Clean, responsive frontend hosted on Amazon S3 Static Website
- 📥 Pre-signed S3 upload via API Gateway + Lambda
- 🔁 Event-driven translation using AWS Lambda + Translate
- 📤 Translated results stored in and fetched from Amazon S3
- 💰 Runs completely within the AWS Free Tier

🧱 Architecture Overview
+---------------------+
\|     Web Browser     |
\|  (index.html/JS UI) |
+----------+----------+
|
v
+----------+----------+
\|  API Gateway (HTTP) |
\|   /getPresignedURL  |
+----------+----------+
|
v
+----------+----------+
\| Lambda: Return pre- |
\| signed URL for S3   |
+----------+----------+
|
v
+----------+----------+
\| Upload input.json to|
\|  S3 Request Bucket   |
+----------+----------+
|
v  (trigger)
+----------+----------+
\| Lambda: Translate   |
\| text, store result  |
\| in S3 Response Bucket|
+----------+----------+
|
v
+----------+----------+
\| JS polls translated |
\| file via S3 public  |
\| URL + displays text |
+---------------------+

📁 Project Structure
aws-translate-capstone/
├── cloudformation/
│   └── infrastructure.yaml         # S3 buckets, IAM roles
│
├── lambda/
│   └── lambda\_function.py          # Main translation handler
│
├── frontend/
│   ├── index.html                  # Web UI
│   └── translate.js                # JS logic for pre-signed URL + polling
│
├── sample\_input.json               # Example input file
├── README.md                       # This file
└── .gitignore                      # Optional

🛠️ Technologies Used

- AWS S3 – static website hosting + file storage
- AWS Lambda – translation logic
- AWS Translate – real-time translation API
- Amazon API Gateway– HTTP API to trigger Lambda
- IAM – permission roles for Translate + S3
- CloudFormation – infrastructure-as-code provisioning
- JavaScript + HTML/CSS – interactive UI

🔧 Setup Instructions

1. Deploy Infrastructure 
   Use cloudformation/infrastructure.yaml via AWS Console or CLI:
   ```bash
   aws cloudformation deploy \
     --template-file infrastructure.yaml \
     --stack-name translate-infra-stack \
     --capabilities CAPABILITY_NAMED_IAM


2.Deploy Lambda Function**

   Zip `lambda/lambda_function.py`
   Create the function via AWS Console or CLI
   Attach IAM role from stack

3. Configure API Gateway
     Create HTTP API
     Integrate with Lambda for pre-signed URL generation
      Enable CORS (POST + OPTIONS)

4. Frontend Upload
  Upload frontend/index.html and translate.js to S3 bucket configured for static hosting
  Set public read permissions + CORS on request/response buckets

5. Test Translation
   Open your S3 static website URL
   Enter text and choose source/target language
    Watch translated result appear

Sample Input Format
```json
{
  "source_language_code": "en",
  "target_language_code": "fr",
  "text_list": ["Hello, how are you?"]
}
```

