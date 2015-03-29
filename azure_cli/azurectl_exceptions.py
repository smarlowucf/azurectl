# Copyright (c) 2015 SUSE Linux GmbH.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


class AzureError(Exception):
    """
        Base class to handle all known exceptions. Specific exceptions
        are sub classes of this base class
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class AzureConfigParseError(AzureError):
    pass


class AzureHelpNoCommandGiven(AzureError):
    pass


class AzureLoadCommandUndefined(AzureError):
    pass


class AzureLoadServiceNameUndefined(AzureError):
    pass


class AzureAccountLoadFailed(AzureError):
    pass


class AzureAccountNotFound(AzureError):
    pass


class AzureAccountValueNotFound(AzureError):
    pass


class AzureStorageFileNotFound(AzureError):
    pass


class AzureCommandNotLoaded(AzureError):
    pass


class AzureUnknownCommand(AzureError):
    pass


class AzureContainerListContentError(AzureError):
    pass


class AzureContainerListError(AzureError):
    pass


class AzureStorageUploadError(AzureError):
    pass


class AzureStorageDeleteError(AzureError):
    pass


class AzureOsImageListError(AzureError):
    pass


class AzureSubscriptionIdNotFound(AzureError):
    pass


class AzureManagementCertificateNotFound(AzureError):
    pass


class AzureInternalError(AzureError):
    pass


class AzurePageBlobAlignmentViolation(AzureError):
    pass


class AzureServiceManagementError(AzureError):
    pass


class AzureStorageListError(AzureError):
    pass


class AzureXZError(AzureError):
    pass
