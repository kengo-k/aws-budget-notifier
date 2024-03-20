import os
import datetime
import json
import requests
import boto3


def get_webhook_url():
    key = "BUDGET_NOTIFIER_SLACK_WEBHOOK_URL"
    webhook_url = os.environ.get(key)
    if webhook_url is not None:
        return webhook_url

    ssm_client = boto3.client("ssm")
    response = ssm_client.get_parameter(Name=key, WithDecryption=True)
    webhook_url = response["Parameter"]["Value"]

    return webhook_url


def get_monthly_cost(year, month):
    ce = boto3.client("ce")
    monthly_cost = ce.get_cost_and_usage(
        TimePeriod={
            "Start": f"{year}-{month:02d}-01",
            "End": f"{year}-{month+1:02d}-01" if month < 12 else f"{year+1}-01-01",
        },
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}, {"Type": "DIMENSION", "Key": "RECORD_TYPE"}],
    )

    result = []
    total_cost = 0

    for item in monthly_cost["ResultsByTime"][0]["Groups"]:
        record_type = item["Keys"][1]
        if record_type == "Tax":
            service_name = "Tax"
        else:
            service_name = item["Keys"][0]

        cost = float(item["Metrics"]["UnblendedCost"]["Amount"])
        result.append((service_name, cost))
        total_cost += cost

    services = sorted([item for item in result if item[0] not in ["Tax", "Total"]], key=lambda x: x[1], reverse=True)

    tax_item = next((item for item in result if item[0] == "Tax"), None)
    total_item = ("Total", total_cost)

    sorted_result = services + ([tax_item] if tax_item else []) + [total_item]

    result_with_percentage = [(service_name, cost, cost / total_cost * 100) for service_name, cost in sorted_result]
    return result_with_percentage


def get_report_string(cost_data):
    report = []
    for item in cost_data:
        service_name, cost, percentage = item
        formatted_cost = f"${cost:.2f}"
        formatted_percentage = f"({percentage:.1f}%)"
        report_line = f"{service_name}: {formatted_cost} {formatted_percentage}"
        report.append(report_line)

    return "\n".join(report)


def notify_slack(message):
    webhook_url = get_webhook_url()
    data = {"text": message}
    response = requests.post(webhook_url, json=data)

    return response


def main(event, context):

    now = datetime.datetime.now()
    year = now.year
    month = now.month

    monthly_cost = get_monthly_cost(year, month)
    report_string = get_report_string(monthly_cost)

    notify_slack(report_string)

    body = {"message": "success", "data": monthly_cost}

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


if __name__ == "__main__":
    event = {}
    context = None
    main(event, context)
