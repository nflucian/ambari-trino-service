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

import ConfigParser
import ast
import os
import os.path as path
import uuid
from resource_management.core.resources.system import Execute

scriptDir = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser.ConfigParser()
config.readfp(open(os.path.join(scriptDir, 'download.ini')))

trinoTarUrl = config.get('download', 'trino_tar_url')
trinoTarName = trinoTarUrl.split('/')[-1]
trinoCliUrl = config.get('download', 'trino_cli_url')
jdk11Url = config.get('download', 'jdk11_url')
jdk11TarName = jdk11Url.split('/')[-1]

packageDir = os.path.dirname(scriptDir)
serviceDir = os.path.dirname(packageDir)
serviceName = os.path.basename(serviceDir)

# stack = serviceDir.split('/')
# basePath = '/usr/{0}/{1}/trino/'.format(stack[-4].lower(), stack[-3])
basePath = '/opt/trino/'

trinoHome = basePath + serviceName
jdk11Home = basePath + 'jdk11/'
etcDir = trinoHome + '/etc'
catalogDir = etcDir + '/catalog'
launcherPath = trinoHome + '/bin/launcher'

exportJavaHomeAndPath = ' export JAVA_HOME=' + jdk11Home + ' && export PATH=${JAVA_HOME}/bin:$PATH '

def deploying():
    # download jdk11 and extract jdk11 tarball
    tmpJdk11Path = '/tmp/' + jdk11TarName
    Execute('mkdir -p {0}'.format(jdk11Home))
    Execute('wget --no-check-certificate {0} -O {1}'.format(jdk11Url, tmpJdk11Path))
    Execute('tar -xf {0} -C {1} --strip-components=1'.format(tmpJdk11Path, jdk11Home))

    # download and extract trino tarball
    Execute('mkdir -p {0}'.format(catalogDir))
    tmptrinoTarballPath = '/tmp/' + trinoTarName
    Execute('wget --no-check-certificate {0} -O {1}'.format(trinoTarUrl, tmptrinoTarballPath))
    Execute('tar -xf {0} -C {1} --strip-components=1'.format(tmptrinoTarballPath, trinoHome))


def create_connectors(connectors_to_add):
    if not connectors_to_add:
        return
    connectors_dict = ast.literal_eval(connectors_to_add)
    for connector in connectors_dict:
        connector_file = os.path.join(catalogDir, connector + '.properties')
        with open(connector_file, 'w') as f:
            for lineitem in connectors_dict[connector]:
                f.write('{0}\n'.format(lineitem))


def delete_connectors(connectors_to_delete):
    if not connectors_to_delete:
        return
    connectors_list = ast.literal_eval(connectors_to_delete)
    for connector in connectors_list:
        connector_file_name = os.path.join(catalogDir, connector + '.properties')
        Execute('rm -f {0}'.format(connector_file_name))

def create_configure(coordinator): 
    from params import node_properties, jvm_config, memory_configs, config_properties, \
            connectors_to_add, connectors_to_delete, discoveryUri

    key_val_template = '{0}={1}\n'

    with open(path.join(etcDir, 'node.properties'), 'w') as f:
        for key, value in node_properties.iteritems():
            f.write(key_val_template.format(key, value))
        f.write(key_val_template.format('node.id', str(uuid.uuid4())))

    with open(path.join(etcDir, 'jvm.config'), 'w') as f:
        f.write(jvm_config['content'])

    # with open(path.join(etcDir, 'access-control.properties'), 'w') as f:
    #     for key, value in access_control_properties.iteritems():
    #         f.write(key_val_template.format(key, value))

    # rulesJsonFilePath = access_control_properties['security.config-file']
    # with open(path.join(trinoHome, rulesJsonFilePath), 'w') as f:
    #     f.write(rules_json['content'])

    with open(path.join(etcDir, 'config.properties'), 'w') as f:
        for key, value in config_properties.iteritems():
            if key in memory_configs:
                value += 'GB'
            if key != 'coordinator.host':
                f.write(key_val_template.format(key, value))
        f.write(key_val_template.format('coordinator', coordinator))
        f.write(key_val_template.format('discovery.uri', discoveryUri))
        
    create_connectors(connectors_to_add)
    delete_connectors(connectors_to_delete)
    create_connectors("{'tpch': ['connector.name=tpch']}")
