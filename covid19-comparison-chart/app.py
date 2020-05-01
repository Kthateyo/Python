import sys, getopt
import openpyxl as xl
from data import getJson, dateRange, Date
from utils import adjustWidth, fillWithArray

### Flags and Variables
_days_limit = 0
_starting_count = 100
_type = ''
_file = ''

### Function Definitions

# Align country data, that it starts with starting_count value
def alignFrom(country):
    start = Date(22, 1, 20)
    end = Date(29,4,20)

    if _type == 'confirmed':
        start = Date(22, 1, 2020)
        end = Date(29,4,2020)

    countryDays = []
    i = 0
    for date in dateRange(start, end):
        cases = country[date]
        if int(cases) > _starting_count:
            countryDays.append(cases)
            i += 1
            
            if _days_limit > 0:
                if i >= _days_limit:
                    break
            else:
                pass

    return countryDays

# Add to spreadsheet data of countries
def addCountries(countries):
        # get json of some countries
    data = getJson(_file)

    i = 1
    for country in countries:
        countryData = data[country]
        # align their data to start from 100 confirmed cases
        countryDays = alignFrom(countryData)
        ws.cell(1, i, country)
        fillWithArray(ws, 2, i, countryDays)
        i += 1


def drawChart(sheet):
    values = xl.chart.Reference(sheet, 1, 1, sheet.max_column, sheet.max_row)
    chart = xl.chart.LineChart()
    chart.add_data(values, titles_from_data=True)
    sheet.add_chart(chart, str(sheet.cell(1, sheet.max_column + 3).column_letter) + '3')

# Prints help for usage of program
def printHelp():
    print('')
    print('That console program take data type and list of countries and produces ')
    print('a covid19.xlsx spreadsheet with char comparising those countries.')
    print('')
    print('Usage:')
    print('    python ./app.py <type> [country0, country1, ..]')
    print('')
    print('Example:')
    print('  python ./app.py confirmed Czechia Poland')
    print('  python ./app.py deaths Germany France "Korea, South"')
    print('')
    print('type:')
    print('  confirmed      Data about confirmed cases')
    print('  deaths         Data about deaths')
    print('  recovered      Data about recovered cases')
    print('  countries      Lists available countries')
    print('')
    print('arguments:')
    print('  --days-limit <number>      Limits number of days')
    print('  --starting-count <number>  Number of cases when chart starts with for each country')
    print('')

# Print available countries
def printCoutries():
    data = getJson('time_series_covid19_confirmed_global.csv')
    for country in data:
        print(country)

def checkCountries(countries):
    data = getJson('time_series_covid19_confirmed_global.csv')

    countries = []
    for country in data:
        countries.append(country)

    for arg in args:
        if not arg in countries:
            print('')
            print('\033[1m'+'Propably wrong name of country. Check if you misspelled a name with \'countries\' command'+'\033[0m')
            printHelp()
            exit()

### Program

# Check if arguments are valid, if not print help and terminate app
if len(sys.argv) == 1 or not sys.argv[1] in ['confirmed', 'deaths', 'recovered', 'countries']:
    printHelp()
    exit()

# Set up global variable
_type = sys.argv[1]

# List available countries
if _type == 'countries':
    printCoutries()
    exit()

# Set up global variable
_file = 'time_series_covid19_'+ _type +'_global.csv'

# Get flag arguments
opts, args = getopt.getopt(sys.argv[2:], '', ['days-limit=', 'starting-count='])
for opt, arg in opts:
    if opt == '--days-limit':
        _days_limit = int(arg)
    elif opt == '--starting-count':
        _starting_count = int(arg)

# Check for misspelled names
checkCountries(args)

# create workbook
wb = xl.Workbook()
ws = wb.active

# Get countries from arguments
countries = []
for arg in args:
    countries.append(arg)

# add data to worksheet
addCountries(countries)

# create comparison chart
drawChart(ws)

# save workbook
adjustWidth(ws)
wb.save('covid.xlsx')
