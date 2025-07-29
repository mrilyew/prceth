from colorama import init as ColoramaInit
from resources.Consts import consts
from pathlib import Path
from datetime import datetime
from utils.Hookable import Hookable
import os, traceback

class Logger(Hookable):
    '''
    Module for logging of messages and printing them to terminal
    '''

    events = ["log"]

    KIND_SUCCESS = 'success'
    KIND_ERROR = 'error'
    KIND_DEPRECATED = 'deprecated'
    KIND_MESSAGE = 'message'

    SECTION_SERVICES = 'Services'
    SECTION_DB = 'DB'
    SECTION_LINKAGE = 'Linkage'
    SECTION_EXECUTABLES = 'Executables'
    SECTION_SAVEABLE = 'Saveable'
    SECTION_EXTRACTORS = 'Extractors'
    SECTION_ACTS = 'Acts'
    SECTION_WEB = "Web"

    def __init__(self, config, storage, keep: bool = False):
        '''
        Params:

        keep: On True creates log file for app startup, on False create log file for current day.
        '''
        super().__init__()

        ColoramaInit()

        self.per_startup_mode = keep
        self.logs_storage = storage.sub('logs')
        self.config_link = config
        self.skip_categories = self.config_link.get("logger.skip_categories")
        self.is_out_to_file = self.config_link.get("logger.skip_file") == 0

        __path = self.logs_storage.dir
        if __path.is_dir() == False:
            __path.mkdir()

        self.add_hook("log", self.__console_hook)
        self.add_hook("log", self.__write_to_file_hook)

    def __console_hook(self, **kwargs):
        components = kwargs.get("components")

        section = components.get("section")
        message = components.get("message")
        kind = components["kind"]
        date = datetime.fromtimestamp(components.get("time"))

        write_message = f"{date.strftime("%Y-%m-%d %H:%M:%S")} [{section}] {message}\n"
        write_message = write_message.replace("\\n", "\n")
        write_colored_message = ""

        if kind == self.KIND_ERROR:
            write_colored_message = "\033[91m" + write_message + "\033[0m"
        elif kind == self.KIND_SUCCESS:
            write_colored_message = "\033[92m" + write_message + "\033[0m"
        elif kind == self.KIND_DEPRECATED:
            write_colored_message = "\033[93m" + write_message + "\033[0m"
        else:
            write_colored_message = write_message

        print(write_colored_message, end='')

    def __write_to_file_hook(self, **kwargs):
        components = kwargs.get("components")

        section = components.get("section")
        message = components.get("message")
        kind = components["kind"]
        date = datetime.fromtimestamp(components.get("time"))

        write_message = f"{date.strftime("%Y-%m-%d %H:%M:%S")} {section} {kind} >>> {message}\n"

        if self.is_out_to_file:
            self.log_stream.seek(0, os.SEEK_END)
            self.log_stream.write(write_message)

    def __del__(self):
        try:
            self.log_stream.close()
        except AttributeError:
            pass

    def __log_file_check(self):
        if self.is_out_to_file == False:
            return True

        if getattr(self, "file", None) != None:
            return True

        now = datetime.now()
        log_path = ""

        # appends current time to file name
        if self.per_startup_mode:
            log_path = f"{self.logs_storage.dir}/{now.strftime('%Y-%m-%d_%H-%M-%S')}.log"
        # creates log files per day
        else:
            log_path = f"{self.logs_storage.dir}/{now.strftime('%Y-%m-%d')}.log"

        self.path = Path(log_path)

        # Checking if file exists, If no creating it
        if self.path.exists() == False:
            __temp_logger_stream = open(self.path, 'w', encoding='utf-8')
            __temp_logger_stream.close()

        self.log_stream = open(str(self.path), 'r+', encoding='utf-8')

        return True

    def log(self, message: str = "Undefined", section: str = "App", kind: str = "message", silent: bool = False):
        '''
        Logs message.

        Params:

        message: Message that will printed to console and log file

        section: Section from place that message was printed

        kind: Type of message ("success", "message", "deprecated" or "error")

        silent: If True, message will not be displayed at the console
        '''

        for compare_section in self.skip_categories:
            if compare_section == section:
                return

            if compare_section.endswith('*') and section.find(compare_section.replace('*', '')) != -1:
                return

        self.__log_file_check()

        self.trigger_hooks("log", components={
            "time": (datetime.now()).timestamp(),
            "section": section,
            "message": message,
            "kind": kind,
            "silent": silent
        })

    def logException(self, input_exception, section: str = "App", silent: bool = False):
        __exp = traceback.format_exc()

        self.log(section=section, message=type(input_exception).__name__ + " " + __exp, kind=self.KIND_ERROR, silent=silent)
