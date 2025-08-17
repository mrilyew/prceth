class WebServiceApiException(Exception):
    pass

class NotFoundException(Exception):
    pass

class InvalidPassedParam(Exception):
    pass

class NotPassedException(Exception):
    pass

class NotInstalledException(Exception):
    pass

class AccessDeniedException(Exception):
    pass

class LibNotInstalledException(Exception):
    pass

class DeclaredArgumentsException(Exception):
    pass

class AbstractClassException(Exception):
    pass

class SuitableExtractMethodNotFound(Exception):
    pass

class FatalError(Exception):
    pass

class EndOfCycleException(Exception):
    pass

class InvalidArgumentName(Exception):
    pass

class AlreadyLinkedException(Exception):
    pass
