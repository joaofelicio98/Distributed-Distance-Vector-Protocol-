import json
import csv
from datetime import datetime

with open("stats.json","r") as file:
    data = json.load(file)

filtered_data = {}

# Filter all data from json file by max timestamp per node/seq_no
for topo in data:
    filtered_data[topo]={}
    for ntry in data[topo]:
        filtered_data[topo][ntry]={}
        for node,list in data[topo][ntry].items():
            for n in range(len(list)):
                if n == 0:
                    aux = [list[n]['seq_no']]
                    filtered_data[topo][ntry][node]=[list[n]]
                elif list[n]['seq_no'] not in aux:
                    aux.append(list[n]['seq_no'])
                    filtered_data[topo][ntry][node].append(list[n])
                else:
                    for i in range(len(filtered_data[topo][ntry][node])):
                        dict = filtered_data[topo][ntry][node][i]
                        if dict['seq_no'] == list[n]['seq_no']:
                            time1 = datetime.strptime(dict['time'],"%H:%M:%S")
                            time2 = datetime.strptime(list[n]['time'],"%H:%M:%S")
                            if time2 > time1 or dict['count'] < list[n]['count']:
                                filtered_data[topo][ntry][node][i] = list[n]
                            break

final_list = []
# Transfer dict to a list with all parameters
for topo in filtered_data:
    for ntry in filtered_data[topo]:
        for node,list in filtered_data[topo][ntry].items():
            for dict in list:
                aux=[]
                for key,value in dict.items():
                    aux.append(value)
                final_list.append([topo,ntry,node]+aux)

#print(final_list)
fields = ['Topology', 'Try', 'Node', 'Sequence Number', 'Timestamp', 'States Count']
with open('results.csv', 'w') as csvfile:
    # Create csv writer object
    csvwriter = csv.writer(csvfile)
    # Write the fields
    csvwriter.writerow(fields)
    # Write data
    csvwriter.writerows(final_list)
