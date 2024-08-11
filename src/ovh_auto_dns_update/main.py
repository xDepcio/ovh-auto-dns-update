'''
First, install the latest release of Python wrapper: $ pip install ovh
'''
import json
import ovh
from dotenv import load_dotenv
import os

load_dotenv()

# Instantiate an OVH Client.
# You can generate new credentials with full access to your account on
# the token creation page (https://api.ovh.com/createToken/index.cgi?GET=/*&PUT=/*&POST=/*&DELETE=/*)
client = ovh.Client(
	endpoint='ovh-eu',               # Endpoint of API OVH (List of available endpoints: https://github.com/ovh/python-ovh#2-configure-your-application)
	application_key=os.getenv('OVH_APPLICATION_KEY'),
	application_secret=os.getenv('OVH_APPLICATION_SECRET'),
	consumer_key=os.getenv('OVH_CONSUMER_KEY'),
)

result = client.get("/domain")

# Pretty print
print(json.dumps(result, indent=4))

result2 = client.get("/domain/zone/adrwal.pl/record/")
print(json.dumps(result2, indent=4))

result3 = client.get("/domain/zone/adrwal.pl/record/5316053875/")
print(json.dumps(result3, indent=4))

# postResult = client.post("/domain/zone/adrwal.pl/record/", target="8.8.8.8", subDomain="olek-test", fieldType='A')

# print(json.dumps(postResult, indent=4))

# refreshResult = client.post("/domain/zone/adrwal.pl/refresh")

# # Pretty print
# print(json.dumps(refreshResult, indent=4))

resultRecords = client.get("/domain/zone/adrwal.pl/record", fieldType='A', subDomain='strapup')

# Pretty print
print(json.dumps(resultRecords, indent=4))
