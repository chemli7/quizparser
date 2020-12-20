from firebase import firebase
from flask import Flask, request

app = Flask(__name__)
    
firebase = firebase.FirebaseApplication("https://ionicapp-2bb5c-default-rtdb.firebaseio.com/", None) # Auth= None because we're in Test Mode


@app.route('/data', methods=["POST"])
def home():
    # To get data
    input_json = request.get_json() # userName - year - school - course

    jsonFileFromdB=firebase.get('ionicapp-2bb5c-default-rtdb/Quiz', '')
    key_ = list(jsonFileFromdB.keys())[0]
    extractedData = jsonFileFromdB[key_]
    try:
        return {'data':extractedData[input_json['year']][input_json['school']][input_json['course']]}
    except:
        return {'data':[]}
    
if __name__ == '__main__':
    app.run(debug=True, port=8080)