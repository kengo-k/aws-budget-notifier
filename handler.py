import os
import json
import requests

import boto3

def get_parameter(key, default_value=None):
    if os.environ.get('ENVIRONMENT') == 'local':
        value = os.environ.get(key, default_value)
    else:
        ssm_client = boto3.client('ssm')
        try:
            response = ssm_client.get_parameter(Name=key, WithDecryption=True)
            value = response['Parameter']['Value']
        except ssm_client.exceptions.ParameterNotFound:
            value = default_value
    
    return value

def get_monthly_cost(year, month):
    ce = boto3.client('ce')
    monthly_cost = ce.get_cost_and_usage(
        TimePeriod={
            'Start': f'{year}-{month:02d}-01',
            'End': f'{year}-{month+1:02d}-01' if month < 12 else f'{year+1}-01-01'
        },
        Granularity='MONTHLY',
        Metrics=['UnblendedCost']
    )
    return monthly_cost



def notify_slack(message):
    webhook_url = get=get_parameter('BUDGET_NOTIFIER_SLACK_WEBHOOK_URL')
    data = {'text': message}
    response = requests.post(webhook_url, json=data)
    
    return response

def main(event, context):

    print('main start')

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

if __name__ == '__main__':
    print(get_monthly_cost(2024, 3))