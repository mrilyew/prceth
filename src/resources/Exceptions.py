class WebServiceApiException(Exception):
    def __init__(self, message):
        super().__init__(message)

class NotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidPassedParam(Exception):
    def __init__(self, message):
        super().__init__(message)

class NotPassedException(Exception):
    def __init__(self, message):
        super().__init__(message)

class NotInstalledException(Exception):
    def __init__(self, message):
        super().__init__(message)

class AccessDeniedException(Exception):
    def __init__(self, message):
        super().__init__(message)

class LibNotInstalledException(Exception):
    def __init__(self, message):
        super().__init__(message)

class ExecutableArgumentsException(Exception):
    def __init__(self, message):
        super().__init__(message)

class AbstractClassException(Exception):
    def __init__(self, message):
        super().__init__(message)
