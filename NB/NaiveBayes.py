import sys
import copy
from collections import defaultdict

inputFile = open(sys.argv[2])
array = inputFile.readlines()
tmp1,tmp2=array[0].split()
numD,numP=int(tmp1),int(tmp2)
listP=[] #list of patients
for i in range(0,numP):
	str1='Patient-'+str(i+1)
	listP.append(str1)
listDS=[]
listFind=[]
table1,table2,table3,table4,table5,table6,table7,table8,table9,table10,table11={},{},{},{},{},{},{},{},{},{},{} #D-P(D)
for i in range(0,numD):
	tmp=array[4*i+1]
	dis,num,pos=tmp.split()
	listDS.append(dis)
	table1[dis]=float(pos)
	table2[dis]=eval(array[4*i+2])
for i in range(0,numD):
	listF=eval(array[4*i+2])
	a=eval(array[4*i+3])
	b=eval(array[4*i+4])
	for j in range(0,len(listF)):
		listFind.append(listF[j])
		table3[listF[j]]=float(a[j])
		table4[listF[j]]=float(b[j])
		table8[listF[j]]=float(float(a[j])/float(b[j]))
		table9[listF[j]]=float((1-float(b[j]))/(1-float(a[j])))
		table10[listF[j]]=float((1-float(a[j]))/(1-float(b[j])))
		table11[listF[j]]=float(float(b[j])/float(a[j]))
		if float(a[j])>float(b[j]):
			table6[listF[j]]='T'
			table7[listF[j]]='F'
		else:
			table6[listF[j]]='F'
			table7[listF[j]]='T'
for i in range(0,numP):
	tmpList=[]
	for j in range(0,numD):
		tmpList.append(eval(array[4*numD+1+j+numD*i]))
	table5[listP[i]]=tmpList
def func1(D,arr):
	PD=table1[D]
	arrFind=table2[D] #list of findings
	arr1=[]
	arr2=[]
	for i in range(0,len(arr)):
		if arr[i]=='T':
			arr1.append(table3[arrFind[i]]) #cha ru yi ge float 
			arr2.append(table4[arrFind[i]])
		elif arr[i]=='F':
			arr1.append(1-table3[arrFind[i]]) 
			arr2.append(1-table4[arrFind[i]])
	fenzi=PD
	fenmu=1-PD
	for x in arr1:
		fenzi=fenzi*x
	for y in arr2:
		fenmu=fenmu*y
	ans=float(1/(1+fenmu/fenzi))
	return "{0:.4f}".format(round(ans,4))

def func2(tmplist):
	ans={}
	for i in range(0,len(tmplist)):
		ans[listDS[i]]=func1(listDS[i],tmplist[i])
	return ans

def maxP(table):
	for x in table.values():
		count=0
		for y in x:
			for i in range(0,len(y)):
				if y[i]=='U':
					y[i]=table6[listFind[count]]
				count=count+1
	return table

def minP(table):
	for x in table.values():
		count=0
		for y in x:
			for i in range(0,len(y)):
				if y[i]=='U':
					y[i]=table7[listFind[count]]
				count=count+1
	return table

copy1=copy.deepcopy(table5)
copy2=copy.deepcopy(table5)
maxTable=maxP(copy1)
minTable=minP(copy2)

def findMax(D,list1):
	maxNum=0
	ans=[]
	tempStr=''
	flag=''
	check=0
	check1=0
	list2=table2[D]
	for i in range(0,len(list1)):
		if list1[i]=='U':
			check=1
	if check==0:
		ans.append("none")
		ans.append("N")
	else:
		for i in range(0,len(list1)):
			if list1[i]=='U':
				if table8[list2[i]]!=table10[list2[i]]:
					check1=1					
					if table8[list2[i]]>table10[list2[i]]:
						curMax=table8[list2[i]]
					else:
						curMax=table10[list2[i]]
					if curMax>maxNum:
						maxNum=curMax
						tempStr=list2[i]
						if table8[list2[i]]<table10[list2[i]]:
							flag='F'
						else:
							flag='T'
		if check1==0:
			ans.append("none")
			ans.append("N")
		else:
			ans.append(tempStr)
			ans.append(flag)
	return ans

def findMin(D,list1):
	maxNum=0
	ans=[]
	tempStr=''
	flag=''
	check=0
	check1=0
	list2=table2[D]
	for i in range(0,len(list1)):
		if list1[i]=='U':
			check=1
	if check==0:
		ans.append("none")
		ans.append("N")
	else:
		for i in range(0,len(list1)):
			if list1[i]=='U':
				if table8[list2[i]]!=table10[list2[i]]:
					check1=1					
					if table8[list2[i]]>table10[list2[i]]:
						curMax=table8[list2[i]]
					else:
						curMax=table10[list2[i]]
					if curMax>maxNum:
						maxNum=curMax
						tempStr=list2[i]
						if table8[list2[i]]<table10[list2[i]]:
							flag='T'
						else:
							flag='F'
		if check1==0:
			ans.append("none")
			ans.append("N")
		else:
			ans.append(tempStr)
			ans.append(flag)
	return ans

tmpT={}
for key,value in table5.items():
	tmpTT={}
	for i in range(0,len(value)):
		ans=[]
		ans.append(findMax(listDS[i],value[i])[0])
		ans.append(findMax(listDS[i],value[i])[1])
		ans.append(findMin(listDS[i],value[i])[0])
		ans.append(findMin(listDS[i],value[i])[1])
		tmpTT[listDS[i]]=ans
	tmpT[key]=tmpTT
#print tmpT
f=open('/Users/dengyaqiao/Desktop/561HW3.txt','w')
for i in range(0,len(listP)):
	f.write(listP[i]+':\n')
	f.write(str(func2(table5[listP[i]]))+'\n')
	b=func2(maxTable[listP[i]])
	a=func2(minTable[listP[i]])
	c=dict([(k,[a[k],b[k]]) for k in a])
	f.write(str(c)+'\n')
	f.write(str(tmpT[listP[i]])+'\n')
f.close()






