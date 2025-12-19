import boto3
import json
import time
import random

lambda_client = boto3.client("lambda", region_name="ap-south-1")

def simulate_vitals():
    return {
        "patientId": random.randint(1000, 1010),
        "vitals": {
            "heartRate": random.randint(60, 140),
            "spo2": random.randint(85, 100),
            "temperature": round(random.uniform(36.0, 39.0), 1)
        }
    }

if __name__ == "__main__":
    while True:
        payload = simulate_vitals()
        response = lambda_client.invoke(
            FunctionName="IngestVitals",
            InvocationType="RequestResponse",
            Payload=json.dumps(payload)
        )
        print("Sent:", payload)
        print("Response:", response['Payload'].read().decode())
        time.sleep(5)
