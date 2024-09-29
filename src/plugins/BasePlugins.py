import time
import threading
from components.settings import settings

class BasePlugin():
    pass

class BaseUploadPlugin(BasePlugin):
    name = 'BasePlugin'
    works = 'all'

    def show_window(self):
        pass

    def run(self, input_data=None):
        pass

    def run_file(self, input_data=None):
        pass

class BaseActionPlugin(BasePlugin):
    name = 'BasePlugin'
    allow_extensions = ['non']
    allow_type = 'entity'
    action = 'r'
    works = 'all'

    def run(self, input_entity=None):
        pass

class BaseDisplayPlugin(BasePlugin):
    name = 'Base'

class BaseService(BasePlugin):
    name = 'BaseService'
    interval = 60
    def __init__(self):
        self._stop_event = threading.Event()
        self.start_time = time.time()
        self.thread = None
    
    def start(self, input_data=None):
        self.input_data = input_data
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
    
    def setParam(self, setting, value):
        return settings.set(setting, value)
    
    def getParam(self, setting):
        return settings.get(setting)
