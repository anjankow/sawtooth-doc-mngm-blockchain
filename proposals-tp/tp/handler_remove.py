from audioop import add
from calendar import c
from curses import newpad
from re import A
from select import select
from typing import List
import logging
import cbor
import hashlib
from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError
from .models import *
from .utils import *
from base64 import b64decode

LOGGER = logging.getLogger(__name__)

DEFAULT_VOTE_THRESHOLD = 1


def handle_remove(context, content):

    proposalID = _decode_remove(content)

    if proposalID == '':
        LOGGER.warning(
            'missing remove param: proposalID')
        return

    address = make_proposal_data_address(proposalID)
    state = get_state_data(context, address)
    if state == {} or state == None:
        LOGGER.warning('proposal data does not exist: '+proposalID)
        return

    proposal = ProposalData(**state)
    proposal = proposal.set_status(STATUS_REMOVED)

    state = proposal._asdict()
    LOGGER.debug('updated proposal:')
    LOGGER.debug(state)

    set_state_data(context, state, address)

    _remove_from_author(context, proposal)
    _remove_from_voters(context, proposal)
    _remove_from_doc(context, proposal)


def _remove_from_author(context, proposal: ProposalData):
    address = make_user_address(proposal.author)
    LOGGER.debug('author address:')
    LOGGER.debug(address)

    state = get_state_data(context, address)
    if state == {} or state == None:
        LOGGER.warning('proposal author doesn\'t exist: '+proposal.author)
        return

    state['active'].remove(proposal.proposalID)

    set_state_data(context, state, address)


def _remove_from_voters(context, proposal: ProposalData):
    for voter in proposal.signers:

        address = make_user_address(voter)
        LOGGER.debug('voter address:')
        LOGGER.debug(address)

        state = get_state_data(context, address)
        if state == {} or state == None:
            LOGGER.warning('user doesn\'t exist: '+voter)
            continue

        state['voted'].remove(proposal.proposalID)

        set_state_data(context, state, address)


def _remove_from_doc(context, proposal: ProposalData):
    address = make_doc_address(proposal.category, proposal.docName)
    LOGGER.debug('doc address:')
    LOGGER.debug(address)

    state = get_state_data(context, address)

    if state == {} or state == None:
        LOGGER.warning('doc doesn\'t exist: ' +
                       proposal.docName + ', ' + proposal.category)
        return

    updated = dict(state['proposals'])
    del updated[proposal.proposalID]

    LOGGER.debug('updated doc:')
    LOGGER.debug(updated)

    set_state_data(context, updated, address)


def _decode_remove(content):

    try:
        proposalID = content['proposalID']
    except:
        proposalID = ''

    return proposalID
