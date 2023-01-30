import os
import msal
import requests

AUTHORITY = "https://login.microsoftonline.com/{}".format(os.environ['TENANT_ID'])
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
RESOURCE = os.environ['RESOURCE_ID']

app = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)

result = app.acquire_token_for_client(scopes=[RESOURCE])

access_token = result.get("access_token")
refresh_token = result.get("refresh_token")

headers = {"Authorization": "Bearer " + access_token}
response = requests.get("https://your_resource_endpoint", headers=headers)

print(response.text)

# Check if the access token has expired
if response.status_code == 401:
    result = app.acquire_token_by_refresh_token(refresh_token, scopes=[RESOURCE])
    access_token = result.get("access_token")
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get("https://your_resource_endpoint", headers=headers)
    print(response.text)
