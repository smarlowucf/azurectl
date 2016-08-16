# Copyright (c) 2016 SUSE.  All rights reserved.
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
Data-disks are virtual disks attached to a virtual machine, backed by a virtual
hard disk (VHD) image in Azure storage.

usage: azurectl compute data-disk -h | --help
       azurectl compute data-disk create --cloud-service-name=<name> --size=<disk-size-in-GB>
           [--instance-name=<name>]
           [--label=<label>]
           [--disk-name=<name>]
           [--lun=<lun>]
           [--no-cache|--read-only-cache|--read-write-cache]
           [--wait]
       azurectl compute data-disk delete --disk-name=<name>
       azurectl compute data-disk detach --cloud-service-name=<name> --lun=<lun>
           [--instance-name=<name>]
           [--wait]
       azurectl compute data-disk list
       azurectl compute data-disk show --disk-name=<name>
       azurectl compute data-disk show attached --cloud-service-name=<name>
           [--lun=<lun>]
           [--instance-name=<name>]
       azurectl compute data-disk help

commands:
    create
        create a new, empty data disk attached to the specified instance.
        The data disk vhd file will be created using the following naming
        schema: <instance-name|cloud-service-name>-data-disk-<utctime>
    delete
        delete the specified data disk. The call will fail if the disk
        is still attached to an instance
    detach
        detach a data disk from the selected virtual machine and retain the
        data disk vhd file
    list
        return list of all disks from your image repository
    show
        return details of the specified disk
    show attached
        return details about the data disk(s) attached to the selected
        virtual machine. If a lun is specified only details about the
        disk connected to that lun will be shown

options:
    --cloud-service-name=<name>
        name of the cloud service where the virtual machine may be found
    --disk-name=<name>
        name of the data disk as registered in the image repository
    --instance-name=<name>
        name of the virtual machine instance. If no name is given the
        instance name is assumed to be the same as the cloud service name
    --label=<label>
        custom label name for the disk
    --lun=<lun>
        logical unit number where the disk is mounted. Must be an integer
        between 0 and 15. If omitted during create, the first available LUN
        will be selected automatically
    --no-cache
        disable caching on the data disk
    --read-only-cache
        enable cached reads from the data disk. If a cache method is not
        selected, read-only will be selected by default
    --read-write-cache
        enable cached reads from and writes to the data disk
    --size=<disk-size-in-GB>
        size of the disk, in GB, that will be provisioned. Must be an integer,
        and less than 1024
    --wait
        wait for the request to succeed
"""
# project
from ..logger import log
from ..account.service import AzureAccount
from base import CliTask
from ..utils.collector import DataCollector
from ..instance.data_disk import DataDisk
from ..utils.output import DataOutput
from ..defaults import Defaults
from ..help import Help


class ComputeDataDiskTask(CliTask):
    """
        Process image commands
    """
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

        self.load_config()

        self.account = AzureAccount(self.config)
        self.data_disk = DataDisk(self.account)

        if self.command_args['create']:
            self.__create()
        if self.command_args['delete']:
            self.__delete()
        if self.command_args['detach']:
            self.__detach()
        if self.command_args['attached']:
            if self.command_args['show']:
                self.__show_attached()
        else:
            if self.command_args['list']:
                self.__list()
            if self.command_args['show']:
                self.__show()

    def __help(self):
        if self.command_args['help']:
            self.manual.show('azurectl::compute::data_disk')
        else:
            return False
        return self.manual

    def __create(self):
        optional_args = {}
        if self.command_args['--label']:
            optional_args['label'] = self.command_args['--label']
        if self.command_args['--disk-name']:
            optional_args['filename'] = self.command_args['--disk-name']
        if self.command_args['--lun']:
            optional_args['lun'] = int(self.command_args['--lun'])
        if (
            self.command_args['--no-cache'] or
            self.command_args['--read-only-cache'] or
            self.command_args['--read-write-cache']
        ):
            optional_args['host_caching'] = Defaults.host_caching_for_docopts(
                self.command_args
            )
        request_id = self.data_disk.create(
            self.command_args['--size'],
            self.command_args['--cloud-service-name'],
            self.command_args['--instance-name'],
            **optional_args
        )
        if self.command_args['--wait']:
            self.request_wait(request_id)
        self.result.add(
            'data-disk', request_id
        )
        self.out.display()

    def __show(self):
        self.result.add(
            'data-disk', self.data_disk.show(self.command_args['--disk-name'])
        )
        self.out.display()

    def __show_attached(self):
        request_params = [
            self.command_args['--cloud-service-name'],
            (
                self.command_args['--instance-name'] or
                self.command_args['--cloud-service-name']
            ),
            self.command_args['--lun'] or 'on_all_luns'
        ]
        self.result.add(
            'data-disk:%s:%s:%s' % tuple(request_params),
            self.data_disk.show_attached(
                self.command_args['--cloud-service-name'],
                self.command_args['--instance-name'],
                self.command_args['--lun']
            )
        )
        self.out.display()

    def __delete(self):
        self.data_disk.delete(
            self.command_args['--disk-name']
        )
        log.info('Deleted data disk %s', self.command_args['--disk-name'])

    def __detach(self):
        request_params = [
            self.command_args['--cloud-service-name'],
            (
                self.command_args['--instance-name'] or
                self.command_args['--cloud-service-name']
            ),
            int(self.command_args['--lun'])
        ]
        request_id = self.result.add(
            'data-disk detach:%s:%s:%d' % tuple(request_params),
            self.data_disk.detach(
                int(self.command_args['--lun']),
                self.command_args['--cloud-service-name'],
                self.command_args['--instance-name']
            )
        )
        if self.command_args['--wait']:
            self.request_wait(request_id)
        self.out.display()

    def __list(self):
        self.result.add(
            'data-disks', self.data_disk.list()
        )
        self.out.display()
