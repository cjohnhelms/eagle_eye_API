from multiprocessing.forkserver import ensure_running
from pathlib import Path
from time import sleep
import requests
import json
import pyperclip
import webbrowser

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
    bridgeList = s.get(url=f'http://{subd}.eagleeyenetworks.com/g/device/list', headers={"Authentication": akey}, params={"t": "bridge"})
    print(bridgeList)
    print('\n')
    print(*bridgeList.json(), sep='\n' * 2)

# Get Bridge
def get_bridge():
    pram = {"id": input('Please provide a valid ESN: ')}
    bridge = s.get(url=f'http://{subd}.eagleeyenetworks.com/g/device', headers={"Authentication": akey}, params=pram)
    print(bridge)
    print('\n')
    print(*bridge.json(), sep='\n' * 2)
    
# Get List of Cameras
def get_cameras():
    cameraList = s.get(url=f'http://{subd}.eagleeyenetworks.com/g/device/list', headers={"Authentication": akey}, params={"t": "camera"})
    print(cameraList)
    print('\n')
    print(*cameraList.json(), sep='\n' * 2)

# Get Camera
def get_camera():
    pram = {"id": input('Please provide a valid ESN: ')}
    camera = s.get(url=f'http://{subd}.eagleeyenetworks.com/g/device', headers={"Authentication": akey}, params=pram)
    print(camera)
    print('\n')
    print(*camera.json(), sep='\n' * 2)

def ask_params():
    global prams
    global esn
    global startts
    global endts
    esn = str(input('Please provide a valid camera ESN: '))
    startts = str(input('Please provide a start timestamp in format YYYYMMDDHHMMSS.NNN: '))
    endts = str(input('Please provide an end timestamp in YYYMMDDMMSS.NNN format: '))
    prams = {"id": esn, "start_timestamp": startts, "end_timestamp": endts}

# Get Videos
def get_videos():
    videos = s.get(f'https://{subd}.eagleeyenetworks.com/asset/list/video', headers=my_headers, params=prams)
    print(videos)
    print('\n')
    for i in videos.json():
        print(i)

# Get Video
def get_video():
    video = s.get(f'https://{subd}.eagleeyenetworks.com/asset/play/video.mp4', headers={"Authentication": akey}, params=prams)
    print('\n')
    if video.status_code == 202:
        print(video.json())
    if video.status_code == 200:
        pyperclip.copy(f'https://{subd}.eagleeyenetworks.com/asset/play/video.mp4?id={esn}&start_timestamp={startts}&end_timestamp={endts}')
        webbrowser.open(f'https://{subd}.eagleeyenetworks.com/asset/play/video.mp4?id={esn}&start_timestamp={startts}&end_timestamp={endts}')
    
# Check Download
def check_download():
    video = s.get(f'https://{subd}.eagleeyenetworks.com/asset/play/video.mp4', headers={"Authentication": akey}, params=prams)
    print('\n')
    if video.status_code == 202:
        print(video.json())
    if video.status_code == 200:
        pyperclip.copy(f'https://{subd}.eagleeyenetworks.com/asset/play/video.mp4?id={esn}&start_timestamp={startts}&end_timestamp={endts}')
        webbrowser.open(f'https://{subd}.eagleeyenetworks.com/asset/play/video.mp4?id={esn}&start_timestamp={startts}&end_timestamp={endts}')



#######################################################################################################################################

menu = {}
menu['1']="Get List of Bridges" 
menu['2']="Get Bridge"
menu['3']="Get List of Cameras"
menu['4']="Get Camera"
menu['5']="Get List of Videos"
menu['6']="Get Video"
menu['7']="Check Download"
menu['8']="Exit"
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
        ask_params()
        get_videos()
    elif selection == '6':
        ask_params()
        get_video()
    elif selection == '7':
        check_download()
    elif selection == '8':
        break
    else: 
      print("Unknown Option Selected.")