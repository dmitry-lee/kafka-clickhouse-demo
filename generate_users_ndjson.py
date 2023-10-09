import requests
import ndjson
import argparse
import sys


quantity = 10
if len(sys.argv) > 1:
    quantity = int(sys.argv[1])    
URL = "https://randomuser.me/api/?results={}".format(quantity)
print("Generating users data...")
r = requests.get(url= URL)
data = r.json()['results']
print("Generated %d users, writing to file..." % (quantity))
with open("users_data.ndjson", "w") as outfile:
    ndjson.dump(data, outfile)
print("Done!")
