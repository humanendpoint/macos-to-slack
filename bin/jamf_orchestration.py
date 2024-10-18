import requests
import os
import time

JSS = "https://catawiki.jamfcloud.com"

def get_api_token():
    api_user = os.environ.get("JAMF_USER")
    api_pw = os.environ.get("JAMF_PW")
    jamf_url = JSS + "/api/v1/auth/token"
    headers = {"Accept": "application/json"}
    response = requests.post(url=jamf_url, headers=headers, auth=(api_user, api_pw))
    if response.status_code == 200:
        response_json = response.json()
        access_token = response_json.get("token")
        return access_token
    else:
        raise Exception(f"Failed to get API token. Status code: {response.status_code}")


def create_smart_group(group_name, jamf_token):
    # Get the ID for the new group
    url = f"{JSS}/JSSResource/computergroups"
    headers = {"accept": "application/json", "Authorization": f"Bearer {jamf_token}"}
    response = jamf_comm(url, method="GET", headers=headers)
    if response.status_code == 200:
        data = response.json()
        computer_groups = data.get('computer_groups', [])
        new_group_id = max(group['id'] for group in computer_groups) + 1
    else:
        print(f"Failed to get computer groups: {response.text}")
        return None

    # Create XML for the new group
    xml_template = f"""
    <computer_group>
        <name>{group_name}</name>
        <is_smart>true</is_smart>
        <criteria>
            <criterion>
                <name>Operating System Version</name>
                <priority>0</priority>
                <and_or>and</and_or>
                <search_type>is</search_type>
                <value>{group_name}</value>
                <opening_paren>false</opening_paren>
                <closing_paren>false</closing_paren>
            </criterion>
        </criteria>
    </computer_group>
    """
    # Create the group
    url = f"{JSS}/JSSResource/computergroups/id/{new_group_id}"
    headers = {"Content-Type": "application/xml", "Authorization": f"Bearer {jamf_token}"}
    response = jamf_comm(url, method="POST", headers=headers, data=xml_template)
    if response and response.status_code == 201:
        print(f"Smart group '{group_name}' created successfully.")
        return response
    else:
        print(f"Failed to create smart group '{group_name}': {response.text}")
        return None

def count_computers_in_smart_group(group_name, jamf_token):
    url = f"{JSS}/JSSResource/computergroups/name/{group_name}"
    headers = {"accept": "application/json", "Authorization": f"Bearer {jamf_token}"}
    response = jamf_comm(url, method="GET", headers=headers)
    print(url)
    if response.status_code == 200:
        data = response.json()
        computers = data.get("computer_group", {}).get("computers", [])
        return len(computers)
    else:
        print(f"Testing to create smart group {group_name}")
        time.sleep(2)
        try:
            resp2 = create_smart_group(group_name, jamf_token)
            if resp2.status_code == 200:
                response = jamf_comm(url, method="GET", headers=headers)
                if response.status_code == 200:
                    data = response.text
                    computers = data.get("computer_group", {}).get("computers", [])
                    return len(computers)
        except Exception as e:
            print(f"we got an error: {e}")

def orchestrate_jamf_data(smart_groups):
    jamf_token = get_api_token()
    computer_counts = []

    for group_name in smart_groups:
        count = count_computers_in_smart_group(group_name, jamf_token)
        computer_counts.append(count)

    print(f"compputer counts: {computer_counts}")
    return computer_counts

def jamf_comm(url, method="GET", headers=None, data=None, auth=None):
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, auth=auth)
        elif method == "POST":
            response = requests.post(url, headers=headers, auth=auth, data=data)
        # Add more methods as needed (PUT, DELETE, etc.)
        else:
            raise ValueError("Invalid HTTP method")

        return response
    except Exception as e:
        print(f"Error in API communication: {e}")
        return None