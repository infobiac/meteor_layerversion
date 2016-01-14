import requests
import json

headers = {'Accept':'application/vnd.layer+json; version=1.0', 'Authorization':'cNJ1Y3WPec2mYhTT5m71PVh2-k9aVYamu3kRzjL0h7nqQrQEI5B0gDUVaKwD1lXZuh45TgQ1A2jqaKBOZVe3Cw.8-4'}

payload = {"participants":["6.04139471302", "2"], "distinct": True}
r = requests.post('https://api.layer.com/conversations', headers=headers, json=payload)
print r.text