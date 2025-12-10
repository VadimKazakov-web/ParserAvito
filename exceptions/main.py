
class NamedParametersError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return "NamedParametersError, {}".format(self.message)
        else:
            return "NamedParametersError, check the named parameters"


class BadInternetConnection(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return "BadInternetConnection, {}".format(self.message)
        else:
            return "BadInternetConnection, check internet or try again later"


class PushStopButton(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return "The \"Stop\" button is pressed, {}".format(self.message)
        else:
            return "The \"Stop\" button is pressed"

