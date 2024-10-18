import requests
from datetime import datetime
import update_slack, fancy_secret, build_image, jamf_orchestration
import ast

# retrieve JSON data
def retrieve_json_data():
    response = requests.get(url="https://sofafeed.macadmins.io/v1/macos_data_feed.json")
    if response.status_code == 200:
        return response.json()
    else:
        return None

# compare and output information
def compare_and_output(previous_version, data):
    if previous_version is None or data is None:
        print("Unable to retrieve data.")
        return
    latest_os_version = data['OSVersions'][0]
    product_version = latest_os_version['Latest']['ProductVersion']
    if product_version != previous_version:
        latest = latest_os_version['SecurityReleases'][0]
        days_since_last = latest['DaysSincePreviousRelease']
        release_date = latest_os_version['Latest']['ReleaseDate']
        sec_link = latest['SecurityInfo']
        cves_addressed = latest['UniqueCVEsCount']
        cves_listed = latest['CVEs']
        exploited_cves = latest['ActivelyExploitedCVEs']
        release_date = datetime.strptime(release_date, "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y")
        # Extract ProductVersion from each Latest and SecurityReleases object
        product_versions_latest = [entry["Latest"]["ProductVersion"] for entry in data["OSVersions"]]
        print(f"product versions latest: {product_versions_latest}")
        product_versions_security = [release["ProductVersion"] for entry in data["OSVersions"] for release in entry["SecurityReleases"]]
        print(f"product versions security: {product_versions_security}")
        # Combine both lists and remove duplicates
        all_product_versions = list(set(product_versions_latest + product_versions_security))
        print(f"all product versions: {all_product_versions}")
        # Sort the combined list in descending order
        all_product_versions.sort(reverse=True)
        print(f"all product versions sorted descending: {all_product_versions}")
        # Select the 6 latest entries of macOS versions (labels)
        labels = all_product_versions[:6]
        print(f"6 latest entries: {labels}")
        updated_check = jamf_orchestration.orchestrate_jamf_data(labels)
        secret_data = "checkdata"
        previous_data = fancy_secret.handle_secret_manager(secret_data)
        previous_data_str = ast.literal_eval(previous_data)
        previous_data_adjusted = [0] + previous_data_str[:-1]
        chart_url = build_image.get_chart(labels, updated_check, previous_data_adjusted)
        attachments = update_slack.create_message(
            product_version, 
            days_since_last, 
            sec_link, 
            cves_addressed, 
            exploited_cves, 
            cves_listed,
            chart_url
        )
        # Send Slack message
        update_slack.send_message(attachments)
        # Store the new version in Secret Manager
        fancy_secret.add_secret_version("macosversion", product_version)
        fancy_secret.add_secret_version("checkdata", updated_check)
    else:
        print("No new OS version available.")


# Main function
def main(data, context):
    secret_vers = "macosversion"
    previous_version = fancy_secret.handle_secret_manager(secret_vers)
    # Retrieve new version data
    data = retrieve_json_data()
    # Compare and output information
    compare_and_output(previous_version, data)

# Entry point
if __name__ == "__main__":
    main()
