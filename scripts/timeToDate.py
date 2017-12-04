import sys
import time

f = sys.argv[1].replace('_','.')
print time.ctime(float(f))