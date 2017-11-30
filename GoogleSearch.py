from bs4 import BeautifulSoup
import requests
import re
import csv

foundersList = {}


def csv_dict_reader(file_obj):
    reader = csv.DictReader(file_obj, delimiter=',')
    for line in reader:
        getFounders(line["companyName"][2:-1])


def getFounders(companyName):
    googleRequest = 'https://www.google.co.in/search?q=' + companyName + ' company founders linkedin'
    googleSearchResult = requests.get(googleRequest)
    googleSearchResult = googleSearchResult.content

    tree = BeautifulSoup(googleSearchResult, "lxml")
    names = tree.find_all('h3', class_='r')[:10]
    details = tree.find_all("span", {'class': 'st'})[:10]

    founderDetailsDict = generateDataDictionary(names, details)
    getFounderNames(founderDetailsDict, companyName)
    writeToCsv()


def generateDataDictionary(names, details):
    nameList = []
    founderDetailsDict = {}

    ind = 0

    for name in names:
        founderName = BeautifulSoup(name.__str__(), "lxml")
        nameList.append(founderName.get_text().lower())

    for data in details:
        founderDetails = BeautifulSoup(data.__str__(), "lxml")
        founderDetailsDict[nameList[ind]] = founderDetails.get_text().lower()
        ind += 1

    return founderDetailsDict


def getFounderNames(founderDetailsDict, companyName):
    regex = re.compile('[^a-zA-Z ]')

    foundersList['CompanyName'] = companyName
    founderString = ''

    for key, value in founderDetailsDict.items():
        key = regex.sub('', key)
        value = regex.sub('', value)

        data = value.split()

        if ('founder') and companyName.lower() in data:
            if not (companyName.lower() in key.split()[0]) and not (companyName.lower() in key.split()[1]):
                founderString += key.split()[0] + " " + key.split()[1] + ", "
        foundersList['Founders'] = founderString


def writeToCsv():
    filename = 'Founders.csv'
    with open(filename, 'a') as f:
        w = csv.DictWriter(f, ['CompanyName', 'Founders'])
        w.writerow(foundersList)
        f.close()


filename = 'Founders.csv'
with open(filename, 'w') as f:
    w = csv.DictWriter(f, ['CompanyName', 'Founders'])
    w.writeheader()
    f.close()
with open("angelList.csv") as f:
    csv_dict_reader(f)
