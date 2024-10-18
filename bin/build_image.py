import json
import requests

def get_chart(labels, updated_check, last_check):
    updated_check = [0 if updated is None else updated for updated in updated_check]
    last_check = [0 if last is None else last for last in last_check]
    # Calculate the difference between updated_check and last_check
    difference = [updated - last for updated, last in zip(updated_check, last_check)]
    updated_check = difference
    # Config can be set as a string or as a nested dict
    config = {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "label": "Last Check",
                    "backgroundColor": "rgb(191, 219, 255)",
                    "data": last_check,
                },
                {
                    "label": "Current",
                    "backgroundColor": "rgb(54, 162, 235)",
                    "data": updated_check,
                }
            ]
        },
        "options": {
            "title": {
            "display": True,
            "text": "macOS versions overview",
            },
            "scales": {
            "xAxes": [
                {
                "stacked": True,
                },
            ],
            "yAxes": [
                {
                "stacked": True,
                },
            ],
            },
        },
    }

    params = {
        'chart': json.dumps(config),
        'width': 600,
        'height': 400,
    }
    resp = requests.post('https://quickchart.io/chart/create', json=params)
    parsed = json.loads(resp.text)
    print(parsed['url'])
    return parsed['url']