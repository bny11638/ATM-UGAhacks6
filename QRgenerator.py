#This will help us generate QR codes for our raspberry pi atm
import qrcode
import json
dictionary = {"username": "HACKATHONUSER220","password":"uga123","transaction":"withdraw","amount":"500"}
json_object = json.dumps(dictionary, indent = 4)   
code = qrcode.make(json_object)
code.save("testQR.png")