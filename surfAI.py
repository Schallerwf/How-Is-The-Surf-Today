import urllib2
import requests
import time
import re
import os 
import json
from subprocess import call

currentDirectory = os.path.dirname(os.path.realpath(__file__))

now = time.time()
nowString = time.strftime('%Y-%m-%d', time.localtime(now))

repeatedSurfFieldnames = ['swell_period', 'swell_direction', 'swell_height']
surfFieldNames = ['surf_max', 'surf_min']
analysisFieldNames = ['surfMin', 'surfMax','generalCondition']

def stripHtmlTags(text):
    return re.sub('<[^<]+?>', '', text.replace('&#160;', ''))

def parseSurfData(info, locKey, writeHeader):
    print 'Parsing data for ' + info['name']

    csvHeader = 'locKey'
    csvResult = locKey
    surf = info['Surf']
    analysis = info['Analysis']

    updatedAt = analysis['startDate_GMT']
    # Convert both timestamps to gmt before comparison, to avoid platform dependant time issues.
    # Divide time difference by number of seconds in an hour to get diff in days
    if ((time.mktime(time.gmtime(now)) - time.mktime(time.gmtime(updatedAt))) / (60 * 60 * 24) > 2):
        raise ValueError('Data is more than two days old. Throwing away.')

    # All of the fields in the 'Analysis' struct are lists of size one
    for field in analysisFieldNames:
        csvHeader += ',' + field
        if field in analysis and len(analysis[field]) > 0:
            csvResult += ',' + str(analysis[field][0])
        else:
            csvResult += ','

    # Most of the fields in the 'Surf' struct are a one item 'list' that contain
    # another list of 4 values
    for field in surfFieldNames:
        csvHeader += ',{0}_0,{0}_1,{0}_2,{0}_3'.format(field)
        if field not in surf:
            csvResult += ',{0}_0,{0}_1,{0}_2,{0}_3'.format('null')
        else:
            csvResult += ',' + ','.join(str(i) for i in surf[field][0])

    # Most of the fields in the 'Surf' struct are a one item 'list' that contain
    # another list of 4 values. 
    for field in repeatedSurfFieldnames:
        # The 3 sets of values appear to be for other nearby locations
        for v in range(1,3):
            fieldName = field+str(v)
            csvHeader += ',{0}_0,{0}_1,{0}_2,{0}_3'.format(fieldName)
            if field not in surf:
                csvResult += ',' + ','.join(str(i) for i in surf[fieldName][0])
            else:
                csvResult += ',{0}_0,{0}_1,{0}_2,{0}_3'.format('null')

    if writeHeader:
        return csvHeader + '\n' + csvResult
    
    return csvResult


with open(currentDirectory + '/txt/validLocationKeysWithSurfData', 'r') as f:
    lines = f.readlines()

for line in lines:
    locKey, locName = line.split(',')

    try: 
        response = requests.get('http://api.surfline.com/v1/forecasts/'+str(locKey)+'?resources=surf,analysis&days=1&getAllSpots=false&units=e&interpolate=false&showOptimal=false',verify=True)
        info = response.json()
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print 'Error while getting data for location ' + locKey + '.\n\t' + str(e)
        continue

    dataReadMode = 'a'
    dataFileName = currentDirectory + '/data/' + nowString + 'surfData.csv'

    if not os.path.isfile(dataFileName):
        dataReadMode = 'w+'

    try:
        data = parseSurfData(info, locKey, dataReadMode == 'w+')
    except Exception as e:
        print 'Error while parsing json blob.\n' + str(info) + '\n' + str(e)
        continue

    with open(dataFileName, dataReadMode) as output:
        output.write(data + '\n') 
