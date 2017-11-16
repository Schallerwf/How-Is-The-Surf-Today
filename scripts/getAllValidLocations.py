import requests
import re

for locationKey in range(0,9999):
    try:
        response = requests.get('http://api.surfline.com/v1/forecasts/'+str(locationKey)+'?resources=surf,analysis&days=1&getAllSpots=false&units=e&interpolate=false&showOptimal=false',verify=True)
        info = response.json()
    except KeyboardInterrupt:
        raise
    except:
        print 'Error for locationKey ' + str(locationKey)

    # A 'valid' location is a location that contains swell data. 
    # Here I just check one field in the json response contains swell data.
    if ('Surf' in info and 'swell_direction1' in info['Surf'] and info['Surf']['swell_direction1']):
        print str(locationKey) + ',' + info['name'].encode('utf-8')    