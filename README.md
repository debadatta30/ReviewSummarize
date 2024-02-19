# ReviewSummarize
This code read a user feedback file from a S3 and use a predefined prompt template to produce the sentiment of the user feedback ad list of issues and store the output in the same S3 bucket.

The code contains the cloudformation templates which will create the AWS Lambda Function which uses the Bedrock to invoke the Amazon titan-text-express-v1 model. 

The AWS Lambda code is written in Python and the source code is available in the Python folder , this is pacakaged as a zip packagae with the dependency. The code uses boto3 and jinja2 template to create the prompt using the user feedbcak and prompt template.Python folder contain the Lambdacode in the file named lambda_function.py . If you cahnge the source code you can create the zip package , the directory is named python . Navigate to the Project directory cd Python

Create a new directory named package install the avro dependency mkdir package pip install --target ./package avro-python3==1.8.2

Create a .zip file with the installed libraries at the root project cd package zip -r ../my_deployment_package.zip .

Add the lambda_function.py file to the root of the .zip file cd .. zip my_deployment_package.zip lambda_function.py

Upload the .zip package to the S3 Bucket and pass the reference to the cloudformation template , cloudformation template will create the lambda function from the zip pacakge.

Upload Template Files from the cfn folder to S3 Bucket:

aws s3 cp . s3://my-bucket/cfntemplate.yaml/ --recursive

CloudFormation Stack Creation:

aws cloudformation create-stack
--stack-name reviewSummarize
--template-url https://my-bucket.s3.region.amazonaws.com/ReviewSummarize/cfntemplate.yaml
--capabilities CAPABILITY_NAMED_IAM
