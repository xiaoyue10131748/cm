#! /usr/bin/env python
########################################################################
#
#    Copyright 2018 cloudmesh.org
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#    License: Apache 2.0
#
########################################################################
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import oyaml as yaml
import os
from cloudmesh.management.configuration.config import Config
from cloudmesh.shell.variables import Variables

class Driver(object):

    def __init__(self, name="~/.cloudmesh/cloudmesh4.yaml"):
        name = os.path.expanduser(name)
        self.config = Config(name=name)

    def get(self, name=None):
        connection = None

        if name is None:
            variables = Variables()
            cloudname = variables['cloud']

        kind = self.config.get(
            "cloudmesh.cloud.{name}.cm.kind".format(name=name))
        credentials = self.config.get(
            "cloudmesh.cloud.{name}.credentials".format(name=name))

        # BUG FROM HERE ON WRONG

        if kind == 'azure':
            AZURE_SUBSCRIPTION_ID = credentials['AZURE_SUBSCRIPTION_ID']
            AZURE_MANAGEMENT_CERT_PATH = credentials[
                'AZURE_MANAGEMENT_CERT_PATH']
            AZDriver = get_driver(Provider.AZURE)
            connection = AZDriver(subscription_id=AZURE_SUBSCRIPTION_ID,
                                  key_file=AZURE_MANAGEMENT_CERT_PATH)
        elif kind == 'aws':
            EC2_ACCESS_ID = credentials['EC2_ACCESS_ID']
            EC2_SECRET_KEY = credentials['EC2_SECRET_KEY']
            EC2Driver = get_driver(Provider.EC2)
            connection = EC2Driver(EC2_ACCESS_ID, EC2_SECRET_KEY)

        return connection


if __name__ == '__main__':
    cm = Driver()
    driver = cm.get("aws")
    print("driver=", driver)
    # connection = cm.get_driver("azure")
    # retrieve available images and sizes
    # images = connection.list_images()
