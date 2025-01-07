import time

class Timeline:
    def __init__(self):
        self.start_time = None
        self.times = {}
        self.elapsed_time = None
    
    def start(self):
        self.start_time = time.time()

    def register(self, name):
        self.times[name] = time.time() - self.start_time
        print(f'Register {self.times[name]}')
    
    def recovery(self, name):
        return self.times[name]
    
    def wait(self, name, second):
        time.sleep(second)  
        self.times[name] = time.time() - self.start_time
        print(f'Waited {self.times[name]}')

    def stop(self):
        self.elapsed_time = time.time() - self.start_time
        print(f'Stoped {self.elapsed_time}')

    def get_elapsed_time(self):
        return self.elapsed_time