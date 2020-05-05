import csv, requests, eel, datetime

#####################
## Variables

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

_data = {
    'confirmed': '',
    'deaths': '',
    'recovered': '',
    'active': ''
}

population = {}

class Date:
    day = 0
    month = 0
    year = 0

    def __init__(self, day = 0, month = 0, year = 0):
        self.day = day
        self.month = month
        self.year = year
    
    def start(self):
        self.day = 22
        self.month = 1
        self.year = 20
        return self

    def today(self):
        today = datetime.date.today()
        end = Date(int(today.strftime('%d')), int(today.strftime('%m')), int(today.strftime('%y')))
        return end


#####################
## Functions

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
    

# Returns population of given country
def getPopulation(countryName):
    
    if countryName == 'US':
        countryName = 'USA'
    elif countryName == 'Czechia':
        countryName = 'Czech'
    elif countryName == 'Korea, South':
        countryName = 'Korea%20(Republic%20of)'
    countryName = countryName.replace(' ', '%20')

    if countryName in population:
        return population[countryName]
    
    data = requests.get('https://restcountries.eu/rest/v2/name/' + countryName).json()
    population[countryName] = data[0]['population']
    return data[0]['population']


def prepareData(_type):
    if _data[_type] == '':
        if _type == 'active':
            prepareData('confirmed')
            prepareData('deaths')
            prepareData('recovered')
            _data['active'] = {}
            for country in _data['confirmed']:
                _data['active'][country] = {}
                for date in dateRange(Date().start(), Date().today()):
                    if date not in _data['confirmed'][country]:
                        break
                    confirmed = _data['confirmed'][country][date]
                    deaths = _data['deaths'][country][date]
                    recovered = _data['recovered'][country][date]
                    _data['active'][country][date] = str(int(confirmed) - int((int(deaths) + int(recovered))))
        else:
            url = 'https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_'+_type+'_global.csv&filename=time_series_covid19_'+_type+'_global.csv'
            print('Downloading Data...')
            r = requests.get(url)

            _json = {}
            csvReader = csv.DictReader(r.text.split('\n'))
            for rows in csvReader:
                id = rows['Country/Region']
                if id in _json:

                    toPass = 4
                    for col in _json[id]:
                        if toPass > 0:
                            toPass -= 1
                            pass
                        else:
                            _json[id][col] = int(_json[id][col]) + int(rows[col])
                else:
                    _json[id] = rows
            _data[_type] = _json


def alignFrom(country, countryName, _starting_count, _perMillion, _days_limit):
    start = Date(22, 1, 20)
    end = Date().today()

    countryPopulation = getPopulation(countryName)
    countryDays = []
    i = 0
    for date in dateRange(start, end):
        if date not in country:
            break
        cases = int(country[date])
        if cases >= _starting_count:
            if _perMillion == True:
                countryDays.append( cases / (countryPopulation / 1000000) )
            else:
                countryDays.append(cases)
            i += 1

            if _days_limit > 0:
                if i >= _days_limit:
                    break

    return countryDays

#####################
## Exposed Functions

@eel.expose
def getAllCountries():
    prepareData('confirmed')
    countries = []
    for country in _data:
        countries.append(country)
    return countries


@eel.expose
def getData(t_type, countries, align, per_million, start_from, days_limit):

    eel.signalizeState('Getting data..')
    prepareData(t_type)
    
    returnData = {
        'labels': [],
        'data': []
    }

    if align:
        numberOfDays = 0

    i = 1
    for country in countries:
        state = str(i)+'/'+str(len(countries)) + ' ' + str(country)
        eel.signalizeState(state)
        print('                                     ', end='\r')
        print(state, end='\r')

        countryData = _data[t_type][country]
        # align their data to start from 100 confirmed cases
        if align:
            countryDays = alignFrom(countryData, country, start_from, per_million, days_limit)
            if(len(countryDays) > numberOfDays):
                numberOfDays = len(countryDays)
            returnData['data'].append(countryDays)
        else:
            countryDays = alignFrom(countryData, country, 0, per_million, 0)
            returnData['data'].append(countryDays)
        i += 1
    
    if align:
        for i in range(1,numberOfDays+1):
            returnData['labels'].append(str(i))
    else:
        start = Date(22, 1, 20)
        # today = datetime.date.timetuple()
        # end = Date(today.day,today.month, int(str(today.year)[2:]))
        returnData['labels'] = dateRange(start, Date().today())

    print('')
    eel.signalizeState('Done')
    
    return returnData
