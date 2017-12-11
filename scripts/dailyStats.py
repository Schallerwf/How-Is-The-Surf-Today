import sys
import pandas as pd
import datetime

def safeBlank(s):
    if pd.isnull(s):
        return ""
    return s

# this is actually really hard to do, given 
# the way surfline builds their links. 
def linkFromLocKey(locKey):
    return ""


tableHeader = """
<tr> 
    <th>Location</th>
    <th>Minumum Surf</th>
    <th>Max Surf</th>
    <th>Condition</th>
</tr>
"""
tableRowTemplate= """
<tr>
    <td>{0}</td>
    <td>{1}</td>
    <td>{2}</td>
    <td>{3}</td>
</tr>
"""

if len(sys.argv) != 5:
    print 'python dailyStats.py <daily_data.csv> <loc_to_name.csv> <html_template> <output_dest>'

ratings = ['flat', 'very poor', 'poor', 'poor to fair', 'fair', 'fair to good','good','very good']
templateReplacements = []

data = pd.read_csv(sys.argv[1])
locations = pd.read_csv(sys.argv[2], header=None, names=['locKey', 'names'])

dailySurfMax = data[data['surfMax'] == data['surfMax'].max()]
dailyMaxLocKey =  dailySurfMax['locKey'].values[0]
dailyMaxLocationName = locations.loc[locations['locKey'] == dailyMaxLocKey]['names'].values[0]
dailySurfMinMean = data['surfMin'].mean()
dailySurfMaxMean = data['surfMax'].mean()

templateReplacements.append(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
templateReplacements.append(dailyMaxLocationName)
templateReplacements.append(linkFromLocKey(dailyMaxLocKey))
templateReplacements.append(dailySurfMax['surfMin'].values[0])
templateReplacements.append(dailySurfMax['surfMax'].values[0])
templateReplacements.append('{0:0.2f}'.format(dailySurfMinMean))
templateReplacements.append('{0:0.2f}'.format(dailySurfMaxMean))

for rating in ratings:
    templateReplacements.append(len(data[data['generalCondition'].str.lower() == rating]))

table = tableHeader
for index, row in data.iterrows():
    location = locations.loc[locations['locKey'] == row['locKey']]['names'].values[0]
    table += tableRowTemplate.format(location, safeBlank(row['surfMin']), safeBlank(row['surfMax']), safeBlank(row['generalCondition']).lower())

templateReplacements.append(table)

with open(sys.argv[3], 'r') as template:
    templateHTML = template.read()
    ndx = 0
    for arg in templateReplacements:
        templateHTML = templateHTML.replace('{' + str(ndx) + '}', str(arg))
        ndx += 1

    with open(sys.argv[4], 'w+') as output:
        output.write(templateHTML);
        

