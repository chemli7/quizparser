from firebase import firebase
from firebase_admin import db

# Initialize the app with a service account, granting admin privileges

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://ionicapp-2bb5c-default-rtdb.firebaseio.com'
})

f = open("test", "rb")
c = f.readline().decode("utf-8")
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

def toNumber(c):
	if c == 'A':
		return 0
	if c == 'B':
		return 1
	if c == 'C':
		return 2
	if c == 'D':
		return 3
	if c == 'E':
		return 4
	
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
			q = f.readline().decode("utf-8")
			if isAnswer(q) :
				line +=1
				element[q[0]] = q
			else:
				element["title"] = element["title"] + q
		resp = f.readline().decode("utf-8").split('.')
		resp = [ toNumber(i.strip()) for i in resp]
		element["rightAnswers"] = resp
		List.append(element)
	c = f.readline().decode("utf-8")
    
JSONFILE = {}
print("Welcome to the quiz parser...\n")
print("please pay attention to the spelling of the words\n")
print("if you see any logs printed in the screen, please contact me")
print("text need to be in a file named test in the same directory(dossier) of the script")
university = str(input("quelle université?\n"))
certif = str(input("quelle certif?\n"))
cours = str(input("quelle cours?\n"))
year = str(input("quelle year?\n"))
JSONFILE[university] = {}
JSONFILE[university][certif] = {}
JSONFILE[university][certif][cours] = List 



	
firebase = firebase.FirebaseApplication("https://ionicapp-2bb5c-default-rtdb.firebaseio.com/", None) # Auth= None because we're in Test Mode

data = JSONFILE

# To post data 
#result = firebase.post('ionicapp-2bb5c-default-rtdb/Quiz', data)
ref = db.reference('/quiz/'+year)
# data["quizlist"]={
        # "course1":{"path": "cardio/Monastir/2017","id":1},
        # "course2":{"path": "cardio/Monastir/2017","id":2},
        # "course3":{"path": "cardio/Monastir/2017","id":3},
        # "course4":{"path": "cardio/Monastir/2017","id":4},
        # "course5":{"path": "cardio/Monastir/2017","id":5},
        # "course6":{"path": "cardio/Monastir/2017","id":6},
        # "course7":{"path": "cardio/Monastir/2017","id":7}
    # }
# ref.set(data)

ref.set(data)

# # To get data
# jsonFileFromdB=firebase.get('ionicapp-2bb5c-default-rtdb/Quiz', '')
# key_ = list(jsonFileFromdB.keys())[0]
# extractedData = jsonFileFromdB[key_]
# print(extractedData)
	
	
	
	
	
	
	
	
	
	
	
	
	
	 
