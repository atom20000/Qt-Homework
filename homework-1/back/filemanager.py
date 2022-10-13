import csv
import os


class WorkFile():

    def __init__(self, path):
        self.path = path
    
    def check_exist_file(method):
        
        def check_exec(self, *args, **kwargs):
            if os.path.exists(self.path) and os.path.isfile(self.path):
                return method(self, *args, **kwargs)
            else:
                return None
        return check_exec

    @check_exist_file
    def read(self):
        with open(self.path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            outdict = {i : [] for i in reader.fieldnames}
            for row in reader:
                for item in row.items():
                     outdict[item[0]].append(item[1])
            return outdict
    
    #@check_exist_file
    def write(self, data: dict, count_rows):
        with open(self.path, 'w') as csvfile:
            filenames = data.keys()
            writer = csv.DictWriter(csvfile, filenames)
            writer.writeheader()
            for r in range(count_rows):
                writer.writerow({i:data[i][r] for i in filenames})
