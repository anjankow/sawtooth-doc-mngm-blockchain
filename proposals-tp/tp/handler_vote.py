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


def handle_vote(context, content):

    proposalID, voter = _decode_vote(content)

    if proposalID == '' or voter == '':
        LOGGER.warning(
            'missing params, voter: {'+voter+'}, proposalID: {'+proposalID+'}')
        return

    address = make_proposal_data_address(proposalID)
    state = get_state_data(context, address)
    if state == {} or state == None:
        LOGGER.warning('proposal does not exist: '+proposalID)
        return

    proposal = ProposalData(**state)
    LOGGER.debug('current proposal state:')
    LOGGER.debug(proposal)

    if voter in proposal.signers:
        LOGGER.info('proposal already signed by this signer: ' +
                    voter+', proposalID: '+proposalID)
        return

    proposal.signers.append(voter)

    voteThreshold = read_setting(
        context, 'proposal.vote.threshold', defaultValue=DEFAULT_VOTE_THRESHOLD)

    if len(proposal.signers) >= int(voteThreshold):
        LOGGER.info('vote threshold reached! signers: ' +
                    ' '.join(proposal.signers))
        proposal = _accept_proposal(context, proposal)

    state = proposal._asdict()
    LOGGER.debug('updated proposal:')
    LOGGER.debug(state)

    set_state_data(context, state, address)

    _add_proposal_to_voter(context, proposal, voter)


def _add_proposal_to_voter(context, proposal: ProposalData, voter: str):
    address = make_user_address(voter)
    LOGGER.debug('voter address:')
    LOGGER.debug(address)

    state = get_state_data(context, address)
    if state == {} or state == None:
        state = User(voted=[], accepted=[], active=[])._asdict()

    state['voted'].append(proposal.proposalID)

    LOGGER.debug('updated voter state:')
    LOGGER.debug(state)

    set_state_data(context, state, address)


def _accept_proposal(context, proposal: ProposalData) -> ProposalData:

    proposal = proposal.set_status('accepted')

    # update the user data
    address = make_user_address(
        proposal.author)
    LOGGER.debug('author address:')
    LOGGER.debug(address)

    state = get_state_data(context, address)
    LOGGER.debug('current author state:')
    LOGGER.debug(state)

    if state == {} or state == None:
        state = User(voted=[], accepted=[], active=[])._asdict()

    state['active'].remove(proposal.proposalID)
    state['accepted'].append(proposal.proposalID)

    LOGGER.debug('updated author state:')
    LOGGER.debug(state)

    set_state_data(context, state, address)

    # update the doc active proposals
    address = make_doc_address(proposal.category, proposal.docName)
    LOGGER.debug('doc address:')
    LOGGER.debug(address)

    state = get_state_data(context, address)

    if state == {} or state == None:
        state = Document(proposals={})._asdict()

    del state['proposals'][proposal.proposalID]

    set_state_data(context, state, address)

    # generate an event
    context.add_event(event_type='proposal_accepted',
                      data=(proposal.proposalID).encode('UTF-8'))

    # return proposal with updated state
    return proposal


def _decode_vote(content):

    try:
        proposalID = content['proposalID']
    except:
        proposalID = ''

    try:
        voter = content['voter']
    except:
        voter = ''

    return proposalID, voter
