import inspect
import os
import requests
import json
from pathlib import Path
import sys

# to detect where am I, in order to find config file
filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))
configFilePath = path+'/config.json'

if __name__ == "__main__":
    url = ""
    headers = {}
    configfd = None
    try:
        configfd = open(configFilePath)
        config = json.load(configfd)

        url = config['url']

        # Lsky Pro's V2 api
        # But don't set Content-Type, it sucks
        headers = {
            "Authorization": "Bearer "+config['token'],"Accept":"application/json",
            #"Content-Type":"multipart/form-data"
        }

        # for Typora, it passes photo file names as args to this program
        # and then reads urls one per line back
        result = []
        for i in range(1,len(sys.argv)):
            
            # P(hoto)file
            Pfile = Path(sys.argv[i])

            # same as curl --form "file=@file_path"
            data = {
            "file" :(Pfile.name,open(Pfile,'rb'),'image/png')
            }

            # here we make the request
            r = requests.post(url,headers=headers,files=data)

            # get response body and parse as json
            rsp = r.json()

            # if status is True, extract the url and push into the result array, waiting for the final output
            if rsp['status'] == True:
                result.append(rsp['data']['links']['url'])
        
        # print one per line to satisfy Typora
        print(*result, sep = "\n")
    except:
        exit(-1)
    finally:
        configfd.close()