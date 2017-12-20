# This file is an absolutly disgusting hack, 
# which uses git as a way to update a static web page every day. 

from subprocess import call
import time
import os
from secret import thisDir

pwd = thisDir
now = time.time()
today = time.strftime('%Y-%m-%d', time.localtime(now))

print pwd
os.chdir(pwd)

# Run update script to generate HTMl
call(["python", "scripts/dailyStats.py", "data/"+today+"_surfData.csv", "txt/validLocationKeysWithSurfData", "html/index.html_template", "how-is-the-surf-today.html"])

# Add, commit, and push index file.
call(["git", "add", "how-is-the-surf-today.html"])
call(["git", "commit", "-m" "Automated commit updating index.html with todays surf report."])
call(["./push.exp"])