from resources.Globals import datetime, os, consts, traceback

class Logger():
    def __init__(self, keep=False):
        self.keep = keep

    def __del__(self):
        try:
            self.file.close()
        except AttributeError:
            pass

    def __log_file_check(self):
        if getattr(self, "file", None) != None:
            return True
        
        now = datetime.now()

        # Keep=True: appends current time to file name.
        if self.keep:
            self.path = f"{consts['storage']}/logs/{now.strftime("%d-%m-%Y_%H-%M-%S")}.log"
        # Keep=False: creates log files per day.
        else:
            self.path = f"{consts['storage']}/logs/{now.strftime("%d-%m-%Y")}.log"
        
        # Checking if file exists. If no, creating.
        if not os.path.exists(self.path):
            __temp_logger_stream = open(self.path, 'w', encoding='utf-8')
            __temp_logger_stream.close()
        
        self.file = open(self.path, 'r+', encoding='utf-8')

        return True
    
    def log(self, section = "App", name = "success", message = "Undefined"):
        # Lets define "section"s: "App", "Config", "Extractor", "Act", "Service", "OS".
        # Name can be "success", "message" or "error".
        # In "message" you should describe what you want to write.
        self.__log_file_check()
        now = datetime.now()

        message = message.replace("\n", "\\n")
        message_to_write = f"{now.strftime("%Y-%m-%d %H:%M:%S")} [{section}] [{name}] {message}\n"
        self.file.seek(0, os.SEEK_END)
        self.file.write(message_to_write)

        if consts.get("context") == "cli":
            print(message_to_write)

    def logException(self, input_exception, section="App"):
        exp = str(input_exception) + traceback.format_exc()
        self.log(section, type(input_exception).__name__, exp)

logger = Logger()
