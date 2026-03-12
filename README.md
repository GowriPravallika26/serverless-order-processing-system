AWS Serverless Event-Driven Order Processing System

A serverless event-driven backend system for processing e-commerce orders asynchronously using AWS services.
This project demonstrates how to build a scalable, resilient cloud-native architecture using queues and event notifications instead of traditional synchronous APIs.
The system is designed using microservices principles and event-driven architecture.

Architecture Overview

The system processes orders in the following flow:

Client
   |
   v
API Gateway
   |
   v
OrderCreator Lambda
   |
   | Save Order
   v
PostgreSQL Database
   |
   | Send Message
   v
SQS Queue (OrderProcessingQueue)
   |
   v
OrderProcessor Lambda
   |
   | Update Status
   v
Database
   |
   | Publish Event
   v
SNS Topic (OrderStatusNotifications)
   |
   v
NotificationService Lambda
   |
   v
Notification Logs
Features

• Serverless architecture
• Event-driven order processing
• Asynchronous message handling
• Fault-tolerant design with Dead Letter Queue
• Notification system for order updates
• Local AWS simulation using Docker
• Automated testing support

Technology Stack

Backend Runtime
Python

Cloud Services
AWS Lambda
API Gateway
Amazon SQS
Amazon SNS
Amazon RDS

Local Development
Docker
LocalStack

Testing
Pytest

Database
PostgreSQL

Project Structure
aws-serverless-order-processing-system
│
├── src
│   ├── order_creator_lambda
│   │   ├── app.py
│   │   └── Dockerfile
│   │
│   ├── order_processor_lambda
│   │   ├── app.py
│   │   └── Dockerfile
│   │
│   └── notification_service_lambda
│       ├── app.py
│       └── Dockerfile
│
├── tests
│   ├── test_order_api.py
│   └── test_processing.py
│
├── infrastructure
│   └── serverless.yml
│
├── docker-compose.yml
├── schema.sql
├── requirements.txt
├── .env.example
└── README.md
API Endpoint

Create Order

POST /orders

Request Body

{
  "user_id": "user123",
  "product_id": "product456",
  "quantity": 2
}

Response

202 Accepted
{
  "order_id": "generated-uuid"
}
Database Schema
CREATE TABLE IF NOT EXISTS orders (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    product_id VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL,
    status VARCHAR(50) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Order Processing Workflow

Step 1 – Order Creation

Client sends request to API Gateway.

OrderCreator Lambda

• Validates request
• Generates unique order ID
• Stores order in database with status PENDING
• Sends message to SQS queue

Step 2 – Order Processing

OrderProcessor Lambda consumes messages from the queue.

It then:

• Fetches the order from database
• Simulates processing logic
• Updates order status

Possible statuses:

CONFIRMED
FAILED

Step 3 – Notifications

After processing:

• Lambda publishes message to SNS topic
• NotificationService Lambda receives message
• Logs notification message

Example log:

Order 12345 status updated to CONFIRMED
Local Development Setup

Clone the repository

git clone https://github.com/GowriPravallika26/aws-serverless-order-processing-system.git
cd aws-serverless-order-processing-system

Start Docker services

docker-compose up --build

This starts:

• LocalStack
• PostgreSQL database
• Lambda containers

Configure AWS CLI

Run:

aws configure

Use dummy credentials:

Access Key: test
Secret Key: test
Region: us-east-1
Create AWS Resources in LocalStack

Create SQS queue

aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name OrderProcessingQueue

Create Dead Letter Queue

aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name OrderProcessingDLQ

Create SNS topic

aws --endpoint-url=http://localhost:4566 sns create-topic --name OrderStatusNotifications
Running Tests

Run the test suite:

pytest tests/

Tests verify:

• API request handling
• Database operations
• Queue messaging
• End-to-end order processing

Environment Variables

Example .env.example

DB_HOST=postgres
DB_PORT=5432
DB_NAME=orders
DB_USER=admin
DB_PASSWORD=password

AWS_REGION=us-east-1
SQS_QUEUE=OrderProcessingQueue
SNS_TOPIC=OrderStatusNotifications
Logging

All Lambda functions include structured logging for:

• request tracing
• order lifecycle tracking
• error debugging

Logs help monitor asynchronous workflows across services.


Author

N.Gowri Pravallika
B.Tech Computer Science Engineering