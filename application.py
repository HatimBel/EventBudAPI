from flask import Flask, request, render_template
import json
import re
import pyrebase
from predicthq import Client
import numpy as np
from ContentBasedRecommenderSystem import contentReccomendation


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
    """
    data = {"Username": userInfo["Username"], "Password": userInfo["Password"], "FullName": userInfo["FullName"],
            "Age": userInfo["Age"], "Bio": userInfo["Bio"], "Show": userInfo["Show"],
            "Events_Liked": 0, "Picture": userInfo["Picture"], "Location": userInfo["Location"], "Channels": 0, "Questionnaire": userInfo["Questionnaire"]}
    """
    
    data = {"Username": userInfo["Username"], "Password": userInfo["Password"], "Book_Read": 0}
    
    db.child("users").child(data["Username"]).set(data)
    print(data)

    try:
        db.child("users").child(data["Username"]).set(data)

    except:
        return json.dumps({"Status": "Error"})

    return json.dumps({"Status": "Success"})


@application.route('/GetEvents', methods=['GET', 'POST'])
def get_Events():
    filters = request.form

    print(filters)

    loc = filters['Location'].split(" ")

    lat = float(loc[1])

    lon = float(loc[0])

    distance = filters['max_range']


    responseDict = {}

    if filters.get('category') == None:

        for event in phq.events.search(category="school-holidays,public-holidays,politics,conferences,expos,concerts,festivals,performing-arts,sports,community", within=("{0}km@{1},{2}").format(distance, lat, lon)):
            responseDict[event.title] = {"Description": event.description, "Category": event.category,
                                         "EventID": event.id, "Location": event.location, "Start Date": event.start.strftime('%Y-%m-%d')}

        return json.dumps(responseDict)

    for event in phq.events.search(category="school-holidays,public-holidays,politics,conferences,expos,concerts,festivals,performing-arts,sports,community", within=("{0}km@{1},{2}").format(distance, lat, lon)):
        responseDict[event.title] = {"Description": event.description, "Category": event.category,
                                     "EventID": event.id, "Location": event.location, "Start Date": event.start.strftime('%Y-%m-%d')}

    return json.dumps(responseDict)

@application.route('/GetEventInfo', methods=['GET', 'POST'])
def get_Event():
    eventID = request.form

    try:
        responseDict = {}

        event = phq.events.search(id = eventID['ID']).to_dict()['results'][0]

        location = str(event['location'][0]) + " " + str(event['location'][1])

        eventDate=str(event['start']).split(" ")


        responseDict[event['title']] = {"Description": event['description'].strip(), "Category": event['category'].strip(),
                                    "EventID": event['id'].strip(), "Location": location,
                                    "Start Date": eventDate[0]}


    except:
        return json.dumps({'Status': 'Error'})

    return json.dumps({'Status': 'Success', 'Data': responseDict})


@application.route('/LikeEvent', methods=['GET', 'POST'])
def likedEvent():
    credentials = request.form

    try:
        db.child("users").child(credentials["Username"]).child("Events_Liked").child(credentials["eventId"]).set(credentials["eventName"])

    except:
        return json.dumps({'Status': 'Error'})

    return json.dumps({'Status': 'Success'})

@application.route('/UnLikeEvent', methods=['GET', 'POST'])
def UnLikeEvent():
    credentials = request.form

    try:
        db.child("users").child(credentials["Username"]).child("Events_Liked").child(credentials["eventId"]).remove()

        return json.dumps({'Status': 'Success'})
    except:
        return json.dumps({'Status': 'Error'})

    return json.dumps({'Status': 'Error'})



@application.route('/GetUsersAttending', methods=['GET', 'POST'])
def getUsersAttending():

    event = request.form
    id=event['eventId']
    username = event['Username']

    users = {}

    try:
        all_users = db.child("users").get()

        for user in all_users.each():

                events_liked = user.val().get('Events_Liked')

                for event in events_liked:
                    if id == event:
                        users[user.key()] = user.val()

    except:
        return json.dumps({'Status': 'Error'})

    users = contentReccomendation(users, users[username]['Questionnaire'])

    users.pop(username, None)

    return json.dumps({'Status': 'Success', 'Data': users})


@application.route('/GetUser', methods=['GET', 'POST'])
def getUser():
    credentials = request.form

    try:
        user = db.child("users").child(credentials["Username"]).get().val()

    except:

        return json.dumps({"Status":"Error"})

    return json.dumps({"Status": "Success", "Data": user})



@application.route('/NewChannel', methods=['GET', 'POST'])
def NewChannel():
    user = request.form

    try:
        db.child("users").child(user["Username"]).child("Channel").child(user["ChannelID"]).set(user["ChatBuddy"])

    except:

        return json.dumps({"Status":"Error"})

    return json.dumps({"Status":"Success"})

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.templates_auto_reload = True
    application.run()