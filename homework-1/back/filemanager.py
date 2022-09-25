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
            #with open('coors.csv', mode='r') as infile:
            #    reader = csv.reader(infile)
            #    with open('coors_new.csv', mode='w') as outfile:
            #        writer = csv.writer(outfile)
            #        mydict = {rows[0]:rows[1] for rows in reader}
    
    @check_exist_file
    def write(self, data):
        with open(self.path, 'w') as csvfile:
            csv.writer(csvfile).writerows(data)

if __name__ == '__main__':
    print(WorkFile('/home/atom/Qt-Homework/homework-1/back/addresses.csv').read())