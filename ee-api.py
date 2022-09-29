import requests
from requests.auth import HTTPBasicAuth
import os

uname = str(input('Please provide a username: '))
password = str(input('Please provide a password: '))
akey = str(input('Please provide an API key: '))
url = str(input('Please provide a URL: '))

my_headers = {'content-type': 'application/json', 'Authentication' : akey}

# Authentication

response = requests.post(
    url,
    auth=HTTPBasicAuth(uname, password),
    headers= my_headers
    )

print(response)