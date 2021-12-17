class ProgramVariablesNotSet(Exception):
    """Exception to raise when necessary variables are not set."""

    pass


class WrongResponseStructure(Exception):
    """Exception to raise when invalid response structure recieved."""

    pass


class ParseHomeworkerror(Exception):
    """Exception to raise when homework parsing errors appears."""

    pass


class APIRequestError(Exception):
    """Exception to raise when API requesting errors appears."""

    pass
