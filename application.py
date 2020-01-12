from flask import Flask, request, render_template
import json
import re
import pyrebase
import time
from predicthq import Client

API_TOKEN = 'pnGTFgD7W5mKiMj3C4M7cdtxDGHu2E4vf6Kdn0du'

phq = Client(access_token=API_TOKEN)

application = Flask(__name__)

config = {
    "apiKey": "AIzaSyBto2Zu9RmCHCH32a5WERS67iERDP1e4YU",
    "authDomain": "eventbud-1e7fc.firebaseapp.com",
    "databaseURL": "https://eventbud-1e7fc.firebaseio.com",
    "storageBucket": "eventbud-1e7fc.appspot.com",
    "serviceAccount": "eventbud-1e7fc-firebase-adminsdk-k2cgs-3b3094e9f8.json"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("h.belhadjhamida@queensu.ca", "HelloWorld")
db = firebase.database()
user = auth.refresh(user['refreshToken'])


@application.route('/')
def hello():
    return render_template("resttest.html")


@application.route('/login', methods=['GET', 'POST'])
def login():
    credentials = request.form

    try:
        user = (db.child("users").get().val())[credentials['Username']]

        if credentials['Password'] == user['Password']:
            return json.dumps({'Status': 'Success', 'Data': user})
    except:
        return json.dumps({'Status': 'Error'})

    return json.dumps({'Status': 'Error'})


@application.route('/CreateLogin', methods=['GET', 'POST'])
def createLogin():
    userInfo = request.form
    data = {"Username": userInfo["Username"], "Password": userInfo["Password"], "FullName": userInfo["FullName"],
            "Age": userInfo["Age"], "Bio": userInfo["Bio"], "Show": userInfo["Show"],
            "Events_Liked": userInfo["Events_Liked"], "Picture": userInfo["Picture"], "Location": userInfo["Location"]}

    try:
        db.child("users").child(data["Username"]).set(data)
    except:
        return json.dumps({"Status": "Error"})

    return json.dumps({"Status": "Success"})


@application.route('/GetEvents')
def get_Events():
    filters= request.form

    loc = filters['location'].split(" ")

    lat = float(loc[1])

    lon = float(loc[0])

    distance = int(filters['max_range'])

    lat = filters['location'][0]
    lon = filters['location'][1]
    distance = filters['location'][2]

    responseDict = {}

    if filters['category'] == None:

        for event in phq.events.search(within=("{0}km@{1},{2}").format(distance, lat, lon)):
            responseDict[event.title] = {"Description": event.description, "Category": event.category,
                                         "Location": event.location, "Start Date": event.start.strftime('%Y-%m-%d')}

        return json.dumps(responseDict)

    for event in phq.events.search(category=filters['category'], within=("{0}km@{1},{2}").format(distance, lat, lon)):
        responseDict[event.title] = {"Description": event.description, "Category": event.category,
                                     "Location": event.location, "Start Date": event.start.strftime('%Y-%m-%d')}

    return json.dumps(responseDict)

@application.route('/likedEvent', methods=['GET', 'POST'])
def likedEvent():
    credentials = request.form

    try:
        user = db.child("users").child(credentials["Username"])
        user.update({"Events_Liked": credentials["Liked_Event"]})

        return json.dumps({'Status': 'Success'})
    except:
        return json.dumps({'Status': 'Error'})

    return json.dumps({'Status': 'Error'})


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.templates_auto_reload = True
    application.run()