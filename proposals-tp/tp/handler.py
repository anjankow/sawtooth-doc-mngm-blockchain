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

import hashlib
import logging
from nis import cat
from select import select
from typing import List

import cbor
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.handler import TransactionHandler

from .handler_add import *
from .handler_remove import *
from .handler_vote import *
from .models import *

LOGGER = logging.getLogger(__name__)


ACTION_INSERT_PROPOSAL = 'insert'
ACTION_VOTE_PROPOSAL = 'vote'
ACTION_DELETE_PROPOSAL = 'delete'


class ProposalsHandler(TransactionHandler):
    def __init__(self, namespace_prefix):
        self._namespace_prefix = namespace_prefix

    @property
    def family_name(self):
        return FAMILY_NAME

    @property
    def family_versions(self):
        return ['1.0']

    @property
    def namespaces(self):
        return [self._namespace_prefix]

    def apply(self, transaction, context):
        # use try-except here to workaround the bug of endless loop of the tp on error
        try:
            action, content = _decode_action(transaction)

            if action == ACTION_INSERT_PROPOSAL:
                LOGGER.info('inserting new proposal')
                handle_new_proposal(context, content)
            elif action == ACTION_VOTE_PROPOSAL:
                LOGGER.info('voting on proposal')
                handle_vote(context, content)
            elif action == ACTION_DELETE_PROPOSAL:
                LOGGER.info('removing proposal')
                handle_remove(context, content)

            else:
                raise InvalidTransaction('action not defined: '+action)
        except Exception as e:
            print(e)


def _decode_action(transaction):

    try:
        content = cbor.loads(transaction.payload)
    except Exception as e:
        raise InvalidTransaction('Invalid payload serialization') from e

    try:
        action = content['action']
    except Exception as e:
        raise InvalidTransaction('no action defined in the payload') from e

    del content['action']
    return action, content
