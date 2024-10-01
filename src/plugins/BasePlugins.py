import time
import threading
from components.settings import settings

class BasePlugin():
    inner_type = 'base'
    name = 'BasePlugin'

    def run(self, input_data=None):
        pass
    
    def getDesc(self):
        return {
            'name': self.name
        }

class BaseUploadPlugin(BasePlugin):
    inner_type = 'upload'
    name = 'BasePlugin'
    works = 'all'
    category = 'base'

    def run(self, input_data=None):
        pass

    def run_file(self, input_data=None):
        pass

    def getDesc(self):
        return {
            'name': self.name,
            'format': self.format
        }

class BaseActionPlugin(BasePlugin):
    inner_type = 'action'
    name = 'BasePlugin'
    allow_extensions = ['non']
    allow_type = 'entity'
    action = 'r'
    works = 'all'

    def canRun(self, input_entity):
        if self.allow_type != 'all' and self.allow_type != input_entity.self_name:
            return False
        
        if '*' in self.allow_extensions:
            return True

        if input_entity.self_name == 'entity' and input_entity.format in self.allow_extensions:
            return True
        
        return False
    
    def run(self, input_entity=None):
        pass

    def getDesc(self):
        return {
            'name': self.name,
            'action': self.action,
            'exts': str(self.allow_extensions)
        }

class BaseDisplayPlugin(BasePlugin):
    inner_type = 'display'
    name = 'Base'
    works = 'all'

    def getDesc(self):
        return {
            'name': self.name
        }

class BaseEditPlugin(BasePlugin):
    inner_type = 'edit'
    name = 'Base'
    works = 'all'

    def getDesc(self):
        return {
            'name': self.name
        }

class BaseThumbnailPlugin(BasePlugin):
    inner_type = 'thumbnail'
    name = 'Base'
    works = 'all'

    def getDesc(self):
        return {
            'name': self.name
        }

class BaseSearchPlugin(BasePlugin):
    inner_type = 'search'
    name = 'Base'

    def getDesc(self):
        return {
            'name': self.name
        }

class BaseService(BasePlugin):
    inner_type = 'service'
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
    
    def getDesc(self):
        return {
            'name': self.name,
            'interval': str(self.interval)
        }
