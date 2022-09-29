import requests
from requests.auth import HTTPBasicAuth
import os

uname = str(input('Please provide a username: '))
pword = str(input('Please provide a password: '))
akey = str(input('Please provide an API key: '))
url = str(input('Please provide a URL: '))

my_headers = {'content-type':'application/json', 'Authentication':akey}
my_data = {'username':uname, 'password':pword}

# Authentication
response = requests.post(url, headers=my_headers, data=my_data)

print(response)