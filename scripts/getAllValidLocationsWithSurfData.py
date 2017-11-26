import sys
import requests

with open(sys.argv[1], 'r') as f:
    for line in f.readlines():
        locationKey = line.split(',')[0]

        try:
            response = requests.get('http://api.surfline.com/v1/forecasts/'+str(locationKey)+'?resources=surf,analysis&days=1&getAllSpots=false&units=e&interpolate=false&showOptimal=false',verify=True)
            info = response.json()
        except KeyboardInterrupt:
            raise
        except:
            print 'Error for locationKey ' + str(locationKey)

        if ('Analysis' in info and 'generalCondition' in info['Analysis'] and info['Analysis']['generalCondition']):
            print str(locationKey) + ',' + info['name'].encode('utf-8')
