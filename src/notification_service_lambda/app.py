import json

def lambda_handler(event, context):

    for record in event["Records"]:

        message = record["Sns"]["Message"]

        print("Notification received:")
        print(message)

    return {
        "statusCode": 200,
        "body": "Notification processed"
    }