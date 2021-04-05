from firebase import firebase
from flask import Flask, request
from flask_cors import CORS


# Import database module.
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize the app with a service account, granting admin privileges

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://ionicapp-2bb5c-default-rtdb.firebaseio.com'
})

# Get a database reference to our blog.
ref = db.reference('/')


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

    
firebase = firebase.FirebaseApplication("https://ionicapp-2bb5c-default-rtdb.firebaseio.com", None) 

@app.route('/statistics', methods=["POST"])
def get_statistics(username):

    input_json = request.get_json()
    
    jsonFileFromdB=firebase.get('ionicapp-2bb5c-default-rtdb/Quiz/statistics')
    key_ = list(jsonFileFromdB.keys())[0]
    extractedData = jsonFileFromdB[key_]
    print("Data: ")
    print(extractedData)
    
    try:
        return {'data':extractedData[input_json['year']][input_json['school']][input_json['course']]}
    except:
        return {'data':[]}

@app.route('/post_specific_statistics', methods=["POST"])
def post_specefic_statistics():
    # you must send data and its path
    input_json = request.get_json()
    path = input_json["path"]
    data = input_json["data"]
   # firebase = firebase.FirebaseApplication("https://ionicapp-2bb5c-default-rtdb.firebaseio.com/", None) # Auth= None because we're in Test Mode
    result = firebase.post('ionicapp-2bb5c-default-rtdb/'+path, data)  # to be modified to fit the path
    print(result)
    return "OK" 

@app.route('/get_specific_statistics', methods=["POST"])
def get_specefic_statistics():
    # you must send data and its path
    input_json = request.get_json()
    path = input_json["path"]
  #  firebase = firebase.FirebaseApplication("https://ionicapp-2bb5c-default-rtdb.firebaseio.com/", None) # Auth= None because we're in Test Mode
    jsonFileFromdB=firebase.get('ionicapp-2bb5c-default-rtdb/'+path,None)
    print(jsonFileFromdB)
    key_ = list(jsonFileFromdB.keys())[0]
    extractedData = jsonFileFromdB[key_]
    return {"message":extractedData, "error":None}

@app.route('/user_init', methods=["POST"])
def user_init():

    user = "userID"
    ref = db.reference('/'+user+'/quiz')
    ref.set({
        "quiz_list":[],
        "avg_score":0,
        "number_quiz_done":0,
        "number_correct_qcm":0,
        "number_qcm_done":0,
        "number_qcm_done_faculte":0,
        "number_qcm_done_year":1
    })

    db_ref= ref.child("number_qcm_done_year")
    db_ref.set(0)
    return "OK - initialized"

@app.route('/get_user_init', methods=["POST"])
def get_user_init():
    user = "userID"
    a=firebase.get('ionicapp-2bb5c-default-rtdb/'+ user + "/quiz/quiz_list",None)
    b=firebase.get('ionicapp-2bb5c-default-rtdb/'+ user + "/quiz/avg_score",None)
    c=firebase.get('ionicapp-2bb5c-default-rtdb/'+ user + "/quiz/number_quiz_done",None)
    return a,b,c


if __name__ == '__main__':
    app.run(debug=True, port=8080)