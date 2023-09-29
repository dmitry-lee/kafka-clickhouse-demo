import requests
import ndjson

URL = "https://randomuser.me/api"
res_list = []
for _ in range(10):
    r = requests.get(url= URL)
    data = r.json()
    details = data['results'][0]['login']
    res_list.append(details)

with open("users_data.ndjson", "w") as outfile:
    ndjson.dump(res_list, outfile)