# Lambda Function for Processing Events with Dynamic Partitioning

## Overview

This AWS Lambda function processes incoming event records, extracts and transforms specific fields, and partitions the data into Amazon S3 buckets based on event types and creation date. It also handles DynamoDB integration to prevent duplicate processing and logs errors for empty event names.

## Prerequisites

- AWS Lambda
- Amazon S3
- Amazon DynamoDB
- AWS SDK for Python (Boto3)

## Environment Variables

- `EVENT_CACHE_TABLE_NAME`: DynamoDB table name for caching events.
- `EVENT_CACHE_TTL_HOURS` : DynamoDB table TTL (Time to live) record in hours

## Functionality

1. **Logging Setup:**
   - Initializes logging for the Lambda function.

2. **AWS SDK Clients Initialization:**
   - Initializes the DynamoDB resource and table.

3. **Event Handling:**
   - Iterates through each record in the incoming event.

4. **Record Processing:**
   - Decodes and parses the base64-encoded JSON payload.
   - Logs the incoming data for debugging purposes.

5. **Field Extraction:**
   - Extracts `event_name` and `created_at`.
   - Converts `created_at` to ISO 8601 format for `created_datetime`.

6. **Unique Key Generation:**
   - Combines `event_uuid`, `event_name`, and `created_at` to create a unique key.

7. **DynamoDB Check and Insert:**
   - Checks if the unique key exists in the DynamoDB table.
   - If not, inserts a new item with a TTL (Time To Live) of 24 hours to avoid duplicate processing.

8. **Error Handling for Empty Event Name:**
   - If `event_name` is empty, logs an error and prepares the record to be saved in the error directory.

9. **Event Name Splitting:**
   - Splits `event_name` to extract `event_type` and `event_subtype`.

10. **Adding New Fields:**
    - Adds `created_datetime`, `event_type`, and `event_subtype` to the data.

11. **Partition Prefix Construction:**
    - Constructs the S3 prefix based on `event_type`, `event_subtype`, and the date.

12. **Record Transformation:**
    - Prepares the transformed record with the new fields and partition metadata.

13. **Duplicate Event Logging:**
    - Logs a message if a duplicate event is detected.

## Return Value

- Returns a dictionary containing the processed records.

## Example Usage

Deploy this Lambda function to process event streams, ensure efficient S3 partitioning, and prevent duplicate event processing using DynamoDB.

**For detailed code logic, please refer to the [Kinesis_firehouse_processing.py](kinesis_firehouse_processing.py)**