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

class AzureDiskImageNotFound(AzureError):
    pass

class AzureCommandNotLoaded(AzureError):
    pass

class AzureUnknownCommand(AzureError):
    pass

class AzureUnknownContainerCommand(AzureError):
    pass

class AzureUnknownDiskCommand(AzureError):
    pass

class AzureContainerListContentError(AzureError):
    pass

class AzureContainerListError(AzureError):
    pass

class AzureDiskUploadError(AzureError):
    pass

class AzureDiskDeleteError(AzureError):
    pass
