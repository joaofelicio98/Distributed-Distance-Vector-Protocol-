import json
from datetime import datetime

class stats_API():

    def __init__(self, ntry, topology):
        self.ntry = str(ntry)
        self.topo = topology

        # All data to store
        self.data = {self.topo:{self.ntry:{}}}

    def insert_new_value(self, node, seq_no, count, timestamp):
        #self.data
        temp ={
                "seq_no":seq_no,
                "time":timestamp,
                "count":count
                }

        try:
            with open("stats.json","r") as f:
                # Read json file
                self.data = json.load(f)
            # Adding new stat and converting data to json format
            if node in self.data[self.topo][self.ntry]:
                self.data[self.topo][self.ntry][node].append(temp)
            else:
                self.data[self.topo][self.ntry][node] = [temp,]
            json_object = json.dumps(self.data, indent=4, default=str)

            with open("stats.json","w") as f:
                # Writing updated stats
                f.write(json_object)
            return self.data

        # File doesn't exist => create one
        except FileNotFoundError:
            with open("stats.json","w") as f:
                # Adding new stat and converting data to json format
                self.data[self.topo][self.ntry][node] = [temp,]
                json_object = json.dumps(self.data, indent=4, default=str)

                f.write(json_object)
            return self.data

    def get_current_stats(self):
        return self.data

if __name__ == "__main__":
    obj = stats_API(1, "test_topo")

    now = datetime.now()
    obj.insert_new_value("s1", 1, 34, now)
    obj.insert_new_value("s2", 2, 54, now)
    obj.insert_new_value("s1", 3, 36, now)
    print(obj.get_current_stats())
    obj.insert_new_value("s1", 34, 3, now)
    obj.insert_new_value("s2", 4, 54, now)
    obj.insert_new_value("s1", 6, 36, now)
