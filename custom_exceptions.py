class ProgramVariablesNotSet(Exception):
    """Exception to raise when necessary variables are not set."""

    pass


class WrongResponseStructure(Exception):
    """Exception to raise when invalid response structure recieved."""

    pass


class APIRequestError(Exception):
    """Exception to raise when API requesting errors appears."""

    pass
