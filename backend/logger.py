import os

class Logger:
    def __init__(self):
        print("Logger initialized")
        self.logs = []

    def log(self, message):
        self.logs.append(message)
    
    def print_logs(self):
        for log in self.logs:
            print(log)

# Create the singleton instance at the module level
logger = Logger()
