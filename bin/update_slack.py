import os
from slack_sdk import WebClient

def create_message(
        product_version, 
        days_since_last, 
        sec_link, 
        cves_addressed, 
        exploited_cves, 
        cves_listed,
        chart_url
    ):
    attachments = [{
        "color": "#36a64f",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":computer: New macOS version released",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn", 
                    "text": f"*Product Version:* {product_version}\n*Days Since Last:* {days_since_last}\n*Sec Info:* <{sec_link}|{sec_link}>\n*Vuln Addressed:* {cves_addressed}"
                }
            }
        ]
    }]
    if exploited_cves:
        cve_links = [f"<https://www.cisa.gov/known-exploited-vulnerabilities-catalog?search_api_fulltext={cve}|{cve}>" for cve in exploited_cves]
        cve_links_text = " ".join(cve_links)
        attachments[0]["blocks"].append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f":fire: *Actively Exploited CVEs:*\n{cve_links_text}"
                }
            ]
        })
    if cves_listed:
        addressed_cve_links = [f"<https://www.cve.org/CVERecord?id={cve}|{cve}>" for cve, status in cves_listed.items() if not status]
        addressed_cves_text = " ".join(addressed_cve_links)
        attachments[0]["blocks"].append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f":check: *Vulnerabilities Addressed:*\n{addressed_cves_text}"
                }
            ]
        })
    if chart_url:
        attachments[0]["blocks"].append({
			"type": "image",
			"image_url": chart_url,
			"alt_text": "macoschart"
		})

    return attachments

# Function to send Slack message
def send_message(attachments):
    client = WebClient(token=os.environ.get("SLACK_TOKEN"))
    client.chat_postMessage(channel=os.environ.get("CHANNEL_ID"), attachments=attachments)