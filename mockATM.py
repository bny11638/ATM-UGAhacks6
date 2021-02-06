#This will be the mock atm for making transactions with that will be run on the raspberry PI
import json
import requests

runFirst = {} # holds access token


def authenticate():
    url = "http://ncrdev-dev.apigee.net/digitalbanking/oauth2/v1/token"
    payload='grant_type=password&username=HACKATHONUSER217&password=uga123'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'transactionId': '61ba5406-fad6-4ae5-ac2b-477b55b6b2f6',
    'institutionId': '00516',
    'Accept': 'application/json',
    'Authorization': 'Basic YUpaR3l1TmhIMDc4MWhYZ3pGWFl6WGp1ZlRKUEZrVjI6R3U0Y3NUV0N5UzBZVVFWTw=='
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    #print(response.text)
    #runFirst = json.dumps(response.text)
    #runFirst = json.loads(runFirst)
    runFirst = response.json() 
    #access_token, expires_in, refresh_token, refresh_token_expires_in, token_type
    print(runFirst["access_token"])



