import requests
import json

uname = 'cjohnhelms@gmail.com'                        #str(input('Please provide a username: '))
pword = 'bry25kur64Q.4323'                            #str(input('Please provide a password: '))
akey = 'ddf9bfba-4006-11ed-b8a3-5e143c58c6f2'         #str(input('Please provide an API key: '))
subd = 'c013'                                         #str(input('Please provide the sub domain: '))

s = requests.Session()
my_headers = {"Content-Type": "application/json", "Authentication": akey}
my_data = json.dumps({"username":uname, "password":pword})

# Authentication
auth_token = s.post(url='https://login.eagleeyenetworks.com/g/aaa/authenticate', headers=my_headers, data=my_data)
print(auth_token)

# Authorization
login = s.post('https://login.eagleeyenetworks.com/g/aaa/authorize', headers=my_headers, data=auth_token)
print(login)

######################################################################################################################################

# Get List of Bridges
def get_bridges():
    bridgeList = s.get(url=f'http://{subd}.eagleeyenetworks.com/g/device/list', headers={"Authentication": akey})
    print(bridgeList)
    print('\n')
    print(*bridgeList.json(), sep='\n' * 2)

# Get Bridge
def get_bridge():
    pram = input('Please provide a valid ESN: ')
    bridge = s.get(url=f'http://{subd}.eagleeyenetworks.com/g/device', headers={"Authentication": akey}, params={"id": pram})
    print(bridge)
    print('\n')
    print(*bridge.json(), sep='\n' * 2)
    
# Get List of Cameras
def get_cameras():
    cameraList = s.get(url=f'http://{subd}.eagleeyenetworks.com/g/device/list', headers={"Authentication": akey})
    print(cameraList)
    print('\n')
    print(*cameraList.json(), sep='\n' * 2)

# Get Camera
def get_camera():
    pram = input('Please provide a valid ESN: ')
    camera = s.get(url=f'http://{subd}.eagleeyenetworks.com/g/device', headers={"Authentication": akey}, params={"id": pram})
    print(camera)
    print('\n')
    print(*camera.json(), sep='\n' * 2)

#######################################################################################################################################

menu = {}
menu['1']="Get List of Bridges" 
menu['2']="Get Bridge"
menu['3']="Get List of Cameras"
menu['4']="Get Cammera"
menu['5']="Exit"
while True: 
    options=menu.keys()
    print('\n')
    for entry in options: 
        print(entry, menu[entry])
    selection=input("\nPlease Select: ")
    if selection =='1': 
        get_bridges()
    elif selection == '2': 
        get_bridge()
    elif selection == '3':
        get_cameras()
    elif selection == '4': 
        get_camera()
    elif selection == '5':
        break
    else: 
      print("Unknown Option Selected.")