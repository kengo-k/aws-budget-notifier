import json
import boto3

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