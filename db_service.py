from firebase import firebase
from flask import Flask, request
from flask_cors import CORS



app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

    
firebase = firebase.FirebaseApplication("https://ionicapp-2bb5c-default-rtdb.firebaseio.com/", None) # Auth= None because we're in Test Mode

get_statistics(username):
    jsonFileFromdB=firebase.get('ionicapp-2bb5c-default-rtdb/Quiz/statistics')

    key_ = list(jsonFileFromdB.keys())[0]
    extractedData = jsonFileFromdB[key_]
    print("Data: ")
    print(extractedData)
    try:
        return {'data':extractedData[input_json['year']][input_json['school']][input_json['course']]}
    except:
        return {'data':[]}

post_specefic_statistics():
    # you must send data and its path
    input_json = request.get_json()
    path = input_json["path"]
    data = input_json["data"]
   # firebase = firebase.FirebaseApplication("https://ionicapp-2bb5c-default-rtdb.firebaseio.com/", None) # Auth= None because we're in Test Mode

    
    result = firebase.post('ionicapp-2bb5c-default-rtdb/'+path, data)  # to be modified to fit the path
    print(result) 

get_specefic_statistics():
    # you must send data and its path
    input_json = request.get_json()
    path = input_json["path"]

  #  firebase = firebase.FirebaseApplication("https://ionicapp-2bb5c-default-rtdb.firebaseio.com/", None) # Auth= None because we're in Test Mode

    jsonFileFromdB=firebase.get('ionicapp-2bb5c-default-rtdb/'+path)

    key_ = list(jsonFileFromdB.keys())[0]
    extractedData = jsonFileFromdB[key_]
    return extractedData
