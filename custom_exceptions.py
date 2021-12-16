class ProgramVariablesNotSet(Exception):
    """Exception to raise when necessary variables are not set."""

    pass


class WrongResponseStatusCode(ConnectionError):
    """Exception to raise when wrong response status code recieved."""

    pass


class WrongResponseStructure(Exception):
    """Exception to raise when invalid response structure recieved."""

    pass
