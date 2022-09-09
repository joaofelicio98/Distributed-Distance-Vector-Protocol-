import json
import csv
import os
from datetime import datetime

extension = '.json'
filtered_data = {}

for file in os.listdir('stats'):
    if file.endswith(extension):
        with open('stats/'+file,"r") as f:
            data = json.load(f)

    node = file.rsplit('_')[0]

    # Filter all data from json file by max timestamp per node/seq_no
    for topo in data:
        if topo not in filtered_data:
            filtered_data[topo]={}
        for ntry,list in data[topo].items():
            if ntry not in filtered_data[topo]:
                filtered_data[topo][ntry] = {}
            if node not in filtered_data[topo][ntry]:
                filtered_data[topo][ntry][node] = {}
            for n in range(len(list)):
                aux = list[n]['seq_no']
                if aux not in filtered_data[topo][ntry][node]:
                    filtered_data[topo][ntry][node][aux]=[list[n],]
                elif len(filtered_data[topo][ntry][node][aux]) == 1:
                    if list[n]['time'] < filtered_data[topo][ntry][node][aux][0]['time']:
                        filtered_data[topo][ntry][node][aux].append(filtered_data[topo][ntry][node][aux][0])
                        filtered_data[topo][ntry][node][aux][0] = list[n]
                    else:
                        filtered_data[topo][ntry][node][aux].append(list[n])
                elif list[n]['time'] < filtered_data[topo][ntry][node][aux][0]['time']:
                    filtered_data[topo][ntry][aux][0] = list[n]
                elif list[n]['time'] > filtered_data[topo][ntry][node][aux][1]['time']:
                    filtered_data[topo][ntry][node][aux][1] = list[n]

final_list = []
# Transfer dict to a list with all parameters
for topo in filtered_data:
    for ntry in filtered_data[topo]:
        for node in filtered_data[topo][ntry]:
            for seq_no,list in filtered_data[topo][ntry][node].items():
                for dict in list:
                    aux=[]
                    for key,value in dict.items():
                        aux.append(value)
                    final_list.append([topo,ntry,node]+aux)


fields = ['Topology', 'Try', 'Node', 'Sequence Number', 'Timestamp', 'States Count']
#if not(os.path.isfile('results.csv')):
with open('results.csv', 'a') as csvfile:
    # Create csv writer object
    csvwriter = csv.writer(csvfile)
    # Write the fields
    csvwriter.writerow(fields)
    # Write data
    csvwriter.writerows(final_list)