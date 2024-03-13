import json
import pulumi
import pulumi_aws as aws


s3bucket = aws.s3.Bucket("basic-s3-bucket",
                        tags={
                            "Name": "MyS3Bucket",
                            "Environment": "Dev"
                        })

dynamodbTable = aws.dynamodb.Table("basic-dynamodb-table",
                billing_mode="PROVISIONED",
                write_capacity=5,
                read_capacity=5,
                hash_key="objectkey",
                range_key="timestamp",
                attributes=[
                    aws.dynamodb.TableAttributeArgs(
                        name="objectkey",
                        type="S",
                    ),
                    aws.dynamodb.TableAttributeArgs(
                        name="timestamp",
                        type="S",
                    ),
                ],
                tags={
                    "Name": "dynamodb-table-1",
                    "Environment": "Dev"
                })


# An IAM Role for Lambda function
role = aws.iam.Role("role", 
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com",
            },
        }],
    }),
    managed_policy_arns=[aws.iam.ManagedPolicy.AWS_LAMBDA_BASIC_EXECUTION_ROLE])


# Attaching DynamoDB Access policy to role
dynamodbTablePolicy = aws.iam.RolePolicyAttachment("fnDynamodbAccess",
                          role=role.name,
                          policy_arn="arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess")

# Attaching S3ReadOnly policy to role
s3ReadOnlyPolicy = aws.iam.RolePolicyAttachment("s3ReadOnlyAccess",
                                                role=role.name,
                                                policy_arn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")

# A Lambda function to invoke 
fn = aws.lambda_.Function("fn",
    runtime="python3.9",
    handler="handler.handler",
    role=role.arn,
    code=pulumi.FileArchive("./function"),
    environment=aws.lambda_.FunctionEnvironmentArgs(
        variables={
            "TABLE_NAME":dynamodbTable.name
        }))

# Lambda permission to allow S3 to invoke it
lambdaPermission = aws.lambda_.Permission("lambdaPermission",
                                           action="lambda:InvokeFunction",
                                           function=fn.name,
                                           principal="s3.amazonaws.com",
                                           source_arn=s3bucket.arn)

# S3 Bucket Access for Lambda function
s3Event = aws.s3.BucketNotification("s3Event",
                                    bucket=s3bucket.id,
                                    lambda_functions=[aws.s3.BucketNotificationLambdaFunctionArgs(
                                        lambda_function_arn=fn.arn,
                                        events=["s3:ObjectCreated:*"]
                                    )],
                                    opts=pulumi.ResourceOptions(depends_on=[lambdaPermission]))

# The bucket name at which the files will be uploaded.
pulumi.export("bucketName", s3bucket.id)

# The database where writes are performed
pulumi.export("tableName", dynamodbTable.name)

# Exporting Lambda Function ARN and Name Info
pulumi.export("lambdaFunctionArn", fn.arn)
pulumi.export("lambdaFunctionName", fn.name)

