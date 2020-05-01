import csv, json, os, requests
import openpyxl as xl
from utils import getAbsolutePath

monthsDays = {
    1:31,
    2:29,
    3:31,
    4:30,
    5:31,
    6:30,
    7:31,
    8:31,
    9:30,
    10:31,
    11:30,
    12:31
}

class Date:
    day = 0
    month = 0
    year = 0

    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

def dateRange(start, end):
    day = start.day
    month = start.month
    year = start.year

    table = []
    while year <= end.year and (month <= end.month or year < end.year) and (day <= end.day or month < end.month):
        
        table.append(str(month)+'/'+str(day)+'/'+str(year))
        day += 1
        
        if day > monthsDays[month]:
            month += 1
            day = 1
            if month > 12:
                year += 1
                month = 1
    return table


def getJson(filename):
    data = {}
    abs_file_path = getAbsolutePath(filename)
    with open(abs_file_path) as csvFile:
        
        csvReader = csv.DictReader(csvFile)
        for rows in csvReader:
            id = rows['Country/Region']
            
            if id in data:

                toPass = 4
                for col in data[id]:
                    if toPass > 0:
                        toPass -= 1
                        pass
                    else:
                        data[id][col] = int(data[id][col]) + int(rows[col])
            else:
                data[id] = rows
    return data
    

# Returns population of given country
def getPopulation(countryName):
    

    if countryName == 'US':
        countryName = 'USA'
    elif countryName == 'Czechia':
        countryName = 'Czech'
    elif countryName == 'Korea, South':
        countryName = 'Korea%20(Republic%20of)'

    countryName = countryName.replace(' ', '%20')

    print(countryName, end=' ')
    data = requests.get('https://restcountries.eu/rest/v2/name/' + countryName).json()
    print(data[0]['population'] / 1000000)
    return data[0]['population']
