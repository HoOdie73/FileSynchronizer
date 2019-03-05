class MissingDataException(Exception, BaseException):
    "file doesn't contain the proper keys to parse the json"
    pass
