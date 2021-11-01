class BaseQueryException(Exception):
    """Base exception class for query logics"""

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return "%s(code=%s): %s" % (self.__class__.__name__, self.code, self.message)


class ProjectCompleteException(BaseQueryException):
    """Exception class for project complete"""

    def __init__(self, work):
        self.code = "ValueError"
        self.message = (
            "You can't complete this projectThis project has incomplete work: %s" % work
        )
