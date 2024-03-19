import os
import datetime
import json
import requests
import dpath
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
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )

    result = []
    total_cost = 0

    for item in monthly_cost['ResultsByTime'][0]['Groups']:
        service_name = item['Keys'][0]
        cost = float(item['Metrics']['UnblendedCost']['Amount'])
        result.append((service_name, cost))
        total_cost += cost

    result.sort(key=lambda x: x[1], reverse=True)
    result_with_percentage = [(service_name, cost, cost / total_cost * 100) for service_name, cost in result]
    result_with_percentage.append(('Total', total_cost, 100))

    return result_with_percentage

def notify_slack(message):
    webhook_url = get=get_parameter('BUDGET_NOTIFIER_SLACK_WEBHOOK_URL')
    data = {'text': message}
    response = requests.post(webhook_url, json=data)
    
    return response

def main(event, context):

    now = datetime.datetime.now()
    year = now.year
    month = now.month

    monthly_cost = get_monthly_cost(year, month)
    results = dpath.get(monthly_cost, 'ResultsByTime')
    result = results[0]
    value = dpath.get(result, 'Total/UnblendedCost/Amount')
    value = round(float(value), 2)
    value = f"Cumulative billing amount for {year}/{month}: ${value}"

    notify_slack(value)

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
    event = {}
    context = None
    main(event, context)