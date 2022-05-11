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

from typing import List
import logging
import cbor
import hashlib
from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError
from .models import ProposalInput, StoredProposal

LOGGER = logging.getLogger(__name__)


FAMILY_NAME = 'proposals'

FAMILY_ADDR_PREFIX = hashlib.sha512(
    FAMILY_NAME.encode('utf-8')).hexdigest()[0:6]


def _make_proposal_address(category, docName):
    return FAMILY_ADDR_PREFIX + hashlib.sha512(
        category.encode('utf-8')).hexdigest()[0:6] + hashlib.sha512(
        docName.encode('utf-8')).hexdigest()[0:58]


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
        transactionInput = _decode_transaction(transaction)
        transactionInput.validate()

        address = _make_proposal_address(
            transactionInput.category, transactionInput.docName)

        state = _get_state_data(context, address)

        updated_state = _insert_new_proposal(
            transactionInput, state)

        _set_state_data(context, updated_state, address)


def _insert_new_proposal(newProposal: ProposalInput, state: dict) -> dict:
    LOGGER.debug('current state:')
    LOGGER.debug(state)

    if state == {}:
        LOGGER.debug('state is empty, creating...')
        state['category'] = newProposal.category
        state['docName'] = newProposal.docName
        state['proposals'] = []

    updated = dict(state.items())
    newProposItem = StoredProposal(
        newProposal.proposalID, newProposal.author, newProposal.proposedStatus, newProposal.contentHash)
    proposList = list(state['proposals'])
    proposList.append(newProposItem)
    updated['proposals'] = proposList

    LOGGER.debug('updated proposals:')
    LOGGER.debug(updated['proposals'])

    return updated


def _get_state_data(context, address):
    state_entries = context.get_state([address])

    try:
        return cbor.loads(state_entries[0].data)
    except IndexError:
        return {}
    except Exception as e:
        raise InternalError('Failed to load state data') from e


def _set_state_data(context, state, address):

    encoded = cbor.dumps(state)

    addresses = context.set_state({address: encoded})
    LOGGER.debug('updated proposals:')

    if not addresses:
        raise InternalError('State error')


def _decode_transaction(transaction) -> ProposalInput:

    try:
        content = cbor.loads(transaction.payload)
    except Exception as e:
        raise InvalidTransaction('Invalid payload serialization') from e

    try:
        category = content['category']
    except:
        pass

    try:
        docName = content['docName']
    except:
        pass
    try:
        contentHash = content['contentHash']
    except:
        pass
    try:
        author = content['author']
    except:
        pass
    try:
        proposedStatus = content['proposedStatus']
    except:
        pass

    proposalID = transaction.signature

    return ProposalInput(category, proposalID, docName, contentHash, author, proposedStatus)
