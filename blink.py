import requests

from gpiozero import LED
from time import sleep
led = LED(22) # eventually change this to a relay signal



username = ""
TWITCH_CLIENT_ID = ""

ERROR = False

print("Monitoring Username: " +username)

TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/kraken/streams/{}"

TWITCH_USERID = "https://api.twitch.tv/kraken/users?login={}"

API_HEADERS = { 'Client-ID' : TWITCH_CLIENT_ID, 
          'Accept' : 'application/vnd.twitchtv.v5+json', } 

reqSession = requests.Session()

def userIsStreaming(userID):
  global ERROR
  #returns true if online, false if not 
  url = TWITCH_STREAM_API_ENDPOINT_V5.format(userID)
  try:
    req = reqSession.get(url, headers=API_HEADERS)
    jsondata = req.json()
    if 'stream' in jsondata:
      if jsondata['stream'] is not None:
        return True
      else:
        return False
  except Exception as e:
    ERROR = True
    return False

def getUserID(userName):
  global ERROR
  url = TWITCH_USERID.format(userName)
  try:
    req = reqSession.get(url, headers=API_HEADERS)
    jsondata = req.json()
    if 'users' in jsondata:
      return int(jsondata['users'][0]['_id'])
    else:
      print("User not found: " + userName)
      return 0
  except Exception as e:
    ERROR = True
    return 0

def error():
  print("ERROR")
  while True:
    led.on()
    sleep(0.15)
    led.off()
    sleep(0.15)


userid = getUserID(username)
print("UserID: "+str(userid))

def stream_notification():
  global userid
  global ERROR
  if ERROR:
    error()
  else:
    if (userIsStreaming(userid)):
      return True
    else:
      return False

def wait(times):
  for i in range(times):
    led.on()
    sleep(1)
    led.off()
    sleep(1)



def check_stream():
  if stream_notification():
    led.on()
    sleep(120)
  else:
    wait(60)








# main loop
while True:
  check_stream()

