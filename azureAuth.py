import requests
import json

# Step 1: Obtain an authorization code
# Replace {client_id} with the application's client ID
# Replace {redirect_uri} with the application's registered redirect URI
authorization_url = f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=openid%20offline_access%20https://graph.microsoft.com/.default"

# Step 2: Exchange the authorization code for an access token
# Replace {client_id} with the application's client ID
# Replace {client_secret} with the application's client secret
# Replace {redirect_uri} with the application's registered redirect URI
# Replace {authorization_code} with the authorization code obtained in step 1
token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
data = {
    "client_id": client_id,
    "client_secret": client_secret,
    "redirect_uri": redirect_uri,
    "code": authorization_code,
    "grant_type": "authorization_code"
}
response = requests.post(token_url, data=data)

# Step 3: Use the access token and refresh token to authenticate the user in subsequent requests to Microsoft Graph API
access_token = response.json()["access_token"]
refresh_token = response.json()["refresh_token"]
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Helper function to refresh the access token using the refresh token
def refresh_access_token():
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    response = requests.post(token_url, data=data)
    access_token = response.json()["access_token"]
    return access_token

# Step 4: Make a request to Microsoft Graph API using the access token
graph_url = "https://graph.microsoft.com/v1.0/me"
try:
    response = requests.get(graph_url, headers=headers)
except requests.exceptions.RequestException as e:
    # If the request fails, refresh the access token and retry the request
    access_token = refresh_access_token()
    headers["Authorization"] = f"Bearer {access_token}"
    response = requests.get(graph_url, headers=headers)

# Step 5: Process the response
print(json.dumps(response.json(), indent=2))
