import inspect
import os
import requests
import json
import hashlib
from pathlib import Path
import sys

def get_hash_memory_optimized(f_path, mode='md5'):
    h = hashlib.new(mode)
    with open(f_path, 'rb') as file:
        block = file.read(512)
        while block:
            h.update(block)
            block = file.read(512)

    return h.hexdigest()

filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))
configFilePath = path+'/config.json'

if __name__ == "__main__":

    configfd = open(configFilePath)
    config = json.load(configfd)

    url = config['url']

    headers = {
        "Authorization": "Bearer "+config['token'],"Accept":"application/json",
        #"Content-Type":"multipart/form-data"
    }

    configfd.close()

    result = []
    for i in range(1,len(sys.argv)):

        Pfile = Path(sys.argv[i])

        hashf = get_hash_memory_optimized(sys.argv[i])

        data = {
        "file" :(Pfile.name,open(Pfile,'rb'),'image/png')
        }

        r = requests.post(url,headers=headers,files=data)

        rsp = r.json()

        if rsp['status'] == True:
            result.append(rsp['data']['links']['url'])

    print(*result, sep = "\n")