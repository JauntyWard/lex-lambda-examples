#!/usr/bin/python

import json
import boto3

FAIL_STREAM = "failed_requests"
OK_STREAM = "fulfilled_requests"

def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response

def handle_feature(event):
    service_name = event["currentIntent"]["slots"]["ServiceName"]
    feature = event["currentIntent"]["slots"]["feature"]
    
    if service_name == "S3" or service_name == "s3":
        if feature == "cross region replication":
            message = "Yes! To activate this feature, you add a replication configuration to your source bucket."
        elif feature == "web hosting" or feature == "hosting":
            message = "Yes! To host a static website, you configure an Amazon S3 bucket for website hosting, and then upload your website content to the bucket."
        else:
            message = "Sorry, I don't know about that feature. I'll make a note and get back to you."
    else:
        message = "Sorry, I don't know about that feature yet. I'll make a note and get back to you."
        firehose_client = boto3.client('firehose', region_name='us-east-1')
    
        entry = "{},{},{},{}\n".format(service_name, USER, EMAIL, feature)

        firehose_client.put_record(
            DeliveryStreamName=FAIL_STREAM,
            Record={
            'Data': entry
            }
        )
        
    session_attributes = {}
    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': message
        }
    )
def handle_service(event):
    service_name = event["currentIntent"]["slots"]["ServiceName"]
    
    if service_name == "S3" or service_name == "s3":
        message = "I see you're in {}. In the {} Region the S3 pricing starts at $0.025 per GB for the first 50 TB and decreases with further usage. There is an additional cost of $0.0055 per 1,000 requests and a cost of $0.090 per per GB of data out from S3 to the internet. "
    elif service_name == "ec2" or service_name == "EC2" or service_name == "Ec2":
        message = "EC2 pricing is based around the instance type you chose. The chepeast instance type: t2.nano starts at $0.0065 per hour."
    else:
        message = "Sorry, I don't know about that service yet. I'll make a note and get back to you."
        firehose_client = boto3.client('firehose', region_name='us-east-1')
    
        entry = "{},{},{},{}\n".format(service_name, USER_NAME, EMAIL, "pricing")
        
        firehose_client.put_record(
            DeliveryStreamName=FAIL_STREAM,
            Record={
            'Data': entry
            }
        )
        
    session_attributes = {}
    
  
    return close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': message
        }
    )


def lambda_handler(event, context):
    if event["currentIntent"]["name"] == "getPricing":
        return handle_service(event)

    if event["currentIntent"]["name"] == "getFeature":
        return handle_feature(event)
