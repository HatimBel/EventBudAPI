from flask import Flask, request, render_template
import json
import re
import pyrebase
from predicthq import Client

API_TOKEN = 'pnGTFgD7W5mKiMj3C4M7cdtxDGHu2E4vf6Kdn0du'

phq = Client(access_token=API_TOKEN)

application = Flask(__name__)

config = {
  "apiKey": "AIzaSyBto2Zu9RmCHCH32a5WERS67iERDP1e4YU",
  "authDomain": "eventbud-1e7fc.firebaseapp.com",
  "databaseURL": "https://eventbud-1e7fc.firebaseio.com",
  "storageBucket": "eventbud-1e7fc.appspot.com",
  "serviceAccount": "/Users/hatimbelhadjhamida/Desktop/EventsBud/eventbud-1e7fc-firebase-adminsdk-k2cgs-3b3094e9f8.json"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("h.belhadjhamida@queensu.ca", "HelloWorld")
db = firebase.database()

@application.route('/')
def hello():

    return render_template("resttest.html")
    
@application.route('/login', methods=['GET', 'POST'])
def login():


    credentials = request.form

    all_users = db.child("users").get()
    for user in all_users.each():

        if credentials['Password'] == user.val()['Password'] and credentials['Username'] == user.val()['Username']:
            return json.dumps({'Status': 'Success', 'Data': user.val()})


    return json.dumps({'Status': 'Error'})


@application.route('/CreateLogin', methods=['GET', 'POST'])
def createLogin():
    userInfo = request.form
    data = {"Username": userInfo["Username"], "Password": userInfo["Password"],
            "Age": userInfo["Age"], "Artists": userInfo["Artists"], "Bio": userInfo["Bio"],
            "Events_Liked": userInfo["Events_Liked"]}

    try:
        db.child("users").push(data)
    except:
        return json.dumps({"Status": "Error"})


    return json.dumps({"Status": "Success"})

@application.route('/GetEvents')
def get_Events():

    #filters=request.form
    filters={'category':None,'location':[174.776792,-36.847319,15000]}

    lat=filters['location'][0]
    lon=filters['location'][1]
    distance=filters['location'][2]

    responseDict = {}

    if filters['category'] == None:

        for event in phq.events.search( within=("{0}km@{1},{2}").format(distance, lat, lon)):

           responseDict[event.title] = {"Description":event.description, "Category":event.category, "Location": event.location, "Start Date": event.start.strftime('%Y-%m-%d')}

        return json.dumps(responseDict)


    for event in phq.events.search(category=filters['category'],within=("{0}km@{1},{2}").format(distance,lat,lon)):
        responseDict[event.title] = {"Description": event.description, "Category": event.category,
                                     "Location": event.location, "Start Date": event.start.strftime('%Y-%m-%d')}


    return json.dumps(responseDict)



if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.templates_auto_reload = True
    application.run()