from resources.globals import time, threading

class BaseService:
    name = 'base'
    name_key = "_"
    desc_key = "_"
    interval = 10 # in seconds, can be set by 

    def __init__(self, args=None):
        self._stop_event = threading.Event()
        self.start_time = time.time()
        self.thread = None
        if args == None:
            args = {}
        
        if args.get("interval", None) != None:
            self.interval = args.get("interval", None)

    def start(self, args=None):
        self.args = args
        if self.thread is None:
            self.thread = threading.Thread(target=self.action_wrapper)
            self.thread.start()
    
    def action_wrapper(self):
        while not self._stop_event.is_set():
            print('Service "{0}" called action, sleeping for {1}s'.format(self.name, self.interval))
            self.action()
            time.sleep(self.interval)
    
    def stop(self):
        self._stop_event.set()
        if self.thread is not None:
            self.thread.join()
            self.thread = None
    
    def action(self):
        pass
    
    def describe(self):
        return {
            "id": self.name,
            "name": getattr(self, "name_key", "_"),
            "description": getattr(self, "desc_key", "_"),
            "interval": self.interval,
        }
