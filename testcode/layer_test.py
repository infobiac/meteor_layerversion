import requests
import json
import random
headers = {'Accept':'application/vnd.layer+json; version=1.0'}

n = requests.post('https://api.layer.com/nonces', headers=headers)
dic = json.loads(n.text)
nonce = dic['nonce']
url = "https://boiling-oasis-4564.herokuapp.com/get_layer_ID_token/"
payload = {'nonce':nonce, 'user_id':"2"}
r = requests.post(url, data=payload)
dic = json.loads(r.text)
poo = str(dic['identity_token'])
data = {"identity_token": poo, "app_id": "layer:///apps/staging/9dc748f6-5db2-11e5-9221-83df00004bf8"}
r = requests.post('https://api.layer.com/sessions', headers=headers, json=data)
print r.text