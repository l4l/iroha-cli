# Copyright Soramitsu Co., Ltd. 2017 All Rights Reserved.
# http://soramitsu.co.jp
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from cmd import Cmd
from info import Info
import re
from crypto import create_keypair, dump, undump
from ed25519 import SigningKey, VerifyingKey


def check_input(arg, regexp, err):
    if re.match(regexp, arg, re.I) is not None:
        return arg
    else:
        print(err)
        return None


class Shell(Cmd):
    motd = '''
                   _            _              _         _  _ 
                  <_> _ _  ___ | |_  ___   ___| |_  ___ | || |
                  | || '_>/ ' \|   |<_> | <_-<|   |/ ._>| || |
                  |_||_|  \___/|_|_|<___| /__/|_|_|\___.|_||_|
                                                              
                                                              
           '''
    prompt = ">> "
    info = Info()

    def do_set_pub(self, arg):
        args = arg.split()
        if len(args) < 1:
            print("No pubkey was provided")
            return

        r = r'[a-z0-9]{64}'
        i = check_input(args[0].lower(), r,
                        "Key format is wrong! Should match " + r)
        if i is None:
            return

        self.info.pubkey = VerifyingKey(undump(i))

    def do_set_pri(self, arg):
        args = arg.split()
        if len(args) < 1:
            print("No prikey was provided")
            return

        r = r'([a-z0-9]{128})|([a-z0-9]{64})'
        i = check_input(args[0].lower(), r,
                        "Key format is wrong! Should match " + r)
        if i is None:
            return

        self.info.prikey = SigningKey(undump(i))

    def do_gen_pair(self, arg):
        i = self.info
        (i.prikey, i.pubkey) = create_keypair()
        print("Your keypair is: sk=[{}], pk=[{}]".format(dump(i.prikey), dump(i.pubkey)))

    def do_pub(self, arg):
        if self.info.pubkey is None:
            print("Pubkey not set yet")
        else:
            print("Current pubkey: {}".format(dump(self.info.pubkey)))

    def do_pri(self, arg):
        if self.info.prikey is None:
            print("Prikey not set yet")
        else:
            print("Current prikey: {}".format(dump(self.info.prikey)))

    def do_exit(self, arg):
        __import__('sys').exit(0)

    def Shell(self):
        pass
