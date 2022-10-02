from multiprocessing.forkserver import ensure_running
from re import X
import requests
import json
import pyperclip
import webbrowser
from getpass import getpass

uname = str(input('Please provide a username: '))
pword = str(getpass('Please provide a password: '))
akey = str(getpass('Please provide an API key: '))
subd = str(input('Please provide the sub domain: '))
print('\n')

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

# Ask for the ESN and start/end times for the list of clips
def ask_params():
    global prams
    global esn
    esn = str(input('Please provide a valid camera ESN: '))
    startts = str(input('Please provide a start timestamp in YYYYMMDDHHMMSS.NNN format: '))
    endts = str(input('Please provide an end timestamp in YYYMMDDMMSS.NNN format: '))
    prams = {"id": esn, "start_timestamp": startts, "end_timestamp": endts}

# Get Video - this code has now been integrated in the get_videos function, but I am leaving here for documentation
# def get_video():
#     video = s.get(f'https://{subd}.eagleeyenetworks.com/asset/play/video.mp4', headers={"Authentication": akey}, params=prams)
#     print('\n')
#     if video.status_code == 202:
#         print(video.json())
#     if video.status_code == 200:
#         # pyperclip.copy(f'https://{subd}.eagleeyenetworks.com/asset/play/video.mp4?id={esn}&start_timestamp={startts}&end_timestamp={endts}')
#         webbrowser.open(f'https://{subd}.eagleeyenetworks.com/asset/play/video.mp4?id={esn}&start_timestamp={startts}&end_timestamp={endts}')
    
# Get Videos
def get_video():
    videos = s.get(f'https://{subd}.eagleeyenetworks.com/asset/list/video', headers=my_headers, params=prams)
    print(videos)
    print('\n')
    # print(type(videos.json()))
    x = 0
    for i in videos.json():
        print('['+str(x)+']'+'\t' + str(i))
        x += 1
    print('\n')
    selection = int(input('Please select a video: '))
    dic = videos.json()[selection]
    global vidInfo
    global stime
    global etime
    stime = str(dic['s'])
    etime = str(dic['e'])
    vidInfo = {"id": esn, "start_timestamp": stime, "end_timestamp": etime}
    video = s.get(f'https://{subd}.eagleeyenetworks.com/asset/play/video.mp4', headers={"Authentication": akey}, params=vidInfo)
    print('\n')
    if video.status_code == 202:
        print(video.json())
    if video.status_code == 200:
        # pyperclip.copy(f'https://{subd}.eagleeyenetworks.com/asset/play/video.mp4?id={esn}&start_timestamp={startts}&end_timestamp={endts}')
        webbrowser.open(f'https://{subd}.eagleeyenetworks.com/asset/play/video.mp4?id={esn}&start_timestamp={stime}&end_timestamp={etime}')
    
# Check Download
def check_download():
    vidCheck = s.get(f'https://{subd}.eagleeyenetworks.com/asset/play/video.mp4', headers={"Authentication": akey}, params=vidInfo)
    print('\n')
    if vidCheck.status_code == 202:
        print(vidCheck.json())
    if vidCheck.status_code == 200:
        # pyperclip.copy(f'https://{subd}.eagleeyenetworks.com/asset/play/video.mp4?id={esn}&start_timestamp={startts}&end_timestamp={endts}')
        webbrowser.open(f'https://{subd}.eagleeyenetworks.com/asset/play/video.mp4?id={esn}&start_timestamp={stime}&end_timestamp={etime}')



#######################################################################################################################################

menu = {}
menu['[1]']="Get List of Bridges" 
menu['[2]']="Get Bridge"
menu['[3]']="Get List of Cameras"
menu['[4]']="Get Camera"
menu['[5]']="Get Video"
menu['[6]']="Check Download"
menu['[7]']="Exit"
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
        get_video()
    elif selection == '6':
        check_download()
    elif selection == '7':
        break
    else: 
      print("Unknown Option Selected.")