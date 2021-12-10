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

class Worker(Script):
    def install(self, env):
        deploying()
        self.configure(env)

    def stop(self, env):
        Execute(exportJavaHomeAndPath + ' && {0} stop'.format(launcherPath))

    def start(self, env):
        self.configure(self)
        Execute(exportJavaHomeAndPath + ' && {0} start'.format(launcherPath))

    def status(self, env):
        try:
            Execute(exportJavaHomeAndPath + ' && {0} status'.format(launcherPath))
        except ExecutionFailed as ef:
            if ef.code == 3:
                raise ComponentIsNotRunning("ComponentIsNotRunning")
            else:
                raise ef

    def configure(self, env):
        create_configure('false')

if __name__ == '__main__':
    Worker().execute()
