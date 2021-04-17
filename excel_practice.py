import pandas
from collections import defaultdict

def getListed(filepath,sheet):
	df = pandas.read_excel(filepath,sheet)
	out = []
	for sl in range(df.shape[0]):
		temp = []
		for head in df.columns:
			temp1 = df[head][sl]
			if type(temp1)!=str and str(temp1)!="":
				temp1 = str(int(temp1))
			if temp1.find(',')!=-1 and str(temp1)!="":
				inside = tagSeparation(temp1)
				temp.append(inside)
			else:
				temp.append(temp1)
		out.append(temp)
	return out

def tagSeparation(tagStr):
	return tagStr.split(",")
	
def regionSorter(path,sheet):
	df = pandas.read_excel(path,sheet)
	rn = []
	for i in range(df.shape[0]):
		temp=[]
		for j in ['region','subnet_name']:
			temp.append(df[j][i])
		rn.append(temp)
	temp = defaultdict(list)
	for key, val in rn: 
    		temp[key].append(val) 
	res = dict((key, tuple(val)) for key, val in temp.items()) 
	return res
	
def listzones(path,sheet):
	df = pandas.read_excel(path,sheet)
	zn = {''}
	for i in range(df.shape[0]):
		zn.add(df['zone'][i])
	return list(zn)[1:]
