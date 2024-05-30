import os
import json
import base64
import logging
from datetime import datetime
import time

import boto3

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS SDK Clients for DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get("EVENT_CACHE_TABLE_NAME"))
event_cache_ttl_hours = os.environ.get("EVENT_CACHE_TTL_HOURS")


def lambda_handler(event, context):
    logger.info('Event: %s', json.dumps(event))
    output = []

    for record in event['records']:
        payload = base64.b64decode(record['data']).decode('utf-8')
        data = json.loads(payload)

        # Log the incoming data
        logger.info('Processing record: %s', data)

        # Extract relevant fields
        event_name = data.get('event_name', '')
        created_at = data.get('created_at', 0)
        created_datetime = datetime.utcfromtimestamp(created_at)
        # Extract year, month, and day
        year = created_datetime.year
        month = created_datetime.month
        day = created_datetime.day

        # Create a unique key by combining event_uuid, event_name, and created_at
        unique_key = f"{data.get('event_uuid')}_{event_name}_{created_at}"

        # Check if the unique key exists in the DynamoDB table
        if "Item" not in table.get_item(Key={'id': unique_key}):

            # If the key does not exist, insert a new item with the unique key and
            # set a time-to-live (ttl) attribute to expire after 24 hours
            table.put_item(Item={'id': unique_key, 'ttl': int(time.time() + 86400)})

            # Check if event_name is empty
            if not event_name:
                # Log the error
                logger.error('event_name is empty: %s', data)

                # Construct the error S3 prefix
                error_s3_prefix = f"error/{year}/{month}/{day}/"

                # Prepare the error record
                error_record = {
                    'recordId': record['recordId'],
                    'result': 'Ok',
                    'data': base64.b64encode(json.dumps(data).encode('utf-8')).decode('utf-8'),
                    'metadata': {
                        'partitionKeys': {
                            's3Prefix': error_s3_prefix
                        }
                    }
                }
                output.append(error_record)
                continue

            # Split event_name to get event_type and event_subtype
            event_name_parts = event_name.split(':')
            event_type = event_name_parts[0] if len(event_name_parts) > 0 else 'unknown'
            event_subtype = event_name_parts[1] if len(event_name_parts) > 1 else 'unknown'

            # Add new fields to the data
            data['created_datetime'] = created_datetime
            data['event_type'] = event_type
            data['event_subtype'] = event_subtype

            # Build the partition prefix
            s3_prefix = f"{event_type}/{event_subtype}/{year}/{month}/{day}/"

            # Prepare the transformed record
            transformed_record = {
                'recordId': record['recordId'],
                'result': 'Ok',
                'data': base64.b64encode(json.dumps(data).encode('utf-8')).decode('utf-8'),
                'metadata': {
                    'partitionKeys': {
                        's3Prefix': s3_prefix
                    }
                }
            }
            output.append(transformed_record)
        else:
            logger.info("Duplicate event is recorded : %s ", unique_key)
    return {'records': output}
