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
module: f5bigip_sys_ntp
short_description: BIG-IP sys ntp module
description:
    - Configures the Network Time Protocol (NTP) daemon for the BIG-IP.
system.
version_added: 2.3
author:
    - "Eric Jacob, @erjac77"
notes:
    - Requires BIG-IP software version >= 11.6
requirements:
    - f5-sdk
options:
    description:
        description:
            - Specifies descriptive text that identifies the component.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 2.3
    servers:
        description:
            - Configures NTP servers for the BIG-IP system.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 2.3
    timezone:
        description:
            - Specifies the time zone that you want to use for the system time.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 2.3
'''

EXAMPLES = '''
- name: Add SYS NTP Servers
  f5bigip_sys_ntp:
    f5_hostname: 172.16.227.35
    f5_username: admin
    f5_password: admin
    f5_port: 443
    servers:
      - 10.20.20.21
      - 10.20.20.22
    timezone: America/Montreal
    state: present
  delegate_to: localhost
'''

from ansible_common_f5.f5_bigip import *

BIGIP_SYS_NTP_ARGS = dict(
    description =   dict(type='str'),
    #restrict    =   dict(type='list'),
    servers     =   dict(type='list'),
    timezone    =   dict(type='str')
)

class F5BigIpSysNtp(F5BigIpUnnamedObject):
    def set_crud_methods(self):
        self.methods = {
            'read':     self.mgmt_root.tm.sys.ntp.load,
            'update':   self.mgmt_root.tm.sys.ntp.update
        }
    
    def _absent(self):
        if not self.params['servers']:
            raise AnsibleF5Error("Absent can only be used when removing NTP servers")
        
        return super(F5BigIpSysNtp, self)._absent()

def main():
    # Translation list for conflictual params
    tr = {}
    
    module = AnsibleModuleF5BigIpUnnamedObject(argument_spec=BIGIP_SYS_NTP_ARGS, supports_check_mode=False)
    
    try:
        obj = F5BigIpSysNtp(check_mode=module.supports_check_mode, tr=tr, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()