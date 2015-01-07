class AzureError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class AzureLoadCommandError(AzureError):
    pass

class AzureLoadCommandUndefined(AzureError):
    pass

class AzureNoCommandGiven(AzureError):
    pass

class AzureAccountLoadFailed(AzureError):
    pass

class AzureAccountNotFound(AzureError):
    pass

class AzureAccountValueNotFound(AzureError):
    pass

class AzureCommandNotLoaded(AzureError):
    pass

class AzureUnknownCommand(AzureError):
    pass

class AzureUnknownContainerCommand(AzureError):
    pass
