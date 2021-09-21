# Slice SRE Challenge
# The intent this sidecar is to facilitate the health checking
# and insights gathering functions of the load balancers
# and metrics agents that preceded it.
# In order to do so, this does:
# 1. Poll `/health` on the web service every 10 seconds
# 2. Output the average, minimum, and maximum of each metric every minute to stdout
# 3. Exit with a non-zero exit code if `/health` does not return 200

# Martin Jones, martin@mailpony.uk 
# 20 August, 2021

import requests
import sys
import time
from itertools import count

HEALTHURI='http://127.0.0.1/health'

def main():
    # Initial values
    reqLatencyAvg = 0
    dbLatencyAvg = 0
    cacheLatencyAvg = 0
    reqLatencyMin = 999999
    dbLatencyMin = 999999
    cacheLatencyMin = 999999
    reqLatencyMax = 0
    dbLatencyMax = 0
    cacheLatencyMax = 0

    for i in count(start = 1, step = 1):
        response = requests.get(HEALTHURI)
        # Check the response is 200, if not then exit(1)
        if response.status_code != 200:
            sys.exit(1)
        metrics=response.json()
        # Extract the requests, db and cache metrics
        reqLatency=metrics['metrics']['requestLatency']
        dbLatency=metrics['metrics']['dbLatency']
        cacheLatency=metrics['metrics']['cacheLatency']
        # Caculate the min, max and avg for each metric
        reqLatencyMin= min(reqLatencyMin, reqLatency) 
        dbLatencyMin= min(dbLatencyMin, dbLatency) 
        cacheLatencyMin= min(cacheLatencyMin, cacheLatency) 
        reqLatencyMax= max(reqLatencyMax, reqLatency) 
        dbLatencyMax= max(dbLatencyMax, dbLatency) 
        cacheLatencyMax= max(cacheLatencyMax, cacheLatency) 
        dbLatencyAvg=(dbLatencyAvg*(i-1) + dbLatency)/i 
        cacheLatencyAvg=(cacheLatencyAvg*(i-1) + cacheLatency)/i 
        reqLatencyAvg=(reqLatencyAvg*(i-1) + reqLatency)/i 
        dbLatencyAvg=(dbLatencyAvg*(i-1) + dbLatency)/i 
        cacheLatencyAvg=(cacheLatencyAvg*(i-1) + cacheLatency)/i 

        #Output values to stdout
        # Todo - allow output format to be supplied eg json, yaml, text
        print("Requests min,max,avg: {:.4f},{:.4f},{:.4f}".format(reqLatencyMin,reqLatencyMax,reqLatencyAvg))
        print("DB min,max,avg: {:.4f},{:.4f},{:.4f}".format(dbLatencyMin,dbLatencyMax,dbLatencyAvg))
        print("Cache min,max,avg: {:.4f},{:.4f},{:.4f}".format(cacheLatencyMin,cacheLatencyMax,cacheLatencyAvg))
        sys.stdout.flush()
        time.sleep(10)
    return

if __name__ == "__main__":
    main()
