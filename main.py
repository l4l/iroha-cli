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

from time import time
from random import randint

import grpc

from block_pb2 import Header, Transaction
from endpoint_pb2_grpc import CommandServiceStub
from primitive_pb2 import Signature
import config


def main():
    chan = grpc.insecure_channel(config.TORII_HOST + ":" + str(config.TORII_PORT))
    stub = CommandServiceStub(chan)
    # tx = block_pb2.Transaction(header=block_pb2.Header())
    pub = b"fed5"
    sig = Signature(pubkey=pub, signature=b"1234abcdef")
    hdr = Header(created_time=int(time()), signature=sig)
    meta = Transaction.Meta(creator_account_id=pub, tx_counter=randint(0, 2**32-1))
    body = Transaction.Body
    # stub.Torii


if __name__ == '__main__':
    main()
