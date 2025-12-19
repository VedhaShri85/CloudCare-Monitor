import json
import boto3
import os
from boto3.dynamodb.conditions import Key

# DynamoDB setup
dynamodb = boto3.resource("dynamodb")
table_name = os.environ.get("VITALS_TABLE", "PatientVitals")
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    """
    Lambda entry point for querying patient vitals.
    Expects API Gateway event with query string:
    /query?patientId=1001
    """

    # Extract patientId from query parameters
    patient_id = None
    if isinstance(event, dict):
        params = event.get("queryStringParameters", {})
        if params:
            patient_id = params.get("patientId")

    if not patient_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing patientId"})
        }

    # Query DynamoDB for patient vitals
    response = table.query(
        KeyConditionExpression=Key("patientId").eq(patient_id)
    )

    items = response.get("Items", [])

    return {
        "statusCode": 200,
        "body": json.dumps(items)
    }
