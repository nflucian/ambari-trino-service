# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os.path as path
from resource_management.core.exceptions import ExecutionFailed, ComponentIsNotRunning
from resource_management.core.resources.system import Execute
from resource_management.libraries.script.script import Script

from common import create_configure, deploying, launcherPath, exportJavaHomeAndPath
from trino_client import smoketest_trino, TrinoClient

class Coordinator(Script):
    def install(self, env):
        deploying()
        self.configure(env)

    def stop(self, env):
        Execute(exportJavaHomeAndPath + ' && {0} stop'.format(launcherPath))

    def start(self, env):
        self.configure(self)
        Execute(exportJavaHomeAndPath + ' && {0} start'.format(launcherPath))
        from params import config_properties, host_info, worker_hosts, coordinator_hosts
        if worker_hosts in host_info.keys():
            all_hosts = host_info[worker_hosts] + \
                        host_info[coordinator_hosts]
        else:
            all_hosts = host_info[coordinator_hosts]
        smoketest_trino(TrinoClient(config_properties['coordinator.host'], 'root', config_properties['http-server.http.port']), all_hosts)

    def status(self, env):
        try:
            Execute(exportJavaHomeAndPath + ' && {0} status'.format(launcherPath))
        except ExecutionFailed as ef:
            if ef.code == 3:
                raise ComponentIsNotRunning("ComponentIsNotRunning")
            else:
                raise ef

    def configure(self, env):
        create_configure('true')

if __name__ == '__main__':
    Coordinator().execute()
