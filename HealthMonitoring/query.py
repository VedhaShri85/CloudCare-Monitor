import boto3
import json
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ.get("VITALS_TABLE", "PatientVitals"))

def lambda_handler(event, context):
    patient_id = event.get("queryStringParameters", {}).get("patientId", "1001")
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key("patientId").eq(patient_id)
    )
    return {
        "statusCode": 200,
        "body": json.dumps(response["Items"])
    }
