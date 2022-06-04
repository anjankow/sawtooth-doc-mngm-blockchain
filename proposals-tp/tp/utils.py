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
from .setting_pb2 import Setting
import logging
import hashlib

LOGGER = logging.getLogger(__name__)

SETTINGS_NAMESPACE = '000000'
_SETTINGS_MAX_KEY_PARTS = 4
_SETTINGS_ADDRESS_PART_SIZE = 16


def get_setting_addr(key: str) -> str:
    # source: https://github.com/hyperledger/sawtooth-core/blob/6092b48b4de3498df0416c6ccf2f81f4b5468995/cli/sawtooth_cli/settings.py#L150
    """Creates the state address for a given setting key.
    """
    key_parts = key.split('.', maxsplit=_SETTINGS_MAX_KEY_PARTS - 1)
    key_parts.extend([''] * (_SETTINGS_MAX_KEY_PARTS - len(key_parts)))

    def _short_hash(in_str):
        return hashlib.sha256(in_str.encode()).hexdigest()[:_SETTINGS_ADDRESS_PART_SIZE]

    return SETTINGS_NAMESPACE + ''.join(_short_hash(x) for x in key_parts)


def read_setting(context, key: str, defaultValue):
    state = context.get_state([get_setting_addr(key)])
    data = state[0].data

    set = Setting()
    set.ParseFromString(data)

    if len(set.entries) < 1:
        LOGGER.info('setting missing: '+key+', using default value: ' +
                    str(defaultValue))

        return defaultValue

    if set.entries[0].key != key:
        LOGGER.warning('read unexpected setting: ' +
                       set.entries[0].key+', expected: '+key)
        return defaultValue

    setValue = set.entries[0].value
    LOGGER.debug('read setting: ' + key + '=' + str(setValue))

    return setValue


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
