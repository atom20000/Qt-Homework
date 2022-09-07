import csv
import os


class WorkFile():


    def __init__(self, path):
        self.path = path
    
    def check_exist_file(method):
        
        def check_exec(self):
            if os.path.exists(self.path) and os.path.isfile(self.path):
                return method(self)
            else:
                return None
        return check_exec

    @check_exist_file
    def read(self):
        with open(self.path, 'r') as csvfile:
            csv.reader(csvfile)
    
    @check_exist_file
    def write(self, data):
        with open(self.path, 'w') as csvfile:
            csv.writer(csvfile).writerows(data)
