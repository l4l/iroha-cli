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

import info
import crypto
from commands_pb2 import CreateAccount, CreateAsset, Command
from primitive_pb2 import Signature
from block_pb2 import Transaction
from typing import List, Tuple
from random import randint


# def create_asset(info: info.Info, name: str):
#     return CreateAsset(asset_name=name, domain_id=info.domain_id)
#
# def create_account(info: info.Info, name: str):
#     return CreateAccount(account_name=name, domain_id=info.domain_id, main_pubkey=info.pubkey)

def create_transaction(info: info.Info, comms: List[(str, str)]):
    tx = Transaction()

    commands = []
    for c in comms:
        cmd = Command()
        name = c[1]
        if c[0] == 'create_account':
            cmd.create_account.account_name = name
            cmd.create_account.domain_id = info.domain_id
            commands.append(cmd)
        elif c[0] == 'create_asset':
            cmd.create_asset.asset_name = name
            cmd.create_asset.domain_id = info.domain_id
        elif c[0] == 'transfer_asset':
            cmd.transfer_asset.src_account_id = info.pubkey
            cmd.transfer_asset.dest_account_id = info.pubkey_dest
            cmd.transfer_asset.asset_id = info.asset_id
            # fixme
            cmd.transfer_asset.amount.integer_part = info.amount

    tx.body.commands.extend(commands)
    meta = Transaction.Meta(creator_account_id=info.pubkey, tx_counter=randint(0, 2 ** 32 - 1))

def recalc_sign(tx: Transaction, keys: List[Tuple]):
    msg = None # todo: extract message for signing
    h = crypto.hash(msg)
    signs = []
    for key in keys:
        s = Signature(pubkey=key[1], signature=crypto.sign(h, key[0]))
        signs.append(s)
    tx.header.signatures.MergeFrom(signs)