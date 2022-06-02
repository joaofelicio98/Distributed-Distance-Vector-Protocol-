import json
import csv
import os
from datetime import datetime

extension = '.json'

for file in os.listdir('stats'):
    if file.endswith(extension):
        with open('stats/'+file,"r") as f:
            data = json.load(f)

    filtered_data = {}
    node = file.rsplit('_')[0]

    # Filter all data from json file by max timestamp per node/seq_no
    for topo in data:
        filtered_data[topo]={}
        for ntry,list in data[topo].items():
            for n in range(len(list)):
                if n == 0:
                    aux = [list[n]['seq_no']]
                    filtered_data[topo][ntry]=[list[n]]
                elif list[n]['seq_no'] not in aux:
                    aux.append(list[n]['seq_no'])
                    filtered_data[topo][ntry][node].append(list[n])
                else:
                    for i in range(len(filtered_data[topo][ntry])):
                        dict = filtered_data[topo][ntry][i]
                        if dict['seq_no'] == list[n]['seq_no']:
                            time1 = int(dict['time'])
                            time2 = int(list[n]['time'])
                            if time2 > time1 or dict['count'] < list[n]['count']:
                                filtered_data[topo][ntry][i] = list[n]
                            break

    final_list = []
    # Transfer dict to a list with all parameters
    for topo in filtered_data:
        for ntry,list in filtered_data[topo].items():
            for dict in list:
                aux=[]
                for key,value in dict.items():
                    aux.append(value)
                final_list.append([topo,ntry,node]+aux)

    #print(final_list)
    fields = ['Topology', 'Try', 'Node', 'Sequence Number', 'Timestamp', 'States Count']
    if not(os.path.isfile('results.csv')):
        with open('results.csv', 'w') as csvfile:
            # Create csv writer object
            csvwriter = csv.writer(csvfile)
            # Write the fields
            csvwriter.writerow(fields)
            # Write data
            csvwriter.writerows(final_list)
    else:
        with open('results.csv', 'a') as csvfile:
            # Create csv writer object
            csvwriter = csv.writer(csvfile)
            # Write data
            csvwriter.writerows(final_list)
