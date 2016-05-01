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
from azure.servicemanagement import ConfigurationSetInputEndpoint
from azure.servicemanagement import ConfigurationSet
from azure.servicemanagement import PublicKey
from azure.servicemanagement import LinuxConfigurationSet
from azure.servicemanagement import OSVirtualHardDisk
from azure.storage.blob.baseblobservice import BaseBlobService

# project
from ..azurectl_exceptions import (
    AzureVmCreateError,
    AzureVmDeleteError,
    AzureStorageNotReachableByCloudServiceError,
    AzureImageNotReachableByCloudServiceError
)


class VirtualMachine(object):
    """
        Implements creation/deletion and management of virtual
        machine instances from a given image name
    """
    def __init__(self, account):
        self.account = account
        self.container_name = account.storage_container()
        self.account_name = account.storage_name()
        self.account_key = account.storage_key()
        self.blob_service_host_base = self.account.get_blob_service_host_base()

        self.service = self.account.get_management_service()
        self.storage = BaseBlobService(
            self.account_name,
            self.account_key,
            endpoint_suffix=self.blob_service_host_base
        )

    def create_linux_configuration(
        self, username='azureuser', instance_name=None,
        disable_ssh_password_authentication=True,
        password=None, custom_data=None, fingerprint=u''
    ):
        """
            create a linux configuration
        """
        # The given instance name is used as the host name in linux
        linux_config = LinuxConfigurationSet(
            instance_name, username, password,
            disable_ssh_password_authentication,
            custom_data
        )
        if fingerprint:
            ssh_key_file = '/home/' + username + '/.ssh/authorized_keys'
            ssh_pub_key = PublicKey(
                fingerprint, ssh_key_file
            )
            linux_config.ssh.public_keys = [ssh_pub_key]
        return linux_config

    def create_network_configuration(self, network_endpoints):
        """
            create a network configuration
        """
        network_config = ConfigurationSet()
        for endpoint in network_endpoints:
            network_config.input_endpoints.input_endpoints.append(endpoint)
        network_config.configuration_set_type = 'NetworkConfiguration'
        return network_config

    def create_network_endpoint(
        self, name, public_port, local_port, protocol
    ):
        """
            create a network service endpoint
        """
        return ConfigurationSetInputEndpoint(
            name, protocol, public_port, local_port
        )

    def create_instance(
        self, cloud_service_name, disk_name, system_config,
        network_config=None, label=None, group='production',
        machine_size='Small', reserved_ip_name=None
    ):
        """
            create a virtual disk image instance
        """
        if not self.__storage_reachable_by_cloud_service(cloud_service_name):
            message = [
                'The cloud service "%s" and the storage account "%s"',
                'are not in the same region, cannot launch an instance.'
            ]
            raise AzureStorageNotReachableByCloudServiceError(
                ' '.join(message) % (
                    cloud_service_name, self.account_name
                )
            )

        if not self.__image_reachable_by_cloud_service(
            cloud_service_name, disk_name
        ):
            message = [
                'The selected image "%s" is not available',
                'in the region of the selected cloud service "%s",',
                'cannot launch instance'
            ]
            raise AzureImageNotReachableByCloudServiceError(
                ' '.join(message) % (
                    disk_name, cloud_service_name
                )
            )

        # check if the virtual machine deployment already exists. If so
        # any new instance must be created as additional role to the
        # deployment. Only the initial virtual machine instance must
        # be created as a new deployment for the selected cloud service
        try:
            self.service.get_deployment_by_name(
                service_name=cloud_service_name,
                deployment_name=cloud_service_name
            )
            deployment_exists = True
        except Exception:
            deployment_exists = False

        if reserved_ip_name:
            if not deployment_exists:
                try:
                    self.service.create_reserved_ip_address(reserved_ip_name)
                except Exception as e:
                    raise AzureVmCreateError(
                        '%s: %s' % (type(e).__name__, format(e))
                    )
            else:
                message = [
                    'A deployment of the name: %s already exists.',
                    'Assignment of a reserved IP address name can only',
                    'happen for the initial deployment.'
                ]
                raise AzureVmCreateError(
                    ' '.join(message) % cloud_service_name
                )

        if label and deployment_exists:
            message = [
                'A deployment of the name: %s already exists.',
                'Assignment of a label can only happen for the',
                'initial deployment.'
            ]
            raise AzureVmCreateError(
                ' '.join(message) % cloud_service_name
            )

        media_link = self.storage.make_blob_url(
            self.container_name, ''.join(
                [
                    cloud_service_name,
                    '_instance_', system_config.host_name,
                    '_image_', disk_name
                ]
            )
        )
        instance_disk = OSVirtualHardDisk(disk_name, media_link)
        instance_record = {
            'deployment_name': cloud_service_name,
            'deployment_slot': group,
            'network_config': network_config,
            'role_name': cloud_service_name,
            'role_size': machine_size,
            'service_name': cloud_service_name,
            'system_config': system_config,
            'os_virtual_hard_disk': instance_disk,
            'provision_guest_agent': True
        }
        if network_config:
            instance_record['network_config'] = network_config

        try:
            if deployment_exists:
                result = self.service.add_role(
                    **instance_record
                )
            else:
                if reserved_ip_name:
                    instance_record['reserved_ip_name'] = reserved_ip_name
                if label:
                    instance_record['label'] = label
                else:
                    instance_record['label'] = cloud_service_name
                result = self.service.create_virtual_machine_deployment(
                    **instance_record
                )
            return {
                'request_id': format(result.request_id),
                'cloud_service_name': cloud_service_name,
                'instance_name': system_config.host_name
            }
        except Exception as e:
            raise AzureVmCreateError(
                '%s: %s' % (type(e).__name__, format(e))
            )

    def delete_instance(
        self, cloud_service_name, instance_name
    ):
        """
            delete a virtual disk image instance
        """
        try:
            result = self.service.delete_deployment(
                cloud_service_name, instance_name
            )
            return(format(result.request_id))
        except Exception as e:
            raise AzureVmDeleteError(
                '%s: %s' % (type(e).__name__, format(e))
            )

    def __cloud_service_location(self, cloud_service_name):
        return self.service.get_hosted_service_properties(
            cloud_service_name
        ).hosted_service_properties.location

    def __storage_location(self):
        return self.service.get_storage_account_properties(
            self.account_name
        ).storage_service_properties.location

    def __image_locations(self, disk_name):
        image_properties = self.service.get_os_image(disk_name)
        return image_properties.location.split(';')

    def __storage_reachable_by_cloud_service(self, cloud_service_name):
        service_location = self.__cloud_service_location(
            cloud_service_name
        )
        storage_location = self.__storage_location()
        if service_location == storage_location:
            return True
        else:
            return False

    def __image_reachable_by_cloud_service(self, cloud_service_name, disk_name):
        service_location = self.__cloud_service_location(
            cloud_service_name
        )
        image_locations = self.__image_locations(disk_name)
        if service_location in image_locations:
            return True
        else:
            return False
