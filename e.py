from firebase import firebase
from firebase_admin import db

# Initialize the app with a service account, granting admin privileges

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://ionicapp-2bb5c-default-rtdb.firebaseio.com'
})

f = open("test", "r")
c = f.readline()
List=[]

def isQuestion(s):
	if len(s)<4:
		return None
	if s[0] in ['1','2','3','4','5','6','7','8','9']:
		try :
			if (int(s.split('-')[0])) in range(1000):
				return '-'	
		except:
			if (int(s.split('.')[0])) in range(1000):
				return '.'
		return None
	return None
	
def isAnswer(s):
	if len(s)<4:
		return False
	if ( s[0:2] in ['A-','B-','C-','D-','E-'] ) or ( s[0:2] in ['A.','B.','C.','D.','E.'] ):
		return True	
	return False

	
while not c is None:	
	try :
		c[0]
	except:
		break	
	separator = isQuestion(c)		
	if separator:
		element={}
		element["title"] = c
		#List.append(element)
		line=0
		while True:
			if line==5:							
				break	
			q = f.readline()
			if isAnswer(q) :
				line +=1
				element[q[0]] = q
			else:
				element["title"] = element["title"] + q
		element["rightAnswers"] = [1,3]		 
		List.append(element)
	c = f.readline()
JSONFILE = {}
JSONFILE["2018"] = {}
JSONFILE["2018"]["Monastir"] = {}
JSONFILE["2018"]["Monastir"]["Cardio"] = List 



	
firebase = firebase.FirebaseApplication("https://ionicapp-2bb5c-default-rtdb.firebaseio.com/", None) # Auth= None because we're in Test Mode

data = JSONFILE

# To post data 
#result = firebase.post('ionicapp-2bb5c-default-rtdb/Quiz', data)
ref = db.reference('/quiz')
data["quizlist"]={
        "course1":{"path": "cardio/Monastir/2017","id":1},
        "course2":{"path": "cardio/Monastir/2017","id":2},
        "course3":{"path": "cardio/Monastir/2017","id":3},
        "course4":{"path": "cardio/Monastir/2017","id":4},
        "course5":{"path": "cardio/Monastir/2017","id":5},
        "course6":{"path": "cardio/Monastir/2017","id":6},
        "course7":{"path": "cardio/Monastir/2017","id":7}
    }
ref.set(data)

# # To get data
# jsonFileFromdB=firebase.get('ionicapp-2bb5c-default-rtdb/Quiz', '')
# key_ = list(jsonFileFromdB.keys())[0]
# extractedData = jsonFileFromdB[key_]
# print(extractedData)
	
	
	
	
	
	
	
	
	
	
	
	
	
	 
