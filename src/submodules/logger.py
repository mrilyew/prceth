from resources.globals import datetime, os

class Logger():
    def __init__(self, keep=False):
        now = datetime.now()
        
        if keep:
            self.path = os.getcwd() + '/storage/logs/' + now.strftime("%d-%m-%Y_%H-%M-%S") + '.log'
        else:
            self.path = os.getcwd() + '/storage/logs/' + now.strftime("%d-%m-%Y") + '.log'
        
        if not os.path.exists(self.path):
            temp_stream = open(self.path, 'w', encoding='utf-8')
            temp_stream.close()

        self.file = open(self.path, 'r+', encoding='utf-8')

    def __del__(self):
        try:
            self.file.close()
        except AttributeError:
            pass
    
    def log(self, section, name, message):
        now = datetime.now()
        self.file.seek(0, os.SEEK_END)
        self.file.write(f"{now.strftime("%Y-%m-%d %H:%M:%S")} [{section}] [{name}] {message}\n")

    def logException(self, exc):
        self.log("App", type(exc).__name__, str(exc))

logger = Logger()
