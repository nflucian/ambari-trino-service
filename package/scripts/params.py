#!/usr/bin/env python
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

from resource_management.libraries.script.script import Script

# config object that holds the configurations declared in the config xml file
config = Script.get_config()

node_properties = config['configurations']['node.properties']
jvm_config = config['configurations']['jvm.config']
config_properties = config['configurations']['config.properties']
access_control_properties = config['configurations']['access-control.properties']
rules_json = config['configurations']['rules.json']

connectors_to_add = config['configurations']['connectors.properties']['connectors.to.add']
connectors_to_delete = config['configurations']['connectors.properties']['connectors.to.delete']

memory_configs = ['query.max-memory-per-node', 'query.max-memory']
coordinator_hosts = 'trino_coordinator_hosts'
worker_hosts = 'trino_worker_hosts'

discoveryUri = 'http://{0}:{1}'.format(
    config['configurations']['config.properties']['coordinator.host'],
    config['configurations']['config.properties']['http-server.http.port'])

host_info = config['clusterHostInfo']
host_level_params = config['hostLevelParams']