import pyrebase
from predicthq import Client
from PIL import Image
import base64
import requests

config = {
    "apiKey": "AIzaSyBto2Zu9RmCHCH32a5WERS67iERDP1e4YU",
    "authDomain": "eventbud-1e7fc.firebaseapp.com",
    "databaseURL": "https://eventbud-1e7fc.firebaseio.com",
    "storageBucket": "eventbud-1e7fc.appspot.com",
    "serv"
    "iceAccount": "eventbud-1e7fc-firebase-adminsdk-k2cgs-3b3094e9f8.json"
}

Image.open("/Users/jessielu/Desktop/EventsBud/profilepics/37899371_2177860019118518_6322406646731505664_o.jpg").save("sample1.bmp")

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("h.belhadjhamida@queensu.ca", "HelloWorld")
db = firebase.database()
user = auth.refresh(user['refreshToken'])

with open("sample1.bmp", "rb") as imageFile:
    encoded_string= base64.b64encode(imageFile.read())



data = {"Username": "Cathy1213", "Password": "hello", "FullName": "Cathy Yan",
            "Age": "19", "Bio": "And suddenly you know: It's time to start something new and trust the magic of beginnings.",
        "Show": "Barney",
            "Events_Liked": {}, "Picture": encoded_string.decode("utf-8").strip(), "Location": "-76.49092499 44.2274085"}
print(type(data["Picture"]))
URL = "http://Eventbud-env.whujfx5i63.us-east-2.elasticbeanstalk.com/CreateLogin"

r = requests.get(url = URL, data= data)

print(r.text)




