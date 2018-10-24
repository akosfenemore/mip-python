'''
Create a logging framework to collect all the logs into a single file .Please follow all the tasks below.

 - Make the logger customisable, with settings being retrieved from a configuration file
 - Create the logging framework; every time the logger is invoked, it should log into a single file
 - The logging format has to be generic with the module_name, function_name, line_no : message
'''


import os.path
import json
import logging
import logging.config


class CustomLogger:

    def __init__(self):
        path = os.path.dirname(__file__) + '/log_config.json'
        if os.path.exists(path):
            with open(path, 'r') as f:
                config = json.load(f)
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('mylog')





