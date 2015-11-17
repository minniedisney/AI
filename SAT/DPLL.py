import sys
import copy
from collections import defaultdict
ans=[]
def mkSet(s):
	if s[0]=='and':
		s.remove('and')
		for i in range(0,len(s)):
			if isinstance(s[i],str) or (len(s[i])==2 and s[i][0]=='not'):
				t=[]
				t.append(s[i])
				s.remove(s[i])
				s.insert(i,t)
			if s[i][0]=='or':
				s[i].remove('or')
		return s
	else:
		if s[0]=='or':
			s.remove('or')
		if s[0]=='not':
			s=[s]
		t=[]
		t.append(s)
	return t

def checkPure(s, sub, tmp): #tmp is a string
	if isinstance(tmp,str):
		s1=copy.copy(s)
		s1.remove(sub)
		for i in range(0,len(s1)):
			if ['not', tmp] in s1[i]:
				return False
		return True
	else:
		s1=copy.copy(s)
		s1.remove(sub)
		for i in range(0,len(s1)):
			if tmp[1] in s1[i]:
				return False
		return True
def purify(s):
	for i in s:
		for j in i:
			if isinstance(j,str) and checkPure(s,i,j):			#ru guo mou ge'A' shi pure
				ans.append(j+'=true')
				ret=[]
				for x in s:
					flag=1
					for y in x:
						if isinstance(y,str) and y==j:
							flag=0
					if flag==1: ret.append(x)
				return ret
			elif isinstance(j,list) and checkPure(s,i,j):		#ru guo mou ge'notA' shi pure
				print 'here ',j
				ans.append(j[1]+'=flase')

				ret=[]
				for x in s:
					flag=1
					for y in x:
						if isinstance(y,list) and y[1]==j[1]:
							flag=0
					if flag==1: ret.append(x)
				s=ret
				return ret
	return s
def unify(s):
	for i in s:
		if len(i)==1:								#shi unit
			j=i[0]
			if isinstance(j,str):							#shi 'A'
				ans.append(j+'=true')
				ret=[]
				for x in s:
					flag=1
					t=[]
					for y in x:
						if isinstance(y,str) and y==j:
							flag=0
							break
						elif isinstance(y,list) and y[1]==j:
							continue
						t.append(y)
					if flag==1:
						ret.append(t)
				return ret
			else:
				ans.append(j[1]+'=false')
				ret=[]
				for x in s:
					flag=1
					t=[]
					for y in x:
						if isinstance(y,list) and y[1]==j[1]:
							flag=0
							break
						elif isinstance(y,str) and y==j[1]:
							continue
						t.append(y)
					if flag==1:
						ret.append(t)
				return ret
	return s
def dpll(s):
	global ans
	print 'enter ',s
	if s==[]: return True							#zong ji shi kong,shuo ming suan fa jie shu
	for i in s:										#zi ji shi kong,shuo ming shi bai
		if i==[]: return False
	tmp1=purify(s)
	print tmp1
	if s==tmp1:
		tmp1=unify(s)
		print tmp1
		if s==tmp1:
			tmpsymbol=s[0][0]
			s.append([tmpsymbol])
			tmps=copy.deepcopy(s)
			tmpans=copy.deepcopy(ans)
			if dpll(s): return True
			s=copy.deepcopy(tmps)
			ans=copy.deepcopy(tmpans)
			if isinstance(tmpsymbol,str):
				s[len(s)-1][0]=['not',tmpsymbol]
			else:
				s[len(s)-1][0]=[tmpsymbol[1]]
			return dpll(s)
		else:
			s=tmp1
			return dpll(s)
	else:
		s=tmp1
		return dpll(s)
file1 = open(sys.argv[2])
file2=open('CNF_satisfiability.txt','w')
n=int(file1.readline())
for line in file1:
	print "~~~~~~~~~~~~~~~~~~~"
	ans=[]
	myList= eval(line)
	if dpll(mkSet(myList)): print>>file2, ans
	else: print >>file2,['false']
file1.close()
file2.close()