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
usage: azurectl compute data-disk -h | --help
       azurectl compute data-disk create --cloud-service-name=<name> --size=<disk-size-in-GB>
           [--instance-name=<name>]
           [--label=<label>]
           [--disk-name=<name>]
           [--lun=<lun>]
           [--no-cache|--read-only-cache|--read-write-cache]
       azurectl compute data-disk show --cloud-service-name=<name> --lun=<lun>
           [--instance-name=<name>]
       azurectl compute data-disk list --cloud-service-name=<name>
           [--instance-name=<name>]
       azurectl compute data-disk delete --cloud-service-name=<name> --lun=<lun>
           [--instance-name=<name>]
       azurectl compute data-disk help

commands:
    create
        add a new, empty data disk to the selected virtual machine
    show
        return data about an existing data disk
    delete
        detach a data disk from the selected virtual machine and destroy the
        data file
    list
        return data about all data disks attached to a virtual machine

options:
    --cloud-service-name=<name>
        name of the cloud service where the virtual machine may be found
    --size=<disk-size-in-GB>
        size of the disk, in GB, that will be provisioned. Must be an integer,
        and less than 1024
    --instance-name=<name>
        name of the virtual machine instance. If no name is given the
        instance name is assumed to be the same as the cloud service name
    --label=<label>
        custom label name for the disk
    --disk-name=<name>
        name of the disk file created in the current storage container. If
        omitted, a name will be automatically generated.
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
"""
# project
from ..account.service import AzureAccount
from base import CliTask
from ..utils.collector import DataCollector
from ..data_disk import DataDisk
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
        if self.command_args['show']:
            self.__show()
        if self.command_args['delete']:
            self.__delete()
        if self.command_args['list']:
            self.__list()

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
        self.result.add(
            'data-disk',
            self.data_disk.create(
                self.command_args['--cloud-service-name'],
                (
                    self.command_args['--instance-name'] or
                    self.command_args['--cloud-service-name']
                ),
                self.command_args['--size'],
                **optional_args
            )
        )
        self.out.display()

    def __show(self):
        args = [
            self.command_args['--cloud-service-name'],
            (
                self.command_args['--instance-name'] or
                self.command_args['--cloud-service-name']
            ),
            int(self.command_args['--lun'])
        ]
        self.result.add(
            'data-disk:%s:%s:%d' % tuple(args),
            self.data_disk.show(*args)
        )
        self.out.display()

    def __delete(self):
        args = [
            self.command_args['--cloud-service-name'],
            (
                self.command_args['--instance-name'] or
                self.command_args['--cloud-service-name']
            ),
            int(self.command_args['--lun'])
        ]
        self.result.add(
            'data-disk:%s:%s:%d' % tuple(args),
            self.data_disk.delete(*args)
        )
        self.out.display()

    def __list(self):
        args = [
            self.command_args['--cloud-service-name'],
            (
                self.command_args['--instance-name'] or
                self.command_args['--cloud-service-name']
            )
        ]
        self.result.add(
            'data-disks:%s:%s' % tuple(args),
            self.data_disk.list(*args)
        )
        self.out.display()
