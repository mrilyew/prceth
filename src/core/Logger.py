from resources.Globals import datetime, os, consts, traceback, Path, config
from colorama import Fore, init as ColoramaInit

class Logger():
    '''
    Module for logging of messages and printing them to console.
    '''
    def __init__(self, keep: bool=False):
        '''
        Params:

        keep: On True creates log file for app startup, on False create log file for current day.
        '''
        ColoramaInit()

        self.keep = keep
        self.dir = Path(f"{consts.get('storage')}/logs")
        if self.dir.is_dir() == False:
            self.dir.mkdir()

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
            self.path = f"{consts.get('storage')}/logs/{now.strftime('%Y-%m-%d_%H-%M-%S')}.log"
        # Keep=False: creates log files per day.
        else:
            self.path = f"{consts.get('storage')}/logs/{now.strftime('%Y-%m-%d')}.log"
        
        # Checking if file exists. If no, creating.
        if not os.path.exists(self.path):
            __temp_logger_stream = open(self.path, 'w', encoding='utf-8')
            __temp_logger_stream.close()
        
        self.file = open(self.path, 'r+', encoding='utf-8')

        return True
    
    def log(self, message: str = "Undefined", section: str = "App", name: str = "message", silent: bool = False):
        '''
        Logs message.

        Params:

        message: Message that will printed to console and log file

        section: Section from place that message was printed

        name: Type of message ("success", "message", "deprecated" or "error")

        silent: If True, no message will be displayed in the console
        '''

        if section in config.get("logger.skip_categories"):
            return

        self.__log_file_check()
        now = datetime.now()

        is_console = consts.get("context") == "cli" and silent == False
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        message = message.replace("\n", "\\n")
        message_to_write = f"{current_time} [{section}] {message}\n"

        if is_console == False:
            message_to_write = f"{current_time} [{name}] [{section}] {message}\n"

        self.file.seek(0, os.SEEK_END)
        #self.file.write(message_to_write.replace("\n", "\\n"))
        self.file.write(message_to_write)

        if is_console == True:
            if name == "error":
                print("\033[91m" + message_to_write.replace("\n", "") + "\033[0m")
            elif name == "success":
                print("\033[92m" + message_to_write.replace("\n", "") + "\033[0m")
            elif name == "deprecated":
                print("\033[93m" + message_to_write.replace("\n", "") + "\033[0m")
            else:
                print(message_to_write.replace("\n", ""))

    def logException(self, input_exception, section: str ="App", silent: bool =True):
        exp = str(input_exception) + traceback.format_exc()
        self.log(section=section, message=type(input_exception).__name__ + " " + exp, name="error", silent=silent)

logger = Logger()
