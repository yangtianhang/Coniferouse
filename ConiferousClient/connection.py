#!/bin/env python
# 
# Copyright 2011 Eran Sandler <eran@sandler.co.il>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from thrift.transport import TSocket

try:
    from thrift.protocol import TBinaryProtocolAccelerated as TBinaryProtocol
except ImportError:
    from thrift.protocol import TBinaryProtocol

# Small hack to avoid the need to set PYTHONPATH environment variable
# sys.path.append(os.path.join(os.path.dirname(__file__), "thrift", "gen-py"))

from Coniferous import Coniferous
from Coniferous.constants import *


class Connection(object):
    def __init__(self, host, port=30303, token="a"):
        self._host = host
        self._port = port
        self._token = token

        self._transport = TSocket.TSocket(host, port)
        self._transport = TTransport.TFramedTransport(self._transport)
        self._protocol = TBinaryProtocol.TBinaryProtocol(self._transport)
        self._client = Coniferous.Client(self._protocol)
        self._transport.open()

    def get_ids(self, count):
        return self._client.get_ids(self._token, count)
