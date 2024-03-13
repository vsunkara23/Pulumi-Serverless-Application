# Pulumi-Serverless-Application
Using Pulumi, created and deployed a serverless application that processes uploads to a storage bucket and builds an index of the files in a database table.

The application was initialized with a 'Dev' stack using the default Pulumi project template for serverless applications. 

<br>

### Testing:

<br>

#### Lambda Function Testing

The Lambda function was tested by mocking an S3 event with the following JSON structure:

LambdaEventTestJSON.txt (/LambdaFuncTest/LambdaEventTestJSON.txt)



CloudWatch Log
![lambdaFunctionTest](https://github.com/vsunkara23/Pulumi-Serverless-Application/assets/43553784/95d4b2d7-b281-48ec-91f9-e9059328967b)


<br>

#### Files Uploaded to S3 bucket:

Files were uploaded to the S3 bucket to trigger the Lambda function and verify its operation:

1) city.jpg

CloudWatch Log

![pictureUploadTest](https://github.com/vsunkara23/Pulumi-Serverless-Application/assets/43553784/28b5c06b-f455-40a0-a130-0ff33d7925c4)

<br>


2) hello.txt

CloudWatch Log

![textfileUploadTest](https://github.com/vsunkara23/Pulumi-Serverless-Application/assets/43553784/f77388a8-1b43-4e0c-b13e-3d8b6f7c7901)



<br>
<br>

#### Database Writes

Mocked event and file uploads resulted in corresponding writes to the DynamoDB table.

![DatabaseWrite](https://github.com/vsunkara23/Pulumi-Serverless-Application/assets/43553784/ce71776a-ff67-4e4a-b841-ec9d57606514)


