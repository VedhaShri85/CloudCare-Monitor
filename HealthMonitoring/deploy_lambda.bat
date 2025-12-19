@echo off
REM === Navigate to QueryLambda folder ===
cd /d C:\Projects\HealthMonitoring\QueryLambda

REM === Install dependencies into local folder ===
pip install -r requirements.txt -t .

REM === Zip all files in the folder ===
powershell -command "Compress-Archive -Path * -DestinationPath query_lambda.zip -Force"

REM === Upload to AWS Lambda ===
aws lambda update-function-code --function-name QueryVitals --zip-file fileb://query_lambda.zip

echo Query Lambda deployment complete!
pause
