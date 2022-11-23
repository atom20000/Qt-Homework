import os
import json


class JsonParser():

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
        with open(self.path, 'r') as jsonfile:
            return json.load(jsonfile)
    