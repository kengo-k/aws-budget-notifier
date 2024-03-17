import json
import boto3


def main(event, context):

    print('main start')

    s3 = boto3.client('s3')
    buckets = s3.list_buckets()

    # バケット名を表示
    for bucket in buckets['Buckets']:
        print(bucket['Name'])

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