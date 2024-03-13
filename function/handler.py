from datetime import datetime
import boto3
import os
import json

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(os.environ['TABLE_NAME'])



def handler(event, context):

	for record in event["Records"]:

		# bucket where files are uploaded.
		bucketname = record["s3"]["bucket"]["name"]


		# object key that identifies the file
		objectkey = record["s3"]["object"]["key"]


		# timestamp of file upload
		uploadtime = record["eventTime"]
		timestamp = datetime.strptime(uploadtime, "%Y-%m-%dT%H:%M:%S.%fZ").isoformat() + "Z"


		# Testing values
		print(f"Processing file upload: {objectkey} from bucket: {bucketname} at {timestamp}")


		# writing to table
		try:
			table.put_item(
						Item={
								"objectkey": objectkey,
							 	"timestamp": timestamp
							})
		except Exception as e:
			print(f"Error writing to Dynamodb: {str(e)}")

	return {
		"statusCode": 200,
		"body": json.dumps({
				"message": "Success"
		})
	}
