# Copyright 2016 Intel Corporation
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
# ------------------------------------------------------------------------------

# based on https://github.com/hyperledger/sawtooth-sdk-python/blob/6885a1cbfc210a14fc2406f2dae5504c9881602c/examples/intkey_python/sawtooth_intkey/processor/handler.py


import cbor
from sawtooth_sdk.processor.exceptions import InternalError
import logging

LOGGER = logging.getLogger(__name__)


def get_state_data(context, address):
    state_entries = context.get_state([address])

    try:
        return cbor.loads(state_entries[0].data)
    except IndexError:
        return {}
    except Exception as e:
        raise InternalError('Failed to load state data') from e


def set_state_data(context, state, address):

    encoded = cbor.dumps(state)

    addresses = context.set_state({address: encoded})

    if not addresses:
        raise InternalError('State error')
