import time 

class Cronometer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time() 

    def stop(self):
        self.end_time = time.time()

    def print(self):
        duration = self.end_time - self.start_time
        print(f"Total duration: {duration:.2f} seconds")