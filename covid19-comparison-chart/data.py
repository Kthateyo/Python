import csv, json, os, requests, pathlib, time
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


# Get csv file from the internet
def getCSV(_type):

    # Check for existing file
    filename = 'time_series_covid19_' + _type + '_global.csv'
    path = pathlib.Path(__file__).parent / 'cache'
    filepath = path / filename


    # if yes, decide if get csv again
    isGonnaDownload = False
    if path.exists():
        if filepath.exists():
            difference_time = (time.time() - filepath.stat().st_mtime) / 60 # Difference time in minutes
            if difference_time > 10:
                isGonnaDownload = True
            else:
                isGonnaDownload = False              
        else:
            isGonnaDownload = True
    else:
        isGonnaDownload = True
        path.mkdir()

    if isGonnaDownload:
        # Get csv from Internet
        url = 'https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_'+_type+'_global.csv&filename=time_series_covid19_'+_type+'_global.csv'
        print('Downloading Data...')
        r = requests.get(url)
        
        # Save it
        if filepath.exists():
            filepath.unlink()
        filepath.touch()
        filepath.write_bytes(r.content)
    
    return filepath


def getJson(_type):
    data = {}
    filepath = getCSV(_type)
    with open(filepath.resolve()) as csvFile:
        
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

    data = requests.get('https://restcountries.eu/rest/v2/name/' + countryName).json()
    return data[0]['population']

