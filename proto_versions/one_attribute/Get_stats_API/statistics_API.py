import json
from datetime import datetime
import os

class stats_API():

    def __init__(self, sw_name, ntry, topology):
        self.sw_name = sw_name
        self.ntry = str(ntry)
        self.topo = topology

        # All data to store
        self.data = {self.topo:{self.ntry:{}}}

    def insert_new_value(self, seq_no, count, timestamp):
        #self.data
        temp ={
                "seq_no":seq_no,
                "time":timestamp,
                "count":count
                }

        if not (os.path.isdir(os.path.join(os.getcwd(), 'stats'))):
            os.mkdir(os.path.join(os.getcwd(), 'stats'))

        try:
            with open(f"stats/{self.sw_name}_stats.json","r") as f:
                # Read json file
                self.data = json.load(f)

            if self.topo not in self.data:
                self.data[self.topo] = {}
            if self.ntry not in self.data[self.topo]:
                self.data[self.topo][self.ntry] = []
            # Adding new stat and converting data to json format
            self.data[self.topo][self.ntry].append(temp)
            json_object = json.dumps(self.data, indent=4, default=str)

            with open(f"stats/{self.sw_name}_stats.json","w") as f:
                # Writing updated stats
                f.write(json_object)
            return self.data

        # File doesn't exist => create one
        except FileNotFoundError:
            with open(f"stats/{self.sw_name}_stats.json","w") as f:
                # Adding new stat and converting data to json format
                self.data[self.topo][self.ntry] = [temp,]
                json_object = json.dumps(self.data, indent=4, default=str)

                f.write(json_object)
            return self.data

    def get_current_stats(self):
        return self.data

if __name__ == "__main__":
    obj = stats_API('s3', 1, "Abilene")

    now = datetime.now()
    obj.insert_new_value(1, 4, now)
    obj.insert_new_value(2, 5, now)
    obj.insert_new_value(3, 6, now)
    print(obj.get_current_stats())
