from bs4 import BeautifulSoup
import requests
import json
import sys
import ast
import csv

def getMissingData(toFind):
	url = 'https://autocomplete.clearbit.com/v1/companies/suggest?query='+str(toFind)
	try:
		nextApi = requests.get(url)
		nextApiResp = nextApi.content
		nextApiResp = json.loads(nextApiResp)
		return nextApiResp[0]['domain'].encode('utf-8')
	except:
		return "Couldn't Find value"

pg = 1
totalOut = ''
while pg <=10 :
	tempOut = requests.get("https://angel.co/company_filters/search_data?sort=signal&page="+str(pg))
	tempOut = tempOut.content
	tempOut = json.loads(tempOut)
	val = tempOut['ids']
	paramterstring = ''
	for i in val:
		paramterstring = paramterstring+'ids%5B%5D='+str(i)+'&'

	paramterstring = paramterstring+'page='+str(pg)+'&sort=signal&new=false&hexdigest='+str(tempOut['hexdigest'])

	paramterstring = 'https://angel.co/companies/startups?'+paramterstring

	anotherRequest = requests.get(paramterstring)
	anotherOut = anotherRequest.content

	totalOut = totalOut + anotherOut
	pg += 1
	totalOut=totalOut+'\n'
	
mainList = []
newTitleList = []
newLocationList=[]
newWebsiteList =[]
newSizeList =[]
newRaisedList=[]
newStageList = []
newMarketList=[]
value = totalOut.split('\n')
value.pop(len(value)-1)
for k,i in enumerate(value):

	i=ast.literal_eval(i)
	tree = BeautifulSoup(i['html'],"lxml")
	good_html = tree.prettify()
	
	title = [] 
	elements = BeautifulSoup(good_html,"html.parser").find_all(class_="startup-link")
	for m,v in enumerate(elements):
		if m % 2 == 0:
			title.append((elements[m]['title']).encode('utf-8'))

	
	location =[]
	elements = BeautifulSoup(good_html,"html.parser").find_all(class_="column hidden_column location")
	if k == 0:
		elements.pop(0)

	for i in elements:
		
		newEle = i.find_all(class_="value")

		for j in newEle:
			newEle2 = j.find_all(class_="tag")
			if len(newEle2) == 0:
				location.append("-")	
			else:
				location.append(((newEle2[0].text).encode('utf-8')).strip())
	
	market =[]
	elements = BeautifulSoup(good_html,"html.parser").find_all(class_="column hidden_column market")
	if k == 0:
		elements.pop(0)
	for i in elements:
		
		newEle = i.find_all(class_="value")

		for j in newEle:
			newEle2 = j.find_all(class_="tag")
			if len(newEle2) == 0:
				market.append("-")	
			else:
				market.append(((newEle2[0].text).encode('utf-8')).strip())

	website =[]
	elements = BeautifulSoup(good_html,"html.parser").find_all(class_="column hidden_column website")

	indx = 0
	if k == 0:
		elements.pop(0)

	for i in elements:
	
		newEle = i.find_all(class_="value")
		if len(newEle) is not 0:
			newEle2 = newEle[0].find_all(class_="website")
		else:
			newEle2 = []

		if len(newEle2) == 0:
			
			website.append(getMissingData(title[indx]))	
		else:
			
			website.append(((newEle2[0].text).encode('utf-8')).strip())	
		indx += 1

	size =[]
	elements = BeautifulSoup(good_html,"html.parser").find_all(class_="column company_size hidden_column")
	if k == 0:
		elements.pop(0)
	for i in elements:
		
		newEle = i.find_all(class_="value")
		if (len(newEle)==0):
			size.append("-")
		else:	
			size.append(((newEle[0].text).encode('utf-8')).strip())
	

	stage =[]
	elements = BeautifulSoup(good_html,"html.parser").find_all(class_="column hidden_column stage")
	if k == 0:
		elements.pop(0)
	for i in elements:
		
		newEle = i.find_all(class_="value")
		if (len(newEle)==0):
			stage.append("-")
		else:	
			stage.append(((newEle[0].text).encode('utf-8')).strip())
	

	raised =[]

	elements = BeautifulSoup(good_html,"html.parser").find_all(class_="column hidden_column raised")
	if k == 0:
		elements.pop(0)	


	for i in elements:
		
		newEle = i.find_all(class_="value")
		if len(newEle)==0:
			raised.append("-")
		else:	
			raised.append(((newEle[0].text).encode('utf-8')).strip())

	for i in title:
		newTitleList.append(i)

	for i in market:
		newMarketList.append(i)

	for i in location:
		newLocationList.append(i)

	for i in website:
		newWebsiteList.append(i)

	for i in stage:
		newStageList.append(i)

	for i in size:
		newSizeList.append(i)

	for i in raised:
		newRaisedList.append(i)

index = 0

while index<200:
	tempList = {}
	tempList['companyName']=newTitleList[index]
	tempList['market']=newMarketList[index]
	tempList['location']=newLocationList[index]
	tempList['website']=newWebsiteList[index]	
	tempList['stage']=newStageList[index]
	tempList['raised']=newStageList[index]
	tempList['size']= newSizeList[index]
	mainList.append(tempList)
	index+=1

filename = 'angelList.csv'
with open(filename, 'wb') as f:
    w = csv.DictWriter(f,['companyName','market','location','website','stage','raised','size'])
    w.writeheader()
    for tempList in mainList:
        w.writerow(tempList)
