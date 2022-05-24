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

LOGGER = logging.getLogger(__name__)


def handle_new_proposal(context, transaction, content):
    transactionInput = _decode_new_proposal(content)
    transactionInput.validate()

    LOGGER.debug('inserting proposal data')
    _insert_proposal_data(context, transactionInput)
    LOGGER.debug('adding the proposal to the doc')
    _add_proposal_to_doc(context, transactionInput)
    LOGGER.debug('adding the proposal to the author')
    _add_proposal_to_author(context, transactionInput)


class ProposalInput(NamedTuple):
    category: str
    proposalID: str
    docName: str
    contentHash: str
    author: str
    proposedStatus: str

    def validate(self):
        err = ''
        if self.category == '':
            err += 'category is missing; '
        if self.proposalID == '':
            err += 'proposal ID is missing; '
        if self.docName == '':
            err += 'docName is missing; '
        if not (self.proposedStatus == STATUS_ACTIVE or self.proposedStatus == STATUS_REMOVED):
            err += 'invalid proposedStatus: '+self.proposedStatus+'; '
        if self.contentHash == '' and self.proposedStatus != STATUS_REMOVED:
            err += 'contentHash is missing; '
        if self.author == '':
            err += 'author is missing; '

        if err != '':
            raise InvalidTransaction('validation error: '+err)


def _add_proposal_to_author(context, newProposal: ProposalInput):
    address = make_user_address(
        newProposal.author)
    LOGGER.debug('author address:')
    LOGGER.debug(address)

    state = get_state_data(context, address)
    LOGGER.debug('current author state:')
    LOGGER.debug(state)

    if state == {} or state == None:
        state = User(signed=[], accepted=[], active=[])._asdict()

    state['active'].append(newProposal.proposalID)

    LOGGER.debug('updated author state:')
    LOGGER.debug(state)

    set_state_data(context, state, address)


def _insert_proposal_data(context, newProposal: ProposalInput):

    address = make_proposal_data_address(newProposal.proposalID)
    LOGGER.debug('proposal ID:')
    LOGGER.debug(newProposal.proposalID)
    LOGGER.debug('proposal address:')
    LOGGER.debug(address)

    proposal = ProposalData(proposalID=newProposal.proposalID,
                            docName=newProposal.docName,
                            category=newProposal.category,
                            author=newProposal.author,
                            signers=[],
                            proposedDocStatus=newProposal.proposedStatus,
                            currentStatus=STATUS_ACTIVE,
                            contentHash=newProposal.contentHash)

    state = proposal._asdict()
    set_state_data(context, state, address)


def _add_proposal_to_doc(context, newProposal: ProposalInput):

    address = make_doc_address(
        newProposal.category, newProposal.docName)
    LOGGER.debug('doc address:')
    LOGGER.debug(address)

    state = get_state_data(context, address)

    LOGGER.debug('current state:')
    LOGGER.debug(state)

    if state == {} or state == None:
        state = Document(proposals={})._asdict()

    state['proposals'][newProposal.proposalID] = newProposal.contentHash

    LOGGER.debug('updated doc:')
    LOGGER.debug(state)

    set_state_data(context, state, address)


def _decode_new_proposal(content) -> ProposalInput:

    try:
        proposalID = content['proposalID']
    except:
        pass

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

    return ProposalInput(category, proposalID, docName, contentHash, author, proposedStatus)
