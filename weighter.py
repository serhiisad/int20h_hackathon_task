import json

import glob
import math
import ntpath


path = '/home/pestis/PycharmProjects/24int_mainevent/clusters/*.json'
files=glob.glob(path)
list_weights = []
for file in files:
    with open(file, 'r') as f:
        str = f.read()
        data = json.loads(str)
        num = math.log(len(data), 2)
        print(num)
        list_weights.append({ntpath.basename(file): num})

f = open("weighted", "w")
f.write(json.dumps(list_weights))
