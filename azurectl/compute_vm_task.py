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
"""
usage: azurectl compute vm -h | --help
       azurectl compute vm create --cloud-service-name=<name> --region=<location> --image-name=<image>
           [--custom-data=<base64_string>]
           [--instance-name=<name>]
           [--instance-type=<type>]
           [--label=<label>]
           [--password=<password>]
           [--ssh-private-key-file=<file> | --fingerprint=<thumbprint>]
           [--ssh-port=<port>]
           [--user=<user>]
       azurectl compute vm delete --cloud-service-name=<name>
           [--instance-name=<name>]
       azurectl compute vm types
       azurectl compute vm help

commands:
    create
        create a virtual machine instance from an image
    delete
        delete a virtual machine instance. If no instance name is
        specified, the cloud service and all its associated instances
        will be deleted
    types
        list available virtual machine types
    --cloud-service-name=<name>
        name of the cloud service to put the virtual machine in.
        if the cloud service does not exist it will be created
    --region=<location>
        geographic region to run the virtual image
    --image-name=<image>
        name of the VHD disk image to create the virtual machine
        instance from
    --custom-data=<base64_string>
        base64 encoded data string. The information is available
        from the walinux agent in the running virtual machine
    --instance-name=<name>
        name of the virtual machine instance. if no name is
        given the instance name is the same as the cloud service
        name.
    --instance-type=<type>
        virtual machine type, by default set to: Small
    --label=<label>
        custom label name for the virtual machine instance
    --password=<password>
        password for the user to login. If no password is specified
        SSH password based login will be disabled
    --ssh-private-key-file=<file>
        path to ssh private key, from which a new PEM certificate
        will be created and added to the cloud service in order to
        allow ssh public key authentication
    --fingerprint=<thumbprint>
        thumbprint of an already existing certificate in the
        cloud service used for ssh public key authentication
    --ssh-port=<port>
        external SSH port
    --user=<user>
        user name for login, by default set to: azureuser
    help
        show manual page for image command
"""
import os

# project
from cli_task import CliTask
from azure_account import AzureAccount
from data_collector import DataCollector
from data_output import DataOutput
from logger import log
from azurectl_exceptions import *
from virtual_machine import VirtualMachine
from cloud_service import CloudService
from help import Help


class ComputeVmTask(CliTask):
    """
        Process vm commands
    """
    SSH_DEFAULT_PORT = 22

    def process(self):
        self.manual = Help()
        if self.__help():
            return

        self.result = DataCollector()
        self.out = DataOutput(
            self.result,
            self.global_args['--output-format'],
            self.global_args['--output-style']
        )

        self.account = AzureAccount(self.account_name, self.config_file)
        self.vm = VirtualMachine(self.account)
        self.cloud_service = CloudService(self.account)
        if self.command_args['create']:
            self.__create_cloud_service()
            self.__create_instance()
        elif self.command_args['delete']:
            if self.command_args['--instance-name']:
                self.__delete_instance()
            else:
                self.__delete_cloud_service()
        elif self.command_args['types']:
            self.__list_instance_types()

    def __help(self):
        if self.command_args['help']:
            self.manual.show('azurectl::compute::vm')
        else:
            return False
        return self.manual

    def __list_instance_types(self):
        self.result.add('instance-types', self.account.instance_types())
        self.out.display()

    def __create_instance(self):
        instance_type = self.command_args['--instance-type']
        if not instance_type:
            instance_type = 'Small'
        fingerprint = u''
        if self.command_args['--ssh-private-key-file']:
            fingerprint = self.cloud_service.add_certificate(
                self.command_args['--cloud-service-name'],
                self.command_args['--ssh-private-key-file']
            )
        elif self.command_args['--fingerprint']:
            fingerprint = self.command_args['--fingerprint']
        linux_configuration = self.__prepare_linux_configuration(fingerprint)
        network_configuration = self.__prepare_network()
        self.result.add(
            'instance',
            self.vm.create_instance(
                self.command_args['--cloud-service-name'],
                self.command_args['--region'],
                self.command_args['--image-name'],
                linux_configuration,
                network_configuration,
                self.command_args['--label'],
                'production',
                instance_type
            )
        )
        self.out.display()

    def __create_cloud_service(self):
        cloud_service_request_id = self.cloud_service.create(
            self.command_args['--cloud-service-name'],
            self.command_args['--region']
        )
        if cloud_service_request_id > 0:
            # a new cloud service was created for this instance, waiting
            # for the cloud service to become created. Basically we try
            # to prevent blocking, thus this is an exception to other
            # requests
            self.cloud_service.wait_for_request_completion(
                cloud_service_request_id
            )

    def __delete_cloud_service(self):
        cloud_service = self.command_args['--cloud-service-name']
        complete_deletion = True
        request_id = self.cloud_service.delete(
            cloud_service, complete_deletion
        )
        log.info(
            'Deletion of cloud service %s requested: %s' %
            (format(cloud_service), format(request_id))
        )

    def __delete_instance(self):
        instance_name = self.command_args['--instance-name']
        request_id = self.vm.delete_instance(
            self.command_args['--cloud-service-name'],
            instance_name
        )
        log.info(
            'Deletion of instance %s requested: %s' %
            (format(instance_name), format(request_id))
        )

    def __prepare_linux_configuration(self, fingerprint=u''):
        user = self.command_args['--user']
        instance_name = self.command_args['--instance-name']
        password = self.command_args['--password']
        custom_data = self.command_args['--custom-data']
        disable_ssh_password_authentication = False
        if not user:
            # no user specified, use the default Azure user name
            user = 'azureuser'
        if not instance_name:
            # no instance name specified, use the cloud service name
            instance_name = self.command_args['--cloud-service-name']
        if not password:
            # no password set, disable ssh user authentication
            disable_ssh_password_authentication = True
        return self.vm.create_linux_configuration(
            user,
            instance_name,
            disable_ssh_password_authentication,
            password,
            custom_data,
            fingerprint
        )

    def __prepare_network(self):
        ssh_endpoint = self.__prepare_ssh()
        return self.vm.create_network_configuration(
            [ssh_endpoint]
        )

    def __prepare_ssh(self, ssh_local_port=SSH_DEFAULT_PORT):
        ssh_public_port = self.command_args['--ssh-port']
        if not ssh_public_port:
            # no ssh public port specified, use local port as default
            ssh_public_port = ssh_local_port
        return self.vm.create_network_endpoint(
            'SSH', ssh_public_port, ssh_local_port, 'TCP'
        )