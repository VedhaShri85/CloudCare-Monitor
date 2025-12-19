import boto3
from datetime import datetime, timedelta, timezone
import random

dynamodb = boto3.client('dynamodb', region_name='ap-south-1')

print("Starting patient insert...")

# --- Part 1: Baseline patients with slight variation ---
patients = [
    ("Cardiology","P0001",80,98,36.7),
    ("ICU","P0101",120,88,38.5),
    ("General","P1001",75,97,36.5),
    ("Pediatrics","P2001",92,99,37.1),
    # ... keep your full list here ...
]

for dept, pid, hr, spo2, temp in patients:
    base_time = datetime.now(timezone.utc)
    for j in range(6):  # 6 readings, 10 min apart
        ts = (base_time + timedelta(minutes=10*j)).isoformat()
        hr_val = hr + random.randint(-3, 3)
        spo2_val = spo2 + random.randint(-1, 1)
        temp_val = round(temp + random.uniform(-0.2, 0.2), 1)

        dynamodb.put_item(
            TableName='Vitals',
            Item={
                'patientId': {'S': pid},
                'ts': {'S': ts},
                'department': {'S': dept},
                'heartRate': {'N': str(hr_val)},
                'spo2': {'N': str(spo2_val)},
                'temperature': {'N': str(temp_val)}
            }
        )
    print(f"Inserted {pid} ({dept}) with 6 varied readings")

print("✅ Baseline patients inserted with variation.")

# --- Part 2: Dynamic time-series with drift + noise ---
print("Starting dynamic simulation insert...")

series_patients = {
    "P1001": {"department": "General", "hr": 78, "spo2": 98, "temp": 36.7},   # Normal
    "P2004": {"department": "Pediatrics", "hr": 100, "spo2": 93, "temp": 37.9}, # Warning
    "P0118": {"department": "ICU", "hr": 126, "spo2": 85, "temp": 39.1}        # Critical
}

start_time = datetime(2025, 12, 15, 8, 0, tzinfo=timezone.utc)
for i in range(48):  # 48 readings, every 15 min (12 hours)
    ts = (start_time + timedelta(minutes=15*i)).isoformat()
    for pid, data in series_patients.items():
        # drift + noise
        hr = data['hr'] + int(i/12) + random.randint(-3, 3)
        spo2 = data['spo2'] + random.randint(-2, 1)
        temp = round(data['temp'] + (i/48)*0.3 + random.uniform(-0.2, 0.2), 1)

        dynamodb.put_item(
            TableName='Vitals',
            Item={
                'patientId': {'S': pid},
                'ts': {'S': ts},
                'department': {'S': data['department']},
                'heartRate': {'N': str(hr)},
                'spo2': {'N': str(spo2)},
                'temperature': {'N': str(temp)}
            }
        )
        print(f"Inserted {pid} at {ts} -> HR:{hr}, SpO2:{spo2}, Temp:{temp}")

print("✅ Simulation complete with realistic variation.")
