# 🌍 AWS Translate Capstone Project

## 🤔 What is this?

**Simple explanation**: This is a website where you can type text in one language and instantly get it translated to another language - like having Google Translate, but built from scratch using Amazon's cloud services!

**Try it yourself**: Visit the [Live Demo](http://translate-web-kubernetes.s3-website-us-east-1.amazonaws.com) - no signup required!

### How it works (in simple terms):
1. 📝 You type text on a webpage (like "Hello, how are you?")
2. 🌐 You choose what language to translate FROM and TO
3. ⚡ Click "Translate" and wait a few seconds
4. ✨ See your text translated instantly!

### What makes this special?
- 🆓 **Completely Free** - Uses Amazon's free tier, so it costs nothing to run
- 🔒 **Secure** - Your text is safely processed and automatically deleted
- 🌍 **5 Languages** - English, French, Spanish, Chinese, and Swahili
- 📱 **Works Everywhere** - Any device with internet and a web browser

---

## 🔧 Technical Overview

A fully serverless, multi-language translation application powered by AWS Translate, Lambda, S3, and API Gateway. Users can submit text from a browser and receive translated results in real-time, supporting English, French, Spanish, Chinese, and Swahili.

> 🔗 **Live Demo**: [http://translate-web-kubernetes.s3-website-us-east-1.amazonaws.com](http://translate-web-kubernetes.s3-website-us-east-1.amazonaws.com)

## 📸 Screenshot
<img width="925" alt="AWS Translate Application Screenshot" src="https://github.com/user-attachments/assets/7c4c1566-50c0-456e-a247-a9534d5f6532" />

## ✨ Features

- 🌐 **Multi-language Support**: Translate between English, French, Spanish, Chinese, and Swahili
- 🖥️ **Responsive Frontend**: Clean, modern UI hosted on Amazon S3 Static Website
- 📥 **Secure File Upload**: Pre-signed S3 URLs via API Gateway + Lambda
- 🔁 **Event-Driven Processing**: Automatic translation using AWS Lambda + Translate
- 📤 **Real-time Results**: Translated content stored and fetched from Amazon S3
- 💰 **Cost-Effective**: Runs completely within the AWS Free Tier
- ⚡ **Serverless Architecture**: No server management required

## 🧱 Architecture Overview

![AWS Translate Architecture](https://github.com/user-attachments/assets/3136018c-20d8-4714-affa-aa472f74cee8)

### Workflow:
1. User submits text via web interface
2. Frontend requests pre-signed S3 upload URL from API Gateway
3. Lambda generates secure upload URL for request bucket
4. User uploads translation request JSON to S3
5. S3 event triggers translation Lambda function
6. Lambda processes text using AWS Translate service
7. Translated results saved to response S3 bucket
8. Frontend polls and displays translated content

## 📁 Project Structure

<img width="380" alt="Project Structure" src="https://github.com/user-attachments/assets/22da1a02-fb0c-4118-ab7a-bc066a3088a4" />

```
aws-translate-capstone-project/
├── Cloudformation/
│   └── infrastructure.yaml      # AWS infrastructure template
├── frontend/
│   ├── index.html              # Main web interface
│   ├── translate.js            # Frontend JavaScript logic
│   └── generate_presigned_url.py # Pre-signed URL generator
├── lambda/
│   └── lambda_function.py      # Translation processing logic
├── sample_input.json           # Example translation request
└── README.md                   # Project documentation
```

## 🛠️ Technologies Used

### In Simple Terms:
- **Website Hosting** - Amazon stores and serves the webpage
- **Translation Engine** - Amazon's AI translates the text
- **File Storage** - Temporary storage for translation requests
- **Security** - Amazon handles all the security automatically

### Technical Details:
- **AWS S3** – Static website hosting + secure file storage
- **AWS Lambda** – Serverless translation processing
- **AWS Translate** – AI-powered translation service
- **Amazon API Gateway** – RESTful API for Lambda integration
- **AWS IAM** – Security roles and permissions
- **AWS CloudFormation** – Infrastructure as Code (IaC)
- **JavaScript + HTML/CSS** – Interactive web interface

## 🚀 Quick Start

> **👋 New to AWS?** Don't worry! If you're not familiar with cloud services, you can still use this project by visiting the [Live Demo](http://translate-web-kubernetes.s3-website-us-east-1.amazonaws.com) - no setup required!

### For Developers & Cloud Engineers

#### Prerequisites
- AWS CLI configured with appropriate permissions
- AWS account with access to Translate, Lambda, S3, and API Gateway

### 1. Deploy Infrastructure

Deploy the CloudFormation stack to create S3 buckets and IAM roles:

```bash
aws cloudformation deploy \
  --template-file Cloudformation/infrastructure.yaml \
  --stack-name translate-infra-stack \
  --capabilities CAPABILITY_NAMED_IAM
```

### 2. Deploy Lambda Function

**Option A: AWS Console**
1. Zip the `lambda/lambda_function.py` file
2. Create Lambda function in AWS Console
3. Upload the zip file
4. Set environment variable `RESPONSE_BUCKET` to your response bucket name
5. Attach the IAM role created by CloudFormation

**Option B: AWS CLI**
```bash
cd lambda
zip function.zip lambda_function.py
aws lambda create-function \
  --function-name translate-processor \
  --runtime python3.9 \
  --role arn:aws:iam::YOUR-ACCOUNT:role/translate-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip
```

### 3. Configure S3 Event Trigger

Set up S3 to trigger Lambda when files are uploaded to the request bucket:

```bash
aws s3api put-bucket-notification-configuration \
  --bucket translate-request-bucket-YOUR-ACCOUNT \
  --notification-configuration file://s3-event-config.json
```

### 4. Set Up API Gateway

1. Create HTTP API in API Gateway
2. Create route: `POST /getPresignedUploadURL`
3. Integrate with Lambda function for pre-signed URL generation
4. Enable CORS for `POST` and `OPTIONS` methods
5. Deploy API and note the endpoint URL

### 5. Deploy Frontend

1. Update `API_URL` in `frontend/translate.js` with your API Gateway endpoint
2. Upload `frontend/index.html` and `translate.js` to your S3 website bucket
3. Configure S3 bucket for static website hosting
4. Set public read permissions on frontend files

### 6. Configure CORS

Add CORS configuration to both S3 buckets:

```json
{
  "CORSRules": [
    {
      "AllowedHeaders": ["*"],
      "AllowedMethods": ["GET", "PUT", "POST"],
      "AllowedOrigins": ["*"],
      "MaxAgeSeconds": 3000
    }
  ]
}
```

## 📝 Usage

1. Open your S3 static website URL
2. Enter text in the input field
3. Select source and target languages
4. Click "Translate"
5. Wait for the translation to appear

### Sample Input Format

The application processes JSON in this format:

```json
{
  "source_language_code": "en",
  "target_language_code": "fr",
  "text_list": [
    "Hello, how are you?",
    "This is a test using AWS Translate."
  ]
}
```

### Supported Language Codes

| Language | Code |
|----------|------|
| English  | `en` |
| French   | `fr` |
| Spanish  | `es` |
| Chinese  | `zh` |
| Swahili  | `sw` |

## 🔧 Configuration

### Environment Variables

- `RESPONSE_BUCKET`: S3 bucket name for storing translation results

### AWS Permissions Required

- `translate:TranslateText`
- `s3:GetObject` and `s3:PutObject`
- `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`

## 🚨 Troubleshooting

**Translation not appearing?**
- Check CloudWatch logs for Lambda errors
- Verify S3 event triggers are configured
- Ensure CORS is properly set on S3 buckets

**CORS errors?**
- Update CORS configuration on S3 buckets
- Enable CORS on API Gateway

**Lambda timeout?**
- Increase Lambda timeout in function configuration
- Check AWS Translate service limits

## 💡 Future Enhancements

- [ ] Add support for file uploads (PDF, DOCX)
- [ ] Implement user authentication
- [ ] Add translation history
- [ ] Support for additional languages
- [ ] Real-time translation streaming
- [ ] Mobile app version

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Built with ❤️ using AWS Serverless Technologies**

