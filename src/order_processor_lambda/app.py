import json
import os
import psycopg2
import boto3

# LocalStack endpoint
AWS_ENDPOINT = os.getenv("AWS_ENDPOINT", "http://localhost:4566")

# SNS topic ARN
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:000000000000:OrderStatusNotifications"


def get_db():
    return psycopg2.connect(
        host="localhost",
        database="orders",
        user="admin",
        password="password",
        port=5432
    )


def lambda_handler(event, context):

    conn = get_db()
    cur = conn.cursor()

    sns = boto3.client(
        "sns",
        endpoint_url=AWS_ENDPOINT,
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test"
    )

    for record in event["Records"]:

        body = json.loads(record["body"])
        order_id = body["order_id"]

        # Update order status
        cur.execute(
            "UPDATE orders SET status=%s, updated_at=NOW() WHERE id=%s",
            ("COMPLETED", order_id)
        )

        # Send notification
        message = f"Order {order_id} has been completed."

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="Order Update"
        )

    conn.commit()

    cur.close()
    conn.close()

    return {
        "statusCode": 200,
        "body": "Order processed successfully"
    }