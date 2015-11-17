import sys
import copy
from collections import defaultdict

""" READ THE INPUT FILE """
inputFile = open(sys.argv[2])
array = []
array = inputFile.readlines()
myList=[]
for i in range(1, len(array)):
	myList.insert((i-1),eval(array[i]))


def elim(s):
	if isinstance(s,str):
		return s
	if s[0] == 'implies':
		return ['or', ['not', elim(s[1])], elim(s[2])]
	if s[0] == 'iff':
		return ['and', ['or', ['not', elim(s[1])], elim(s[2])], ['or', ['not', elim(s[2])], elim(s[1])]]
	ret = []
	for sublist in s:
		ret.append(elim(sublist))
	return ret

def neg(s):
	if isinstance(s,str):
		return s
	if s[0]=='not' and s[1][0]=='not':
		return neg(s[1][1])
	ret = []
	for sublist in s:
		ret.append(neg(sublist))
	return ret

def deMog(s):
	if isinstance(s,str):
		return s
	if s[0]=='not' and s[1][0]=='and':
		temp1=['or']
		for i in range(1,len(s[1])):
			temp1.append(deMog(['not', deMog(s[1][i])]))
		return deMog(temp1)
	if s[0]=='not' and s[1][0]=='or':
		temp2=['and']
		for i in range(1,len(s[1])):
			temp2.append(deMog(['not', deMog(s[1][i])]))
		return deMog(temp2)
	ret = []
	for sublist in s:
		ret.append(deMog(sublist))
	return ret

def mul(temp1, temp2):
	ret = []
	if temp1[0]=='not' or temp1[0]=='or' or isinstance(temp1,str):
		for i in range(0,len(temp2)):
			ret.append([temp1,temp2[i]])
		return ret
	if temp2[0]=='not' or temp2[0]=='or' or isinstance(temp2,str):
		for i in range(0,len(temp1)):
			ret.append([temp2,temp1[i]])
		return ret
	
	for i in range(0,len(temp2)):
		for j in range(0,len(temp1)):
			if isinstance(temp1[j],str):
				ret.append([temp1[j],temp2[i]])
			else:
				t=copy.copy(temp1[j])
				t.append(temp2[i])
				ret.append(t)
	return ret

def recurMul(s, n):
	if n<=1:
		return s[0]
	else:
		return mul(recurMul(s, n-1), s[n-1])

def trans(s):
	#temp=[]
	s.remove('or')
	for i in range(0,len(s)):
		if 'and' in s[i]:
			s[i].remove('and')
	k=len(s)
	tmpList = recurMul(s,k)
	#appList=['or']
	for sublist in tmpList:
		sublist.insert(0,'or')
	tmpList.insert(0,'and')
	return tmpList

def check(s):
	if s[0]!='or':
		return False
	for i in range(1,len(s)):
		if s[i][0] == 'and':
			return True	
	return False

def dist(s):
	if isinstance(s,str):
		return s
	if check(s):
#		print "true"
		return trans(s)
		#return dist(['and', dist(['or', dist(s[2]), dist(s[1][1])]), dist(['or', dist(s[2]), dist(s[1][2])])])
	ret = []
	for sublist in s:
		ret.append(dist(sublist))
	return ret

def checkOr(s):
	if s[0]!='or':
		return False
	for i in range(1,len(s)):
		if s[i][0] == 'or':
			return True	
	return False
def checkAnd(s):
	if s[0]!='and':
		return False
	for i in range(1,len(s)):
		if s[i][0] == 'and':
			return True	
	return False		
def ass(s):
	if isinstance(s,str):
		return s
	if checkOr(s):
		temp=['or']
		for i in range(1,len(s)):
			if s[i][0] == 'or':
				for j in range(1,len(s[i])):
					temp.append(s[i][j])
			else:
				temp.append(ass(s[i]))
		return ass(temp)
	if checkAnd(s):
		temp=['and']
		for i in range(1,len(s)):
			if s[i][0] == 'and':
				for j in range(1,len(s[i])):
					temp.append(s[i][j])
			else:
				temp.append(ass(s[i]))
		return ass(temp)
	ret = []
	for sublist in s:
		ret.append(ass(sublist))
	return ret

def elimId(s):	
	if s[0]=='and':		
		ret=['and']
		for i in range(1,len(s)):
			l2 = []
			for j in s[i]:
				if j not in l2:
					l2.append(j)
			ret.append(l2)
		l2 = []
		for i in ret:
			if not i in l2:
				l2.append(i)
		return l2
	else:
		l2=[]
		for i in s:
			if not i in l2:
				l2.append(i)
		return l2

ans=[]
for i in range(0,len(myList)):
	ans.append(elimId(ass(dist(neg(deMog(elim(myList[i])))))))


f=open('/Users/dengyaqiao/Desktop/561HW1.txt','w')
for item in ans:
  print>>f, item
f.close()













