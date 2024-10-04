import time
import threading
from core.settings import settings
from pathlib import Path
from db.db import Entity

class BasePlugin():
    inner_type = 'base'
    name = 'BasePlugin'

    def run(self, args=None):
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

    def run(self, args=None):
        pass

    def run_file(self, args=None):
        pass

    def getDesc(self):
        return {
            'name': self.name,
            'format': self.format
        }
    
    def moveFromTemp(self, entity):
        entity_path = entity.getDirPath()

        file_final_path = Path(Entity.getTempPath() + '\\' + entity.original_name)
        file_final_path_replace = str(entity_path) + '\\' + str((str(entity.id) + '.' + entity.format))
        file_final_path.rename(file_final_path_replace)

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

class BaseService(BasePlugin):
    inner_type = 'service'
    name = 'BaseService'
    interval = 60

    def __init__(self):
        self._stop_event = threading.Event()
        self.start_time = time.time()
        self.thread = None
    
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
    
    def setParam(self, setting, value):
        return settings.set(setting, value)
    
    def getParam(self, setting):
        return settings.get(setting)
    
    def getDesc(self):
        return {
            'name': self.name,
            'interval': str(self.interval)
        }
