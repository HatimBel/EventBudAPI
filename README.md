# EventBudAPI
API developed for the EventBud mobile app, to fetch user data, local events, and chat channels

## Libraries/APIs

* [Firebase](https://firebase.google.com/) - Database used
* [Pyrebase](https://github.com/thisbejim/Pyrebase) - Python wrapper for the Firebase API
* [PredictHQ](https://www.predicthq.com/events/upcoming-events) - API used to fetch local events
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Python Rest API framework 

## Endpoints

**Route: /login**

ARGS:
'Username'
'Password'

Return:

Error:
{'Status': 'Error'}

Success:
{'Status': 'Success', 'Data': user}


**Route: /CreateLogin**

ARGS:
'Username'
'Password'
'FullName'
'Age'
'Bio'
'Show'
'Picture'
'Location'

Error
{'Status': 'Error'}

Success:
{'Status': 'Success'}


**Route: /GetEvents**

ARGS:
'Location' - Lat index 0 Long index 1
'max_range'
'category' - Optional

Error:
{'Status': 'Error'}

Success:
{"Description": event.description, "Category": event.category,
"EventID": event.id, "Location": event.location, "Start Date": event.start.strftime('%Y-%m-%d')}


**Route: /GetEventInfo**

ARGS:
'ID'

Error:
{'Status': 'Error'}

Success:
{'Status': 'Success', 'Data': {"Description": event['description'].strip(), "Category": event['category'].strip(),
                                    "EventID": event['id'].strip(), "Location": event['location'].strip(),
                                    "Start Date": eventDate[0]}}


**Route: /LikeEvent**

ARGS:
'Username'
'eventId'
'eventName'

Error:
{'Status': 'Error'}

Success:
{'Status': 'Success'}


**Route: /LikeEvent**

ARGS:
'Username'
'eventId'

Error:
{'Status': 'Error'}

Success:
{'Status': 'Success'}


**Route: /GetUsersAttending**

ARGS:
'eventId'

Error:
{'Status': 'Error'}

Success:
{'Status': 'Success', 'Data': users}


**Route: /GetUser**

ARGS:
'Username'

Error:
{'Status': 'Error'}

Success:
{'Status': 'Success', 'Data': user}


**Route: /NewChannel**

ARGS:
"Username"
"ChannelID"
"ChatBuddy"

Error:
{'Status': 'Error'}

Success:
{'Status': 'Success'}



USER DATA:

{"Username": userInfo["Username"], "Password": userInfo["Password"], "FullName": userInfo["FullName"], "Channel": {ChannelName:User},
            "Age": userInfo["Age"], "Bio": userInfo["Bio"], "Show": userInfo["Show"], "Questionnaire": userInfo["Questionnaire"],
            "Events_Liked": {}, "Picture": userInfo["Picture"], "Location": userInfo["Location"]}

