#This will be the mock atm for making transactions with that will be run on the raspberry PI
import json
import requests
from ATM import qrReader


#authData = {} # holds access token
#username = "HACKATHONUSER217"
#password = "uga123"
#OUR TARGET ACCOUNT 
#targetAccount = "HACKATHONUSER218"
#password = "uga123"
transactionId = '61ba5406-fad6-4ae5-ac2b-477b55b6b2f6'

class Account:
    def __init__(self,id,institutionUserid,institutionId,accountNumber,availableBalance,username,access_token,institutionCustomerId):
        self.id = id
        self.i_u_d = institutionUserid
        self.institutionId = institutionId
        self.accountNumber = accountNumber
        self.availableBalance = availableBalance
        self.username = username
        self.access_token = access_token
        self.customer = institutionCustomerId

def getAuthenticate(username, password):
    url = "http://ncrdev-dev.apigee.net/digitalbanking/oauth2/v1/token"
    payload='grant_type=password&username='+username+'&password=' + password
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'transactionId': transactionId,
    'institutionId': '00516',
    'Accept': 'application/json',
    'Authorization': 'Basic YUpaR3l1TmhIMDc4MWhYZ3pGWFl6WGp1ZlRKUEZrVjI6R3U0Y3NUV0N5UzBZVVFWTw=='
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    #print(response.text)
    #runFirst = json.dumps(response.text)
    #runFirst = json.loads(runFirst)
    emptyDict = response.json() 
    return emptyDict
    #access_token, expires_in, refresh_token, refresh_token_expires_in, token_type

def getAccounts(authData):
    url = "http://ncrdev-dev.apigee.net/digitalbanking/db-accounts/v1/accounts"
    payload={}
    headers = {
    'Authorization': 'Bearer ' + authData['access_token'],
    'transactionId': transactionId,
    'Accept': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

#I NEED TO USE INSTITUTION CUSTOMER ID TO ALLOW TRANSFERS
def createTransfer(acctOne, recipient):
    url = "http://ncrdev-dev.apigee.net/digitalbanking/db-transfers/v1/transfers"
    payload="{\n    \"fromAccountHolderId\": \"" + acctOne.customer + "\",\n    \"fromAccountId\": \"rf5ao6Qclwsth9OfOvUb-EeV1m2BfmTzUEALGLQ3ehU\",\n    \"toAccountHolderId\": \"" + recipient + "\",\n    \"amount\": {\n        \"amount\": 50.0\n    }\n}"
    headers = {
    'Authorization': 'Bearer ' + acctOne.access_token,
    'transactionId': transactionId,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def getChecking(authData):
    url = "http://ncrdev-dev.apigee.net/digitalbanking/db-accounts/v1/accounts/rf5ao6Qclwsth9OfOvUb-EeV1m2BfmTzUEALGLQ3ehU"
    payload={}
    headers = {
    'Authorization': 'Bearer ' + authData['access_token'],
    'transactionId': transactionId,
    'Accept': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

def createRecipient(authData):
    url = "http://ncrdev-dev.apigee.net/digitalbanking/db-recipients/v1/recipients"
    payload="{\n    \"memberNumber\": \"WORLD\",\n    \"accountNumber\": \"00000019022\",\n    \"accountType\": \"CHECKING\",\n    \"passCode\": \"foo\",\n    \"email\": \"di.api.qal1@gmail.com\",\n    \"nickName\": \"buddy\"\n}"
    headers = {
    'transactionId': transactionId,
    'Authorization': 'Bearer ' + authData['access_token'],
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()['Recipients']
def getRecipients():
    url = "http://ncrdev-dev.apigee.net/digitalbanking/db-recipients/v1/recipients"
    headers = {
    'transactionId': transactionId,
    'Authorization': 'Bearer ' + authData['access_token'],
    'Content-Type': 'application/json'
    }
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()['Recipients'][0]['id']

    





#main loop for script
#intializing User Account     def __init__(id,institutionUserid,institutionId,accountNumber,availableBalance,username,access_token):
"""
authData = getAuthenticate("HACKATHONUSER217","uga123")
acctOneData = getChecking(authData)
userAccount = Account(acctOneData['id'],acctOneData['institutionUserId'],acctOneData['institutionId'],acctOneData['accountNumber'],acctOneData['availableBalance'],"HACKATHONUSER217",authData['access_token'],acctOneData['institutionCustomerId'])
#This will act as the outside world/unlimited bank
authData = getAuthenticate("HACKATHONUSER218","uga123")
acctOneData = getChecking(authData)
worldAccount = Account(acctOneData['id'],acctOneData['institutionUserId'],acctOneData['institutionId'],acctOneData['accountNumber'],acctOneData['availableBalance'],"HACKATHONUSER218",authData['access_token'],acctOneData['institutionCustomerId'])
authData['access_token'] = userAccount.access_token
#print(userAccount.username + " " + userAccount.i_u_d + " " + str(userAccount.availableBalance['amount']))
#print(worldAccount.username + " " + worldAccount.i_u_d + " " + str(worldAccount.availableBalance['amount']))
#createRecipient(authData)
#createTransfer(userAccount,getRecipients())
"""
val = input("Welcome to your ATM press any key to continue")
val = input("Are you here to deposit withdraw via QR code? (y/n)") 
if (val == 'y'):
    print("Scan your QR code now:")
    print(qrReader.scanQR())
else():
    print("Have a great day!")





