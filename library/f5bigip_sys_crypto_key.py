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
module: f5bigip_sys_crypto_key
short_description: BIG-IP sys crypto key module
description:
    - Manage cryptographic keys and related objects on the BIG-IP system.
version_added: 2.3
author:
    - "Eric Jacob, @erjac77"
notes:
    - Requires BIG-IP software version >= 11.6
requirements:
    - f5-sdk
options:
    challenge_password:
        description:
            - Specifies the challenge password to create the certificate request key.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 2.3
    command:
        description:
            - Specifies the command to execute.
        required: false
        default: null
        choices: ['install']
        aliases: []
        version_added: 2.3
    consumer:
        description:
            - Specifies the system component by which a key and/or associated cryptographic file will be consumed.
        required: false
        default: ltm
        choices: ['enterprise-manager', 'iquery', 'iquery-big3d', 'ltm', 'webserver']
        aliases: []
        version_added: 2.3
    curve_name:
        description:
            - Specifies the curve name to be used in creation of elliptc curve (EC) key.
        required: false
        default: prime256v1
        choices: ['prime256v1', 'secp384r1']
        aliases: []
        version_added: 2.3
    from_editor:
        description:
            - Specifies that the key should be obtained from a text editor session.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 2.3
    from_local_file:
        description:
            - Specifies a local file path from which a key is to be copied.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 2.3
    from_url:
        description:
            - Specifies a URI which is to be used to obtain a key for import into the configuration of the system.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 2.3
    key_size:
        description:
            - Specifies the size, in bits, of the key to be generated.
        required: false
        default: null
        choices: ['512', '1024', '2048', '4096']
        aliases: []
        version_added: 2.3
    key_type:
        description:
            - Specifies the size, in bits, of the key to be generated.
        required: false
        default: null
        choices: ['dsa-private', 'ec-private', 'rsa-private']
        aliases: []
        version_added: 2.3
    lifetime:
        description:
            - Specifies the certificate life time to be used in creation of the certificate associated with the given key.
        required: false
        default: 365
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
    no_overwrite:
        description:
            - Specifies option of not overwriting a key if it is in the scope.
        required: false
        default: true
        choices: [true, false]
        aliases: []
        version_added: 2.3
    partition:
        description:
            - Displays the administrative partition in which the component object resides.
        required: false
        default: Common
        choices: []
        aliases: []
        version_added: 2.3
    passphrase:
        description:
            - Specifies an optional passphrase with which the key has been protected.
        required: false
        default: null
        choices: []
        aliases: []
        version_added: 2.3
    security_type:
        description:
            - Specifies the level of security used in storing the key in question.
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
'''

EXAMPLES = '''
- name: Install SYS Crypto Key from local file
  f5bigip_sys_crypto_key:
    f5_hostname: 172.16.227.35
    f5_username: admin
    f5_password: admin
    f5_port: 443
    name: example.localhost.key
    from_local_file: /tmp/example.localhost.key
    state: present
  delegate_to: localhost

- name: Create SYS Crypto Key
  f5bigip_sys_crypto_key:
    f5_hostname: 172.16.227.35
    f5_username: admin
    f5_password: admin
    f5_port: 443
    name: example.localhost.key
    state: present
  delegate_to: localhost
'''

from ansible_common_f5.f5_bigip import *

BIGIP_SYS_CRYPTO_KEY_ARGS = dict(
    consumer                    =   dict(type='str', choices=['enterprise-manager', 'iquery', 'iquery-big3d', 'ltm', 'webserver']),
    # create
    challenge_password          =   dict(type='str'),
    curve_name                  =   dict(type='str', choices=['prime256v1', 'secp384r1']),
    key_size                    =   dict(type='str', choices=['512', '1024', '2048', '4096']),
    key_type                    =   dict(type='str', choices=['dsa-private', 'ec-private', 'rsa-private']),
    lifetime                    =   dict(type='int'),
    passphrase                  =   dict(type='str'),
    security_type               =   dict(type='str', choices=['fips', 'normal', 'password', 'nethsm']),
    # install
    command                     =   dict(type='str', choices=['install']),
    from_editor                 =   dict(type='str'),
    from_local_file             =   dict(type='str'),
    from_url                    =   dict(type='str'),
    no_overwrite                =   dict(type='bool')
)

class F5BigIpSysCryptoKey(F5BigIpNamedObject):
    def set_crud_methods(self):
        self.methods = {
            'create':   self.mgmt_root.tm.sys.crypto.keys.key.create,
            'read':     self.mgmt_root.tm.sys.crypto.keys.key.load,
            'update':   self.mgmt_root.tm.sys.crypto.keys.key.update,
            'delete':   self.mgmt_root.tm.sys.crypto.keys.key.delete,
            'exists':   self.mgmt_root.tm.sys.crypto.keys.key.exists,
            'exec_cmd': self.mgmt_root.tm.sys.crypto.keys.exec_cmd
        }

    def _exists(self):
        keys = self.mgmt_root.tm.sys.crypto.keys.get_collection()
        for key in keys:
            name = self.params['name']
            if key.name == name:
                return True

        return False

    def _install(self):
        """Upload the key on the BIG-IP system."""
        name = self.params['name']

        if self.params['fromEditor']:
            param_set = { 'from-editor': self.params['fromEditor'] }
        if self.params['fromLocalFile']:
            param_set = { 'from-local-file': self.params['fromLocalFile'] }
        if self.params['fromUrl']:
            param_set = { 'from-url': self.params['fromUrl'] }

        if param_set:
            param_set.update({ 'name': name })
            if self.params['consumer']:
                param_set.update({ 'consumer': self.params['consumer'] })
            if self.params['noOverwrite']:
                param_set.update({ 'no-overwrite': self.params['noOverwrite'] })

            # Install the key
            self.methods['exec_cmd']('install', **param_set)
        else:
            raise AnsibleF5Error("Missing required parameter 'from-*' to install the key.")

        # Make sure it is installed
        if not self._exists():
            raise AnsibleF5Error("Failed to create the object.")
        
        return True

    def _present(self):
        has_changed = False
        
        if self.params['command'] == 'install':
            if not self._exists() or (self.params['noOverwrite'] is not None and self.params['noOverwrite'] is False):
                has_changed = self._install()
        else:
            if not self._exists():
                has_changed = self._create()
        
        return has_changed

def main():
    # Translation list for conflictual params
    tr = {}
    
    module = AnsibleModuleF5BigIpNamedObject(
        argument_spec=BIGIP_SYS_CRYPTO_KEY_ARGS,
        supports_check_mode=False,
        mutually_exclusive=[
            ['from_editor', 'from_local_file', 'from_url']
        ]
    )
    
    try:
        obj = F5BigIpSysCryptoKey(check_mode=module.supports_check_mode, tr=tr, **module.params)
        result = obj.flush()
        module.exit_json(**result)
    except Exception as exc:
        module.fail_json(msg=str(exc))

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()