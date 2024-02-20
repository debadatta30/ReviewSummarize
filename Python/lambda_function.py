import json
import boto3
import logging
import os
from jinja2 import Template

# Set up the  logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Env variables from  CFN 
bucket_name = os.environ['SOURCEBUCKET']
key = os.environ['SOURCEFILE']
keyReview = os.environ['SOURCEREVIEW']

s3_client = boto3.client('s3')
bedrock_runtime = boto3.client('bedrock-runtime', 'us-east-1')

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    try:
        review_content = ""
        response = s3_client.get_object(Bucket=bucket_name, Key=keyReview)
        review_content = response['Body'].read().decode('utf-8')
        prompt_content = ""
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        prompt_content = response['Body'].read().decode('utf-8')
        data = {
            'feedback' : review_content
        }
        template = Template(prompt_content)
        prompt = template.render(data)
        print(prompt)

        config = {
            "modelId": "amazon.titan-text-express-v1",
            "contentType": "application/json",
            "accept": "*/*",
            "body": json.dumps(
                {
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": 500,
                        "temperature": 0,
                        "topP": 0.9
                    }
                }
            )
        }
        response = bedrock_runtime.invoke_model(**config)
        summarize = json.loads(response.get('body').read()).get('results')[0].get('outputText')   
        Keyresult = key + 'results.txt'
        s3_client.put_object(
            Bucket=bucket_name,
            Key=Keyresult,
            Body=summarize,
            ContentType='text/plain'
        ) 
        logger.info(response)
    except Exception as e:
        #print(e)
        logger.info(e)
        raise e
        
        