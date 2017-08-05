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

import ed25519
import hashlib, sha3
from binascii import unhexlify


def create_keypair():
    """returns (sk, vk)"""
    return ed25519.create_keypair()

def sign(msg: bytes, pri: ed25519.SigningKey) -> bytes:
    return pri.sign(msg)

def verify(sig, msg: bytes, pub: ed25519.VerifyingKey) -> bool:
    try:
        pub.verify(sig, msg)
        return True
    except ed25519.BadSignatureError:
        return False

def mac(msg: bytes, pri: ed25519.SigningKey) -> (bytes, bytes):
    h = hash(msg)
    return h, sign(h, pri)

def hash(b: bytes) -> bytes:
    h = hashlib.sha3_256
    h.update(b)
    return h.digest()

def dump(key: bytes) -> bytes:
    return key.to_ascii(encoding='hex')

def undump(key: bytes) -> bytes:
    return unhexlify(key)
