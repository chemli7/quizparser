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
		return None
	if ( s[0:2] in ['A-','B-','C-','D-','E-'] ) or ( s[0:2] in ['A.','B.','C.','D.','E.'] ):
		return True	
	return None

	
while not c is None:	
	try :
		c[0]
	except:
		break	
	separator = isQuestion(c)		
	if separator:
		ch = c.split(separator)[0]
		if int(ch) in range(100):
			element={}
			element["title"] = c
			#List.append(element)
			line=0
			while True:
				if line==5:							
					break	
				q = f.readline()
				if isAnswer(q):
					line +=1
					element[q[0]] = q
				else:
					element["title"] = element["title"] + q 
			List.append(element)
	c = f.readline()
print(List)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	 
