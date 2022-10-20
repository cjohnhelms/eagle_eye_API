import requests
import json
from getpass import getpass

uname = str(input('Please provide a username: '))
pword = str(getpass('Please provide a password: '))
akey = str(getpass('Please provide an API key: '))
subd = str(input('Please provide the sub domain: '))
print('\n')

s = requests.Session()
my_headers = {"Content-Type": "application/json", "Authentication": akey}
my_data = json.dumps({"username":uname, "password":pword})

# Authentication and Authorization

def authenticate():
    global auth_token
    global login

    auth_token = s.post(url='https://login.eagleeyenetworks.com/g/aaa/authenticate', headers=my_headers, data=my_data)
    print(auth_token)

    login = s.post('https://login.eagleeyenetworks.com/g/aaa/authorize', headers=my_headers, data=auth_token)
    print(login)

######################################################################################################################################

# Log in to Sub Account
def switch_account():
    accountList = s.get(url=f'https://{subd}.eagleeyenetworks.com/g/account/list', headers=my_headers)
    print('\n')
    print(accountList)
    if accountList.status_code == 200:
        accnum = str(input('Please input a valid account number: '))
        targetAccount = {'account_id': accnum}
        loginAttempt = s.post(url=f'https://{subd}.eagleeyenetworks.com/g/aaa/switch_account', headers=my_headers, params=targetAccount)
        print('\n')
        print(loginAttempt)
        print('\n')
        if loginAttempt.status_code == 200:
            pass
        else:
            print('Response code was not 200. Verify you are not already in a sub account')

def delete_all_cameras():
    print('This script will delete all cameras on an account. Are you sure you want to do this? Type "Delete All Cameras" to confirm.\n')
    verification = input()
    print('\n')
    if verification == 'Delete All Cameras':
        cameraList = s.get(url=f'http://{subd}.eagleeyenetworks.com/g/device/list', headers={"Authentication": akey}, params={"t": "camera"})
        cameraList = cameraList.json()
        print('\n')
        for i in cameraList:
            result = s.delete(url=f'https://{subd}.eagleeyenetworks.com/g/device', headers=my_headers, params={'id': str(i[1])})
            print(result)
    else:
        print('Verification was not a match. Please try again')

authenticate()
print('\n')
delete_all_cameras()