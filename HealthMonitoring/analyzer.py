import boto3
import json
from datetime import datetime

# SNS client
sns = boto3.client('sns')
TOPIC_ARN = 'arn:aws:sns:ap-south-1:189671594078:HealthAlerts'  # Your actual topic ARN

def publish_alert(patient_id, department, measure, value, reason):
    alert = {
        "patientId": patient_id,
        "department": department,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "measure": measure,
        "value": value,
        "reason": reason,
        "context": { "recent": [value] }
    }

    sns.publish(
        TopicArn=TOPIC_ARN,
        Subject=f"Health Alert - {patient_id} ({department})",
        Message=json.dumps(alert)
    )

def lambda_handler(event, context):
    for record in event['Records']:
        payload = json.loads(record['body']) if 'body' in record else json.loads(record['Sns']['Message'])

        patient_id = payload.get('patientId')
        department = payload.get('department')
        heart_rate = payload.get('heartRate')
        spo2 = payload.get('spo2')
        temperature = payload.get('temperature')

        # Threshold checks
        if spo2 is not None and spo2 < 90:
            publish_alert(patient_id, department, "spo2", spo2, "Low SpO2 threshold")

        if heart_rate is not None and heart_rate > 120:
            publish_alert(patient_id, department, "heartRate", heart_rate, "High heart rate")

        if temperature is not None and temperature > 39:
            publish_alert(patient_id, department, "temperature", temperature, "High temperature")

    return {
        'statusCode': 200,
        'body': json.dumps('Analyzer completed.')
    }
