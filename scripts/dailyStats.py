import sys
import pandas as pd

ratings = ['flat', 'very poor', 'poor', 'poor to fair', 'fair', 'fair to good','good','very good']

data = pd.read_csv(sys.argv[1])
locations = pd.read_csv(sys.argv[2], header=None, names=['locKey', 'names'])

dailySurfMax = data[data['surfMax'] == data['surfMax'].max()]
dailyMaxLocKey =  dailySurfMax['locKey'].values[0]
dailyMaxLocationName = locations.loc[locations['locKey'] == dailyMaxLocKey]['names'].values[0]
dailySurfMinMean = data['surfMin'].mean()
dailySurfMaxMean = data['surfMax'].mean()

print 'Today\'s biggest surf is in {0} with a surf range of {1} to {2} feet.'.format(dailyMaxLocationName, dailySurfMax['surfMin'].values[0], dailySurfMax['surfMax'].values[0])
print 'Today\'s average surf range is {0:0.2f} to {1:0.2f} feet.'.format(dailySurfMinMean, dailySurfMaxMean)

todaysConditions = 'Today, around the world their are\n'
for rating in ratings:
    todaysConditions += '{0}\t{1} surf breaks.\n'.format(len(data[data['generalCondition'] == rating]), rating)
print todaysConditions
