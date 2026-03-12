import json
import uuid
import boto3
import psycopg2

# SQS client (LocalStack)
sqs = boto3.client(
    "sqs",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

QUEUE_URL = "http://localhost:4566/000000000000/OrderProcessingQueue"


def get_db():
    return psycopg2.connect(
        host="localhost",
        database="orders",
        user="admin",
        password="password",
        port=5432
    )


def lambda_handler(event, context):

    body = json.loads(event["body"])

    user_id = body.get("user_id")
    product_id = body.get("product_id")
    quantity = body.get("quantity")

    if not user_id or not product_id or not quantity:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid input"})
        }

    order_id = str(uuid.uuid4())

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO orders (id,user_id,product_id,quantity,status) VALUES (%s,%s,%s,%s,%s)",
        (order_id, user_id, product_id, quantity, "PENDING")
    )

    conn.commit()

    # Send message to SQS
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps({"order_id": order_id})
    )

    return {
        "statusCode": 202,
        "body": json.dumps({"order_id": order_id})
    }