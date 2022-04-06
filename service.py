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
    ref = db.reference(path)  # slash ??
    ref.set(data)
    return "OK" 

@app.route('/get_specific_statistics', methods=["POST"])
def get_specefic_statistics():
    # you must send data and its path
    input_json = request.get_json()
    path = input_json["path"]
    ref = db.reference(path)
    jsonFileFromdB = ref.get()
    #jsonFileFromdB=firebase.get('ionicapp-2bb5c-default-rtdb/'+path,None)
    print(jsonFileFromdB)
    return {"message":jsonFileFromdB, "error":None}

@app.route('/user_init', methods=["POST"])
def user_init():
    user = "userID"
    ref = db.reference('/'+user+'/quiz')
    ref.set({
        "quiz_list":["1"],
        "avg_score":0,
        "number_quiz_done":0,
        "number_correct_qcm":0,
        "number_qcm_done":0,
        "number_qcm_done_faculte":{"Tunis":0,"Monastir":0,"Sfax":0,"Sousse":0}
    })

    return "OK - initialized"

@app.route('/get_user_init', methods=["POST"])
def get_user_init():
    user = "userID"
    a=firebase.get('ionicapp-2bb5c-default-rtdb/'+ user + "/quiz/quiz_list",None)
    b=firebase.get('ionicapp-2bb5c-default-rtdb/'+ user + "/quiz/avg_score",None)
    c=firebase.get('ionicapp-2bb5c-default-rtdb/'+ user + "/quiz/number_quiz_done",None)
    return a,b,c


@app.route('/quizlist_init', methods=["POST"])
def quizlist_init():
    ref = db.reference('/quiz/quizlist')
    ref.set({
        "course1":{"path": "cardio/Monastir/2017","id":1},
        "course2":{"path": "cardio/Monastir/2017","id":2},
        "course3":{"path": "cardio/Monastir/2017","id":3},
        "course4":{"path": "cardio/Monastir/2017","id":4},
        "course5":{"path": "cardio/Monastir/2017","id":5},
        "course6":{"path": "cardio/Monastir/2017","id":6},
        "course7":{"path": "cardio/Monastir/2017","id":7}
    })

    return "OK - initialized"


@app.route('/get_quizlist', methods=["POST"])
def get_quizlist():
    path= "/quiz/quizlist"
    ref = db.reference(path)
    jsonFileFromdB = ref.get()
    #jsonFileFromdB=firebase.get('ionicapp-2bb5c-default-rtdb/'+path,None)
    print(jsonFileFromdB)
    return {"message":extractedData, "error":None}

@app.route('/data', methods=["POST"])
def home():

    # To get data
    input_json = request.get_json() # userName - year - school - course
    #jsonFileFromdB=firebase.get('ionicapp-2bb5c-default-rtdb/Quiz', '')
    ref = db.reference(input_json["path"])
    jsonFileFromdB = ref.get()
    print(jsonFileFromdB)
    try:
        return {'data':jsonFileFromdB}
    except:
        return {'data':[]}


@app.route('/update_quiz_data', methods=["POST"])
def update_quiz_data():
    input_json = request.get_json()
    qcm_done = input_json["qcm_done"]
    qcm_correct = input_json["number_correct_qcm"]
    user = input_json["user"]
    quiz_name = input_json["quiz_name"]
    faculte = input_json["faculte"]
    # quiz list
    quiz_list = db.reference(user+"/quiz/quiz_list").get()
    db.reference(user+"/quiz/quiz_list").set(quiz_list.append(quiz_name))
    # avr score
    avg_score = db.reference(user+"/quiz/avg_score").get()
    db.reference(user+"/quiz/avg_score").set((avg_score*len(quiz_list) + (qcm_correct/qcm_done))/(len(quiz_list)+1))
    # number quiz done
    all_quiz_done = db.reference(user+"/quiz/number_quiz_done").get()
    db.reference(user+"/quiz/number_quiz_done").set(all_quiz_done+1)
    # number correct qcm
    all_correct_qcm = db.reference(user+"/quiz/number_correct_qcm").get()
    db.reference(user+"/quiz/number_correct_qcm").set(all_correct_qcm+qcm_correct)
    # number done qcm
    all_done_qcm = db.reference(user+"/quiz/number_qcm_done").get()
    db.reference(user+"/quiz/number_qcm_done").set(all_done_qcm+qcm_done)
    # faculte qcm_done
    qcm_faculte = db.reference(user+"/quiz/number_qcm_done_faculte").get()
    db.reference(user+"/quiz/number_qcm_done_faculte"+faculte).set(qcm_faculte[faculte]+qcm_done)

    return {"message":"OK", "error":None}

if __name__ == '__main__':
    app.run(debug=True, port=8080)