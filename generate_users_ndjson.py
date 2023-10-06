import requests
import ndjson
import argparse
import sys

#argParser = argparse.ArgumentParser()
#argParser.add_argument("-q", "--quantity", help="quantity generated")
#quantity = argParser.quantity
quantity = 10
if len(sys.argv) > 1:
    quantity = int(sys.argv[1])    
URL = "https://randomuser.me/api"
res_list = []
print("Generating users data...")
for _ in range(quantity):
    r = requests.get(url= URL)
    data = r.json()
    details = data['results'][0]
    res_list.append(details)
print("Generated %d users, writing to file..." % (quantity))
with open("users_data.ndjson", "w") as outfile:
    ndjson.dump(res_list, outfile)
print("Done!")
