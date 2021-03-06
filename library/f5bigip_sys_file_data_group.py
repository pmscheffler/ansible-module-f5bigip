#!/usr/bin/python
#
# Copyright 2016, Eric Jacob <erjac77@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

DOCUMENTATION = '''
---
module: f5bigip_sys_file_data_group
short_description: BIG-IP sys file data-group module
description:
    - Configures an external class.
version_added: 2.3
author:
    - "Eric Jacob, @erjac77"
notes:
    - Requires BIG-IP software version >= 11.6
requirements:
    - f5-sdk
options:
    app_service:
        description:
            - Specifies the application service that the object belongs to.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 2.3
    data_group_description:
        description:
            - Specifies descriptive text that identifies the component.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 2.3
    data_group_name:
        description:
            - Specifies the name of the external data group that will be created within the ltm data-group module and reference the given data group file.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 2.3
    name:
        description:
            - Specifies unique name for the component.
        required: true
        default: null
        choices: []
        aliases: []
        version_added: 2.3
    partition:
        description:
            - Specifies the administrative partition in which the component object resides.
        required: false
        default: Common
        choices: []
        aliases: []
        version_added: 2.3
    separator:
        description:
            - Specifies a separator to use when defining the data group.
        required: false
        default: :=
        choices: []
        aliases: []
        version_added: 2.3
    source_path:
        description:
            - This optional attribute takes a URL.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 2.3
    state:
        description:
            - Specifies the state of the component on the BIG-IP system.
        required: false
        default: present
        choices: ['absent', 'present']
        aliases: []
        version_added: 2.3
    type:
        description:
            - Specifies the kind of data in the group.
        required: false
        default: present
        choices: ['integer', 'ip', 'string']
        aliases: []
        version_added: 2.3
'''

EXAMPLES = '''
- name: Create LTM External Data-Group file
  f5bigip_sys_file_data_group:
    f5_hostname: 172.16.227.35
    f5_username: admin
    f5_password: admin
    f5_port: 443
    name: my_ext_dg_file
    partition: Common
    source_path: file:/var/config/rest/downloads/my_ext_dg.dat
    type: string
    state: present
  delegate_to: localhost
'''

from ansible_common_f5.f5_bigip import *

BIGIP_SYS_FILE_DATA_GROUP_ARGS = dict(
    app_service             =   dict(type='str'),
    data_group_description  =   dict(type='str'),
    data_group_name	        =   dict(type='str'),
    separator               =   dict(type='str'),
    source_path             =   dict(type='str'),
    type                    =   dict(type='str', choices=['integer', 'ip', 'string'])
)

class F5BigIpSysFileDataGroup(F5BigIpNamedObject):
    def set_crud_methods(self):
        self.methods = {
            'create':   self.mgmt_root.tm.sys.file.data_groups.data_group.create,
            'read':     self.mgmt_root.tm.sys.file.data_groups.data_group.load,
            'update':   self.mgmt_root.tm.sys.file.data_groups.data_group.update,
            'delete':   self.mgmt_root.tm.sys.file.data_groups.data_group.delete,
            'exists':   self.mgmt_root.tm.sys.file.data_groups.data_group.exists
        }

def main():
    # Translation list for conflictual params
    tr = {}
    
    module = AnsibleModuleF5BigIpNamedObject(argument_spec=BIGIP_SYS_FILE_DATA_GROUP_ARGS, supports_check_mode=False)
    
    try:
        obj = F5BigIpSysFileDataGroup(check_mode=module.supports_check_mode, tr=tr, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()