import os
import json
from google.cloud import secretmanager

def add_secret_version(secret_id, payload):
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()
    # Build the resource name of the parent secret.
    parent = f"projects/{os.environ.get('PROJECT_ID')}/secrets/{secret_id}"
    # Check if the payload is a list or a string
    if isinstance(payload, list):
        # Convert the payload list to a JSON string
        payload_json = json.dumps(payload)
        # Convert the JSON string payload into bytes
        payload_bytes = payload_json.encode('UTF-8')
    elif isinstance(payload, str):
        # Convert the string payload into bytes
        payload_bytes = payload.encode('UTF-8')
    else:
        raise ValueError("Payload must be a list or a string.")

    # Add the secret version.
    response = client.add_secret_version(parent=parent, payload={'data': payload_bytes})
    # Print the new secret version name.
    print(f'Added secret version: {response.name}')

    return response

def handle_secret_manager(secret_name):
    client = secretmanager.SecretManagerServiceClient()
    # Retrieve secret from Secret Manager
    secret_name = f"projects/{os.environ.get('PROJECT_ID')}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=secret_name)
    previous_version = response.payload.data.decode("UTF-8")

    return previous_version