import hashlib
from typing import Dict, List, NamedTuple
from sawtooth_sdk.processor.exceptions import InvalidTransaction

FAMILY_NAME = 'proposals'

FAMILY_ADDR_PREFIX = hashlib.sha512(
    FAMILY_NAME.encode('utf-8')).hexdigest()[0:6]

# to hold all proposal related data
PROPOSAL_DATA_PREFIX = 'proposaldata'
# to hold proposalIDs of active and accepted proposals created by the user
# and proposalIDs he was voting on
USER_PREFIX = 'user'
# to hold proposal IDs of active proposals for the doc
DOC_PREFIX = 'doc'


STATUS_ACCEPTED = 'accepted'
STATUS_REMOVED = 'removed'
STATUS_ACTIVE = 'active'

ProposalID = str
UserID = str


class ProposalData(NamedTuple):
    proposalID: str
    docName: str
    category: str
    author: UserID
    signers: List[UserID]
    proposedDocStatus: str
    currentStatus: str
    contentHash: str

    def set_status(self, status):
        dic = self._asdict()
        dic['currentStatus'] = status
        return ProposalData(**dic)


class User(NamedTuple):
    voted: List[ProposalID]
    active: List[ProposalID]
    accepted: List[ProposalID]


class Document(NamedTuple):
    # proposal ID and corresponding content hash
    proposals: Dict[ProposalID, str]


def make_doc_address(category, docName) -> str:
    return FAMILY_ADDR_PREFIX + \
        hashlib.sha512(DOC_PREFIX.encode('utf-8')).hexdigest()[0:6] + \
        hashlib.sha512(category.encode('utf-8')).hexdigest()[0:6] + \
        hashlib.sha512(docName.encode('utf-8')).hexdigest()[0:52]


def make_proposal_data_address(proposalID) -> str:
    return FAMILY_ADDR_PREFIX + \
        hashlib.sha512(PROPOSAL_DATA_PREFIX.encode('utf-8')).hexdigest()[0:6] + \
        hashlib.sha512(proposalID.encode('utf-8')).hexdigest()[0:58]


def make_user_address(user) -> str:
    return FAMILY_ADDR_PREFIX + \
        hashlib.sha512(USER_PREFIX.encode('utf-8')).hexdigest()[0:6] + \
        hashlib.sha512(user.encode('utf-8')).hexdigest()[0:58]


print(make_user_address('alabaster'))
print(make_proposal_data_address(
    '60a9e27b2ca2d845d7304a0955a1b358ec6e66d952bfc199b862d05ad365588d4f2272a0d570117518bb781667b6012b0f89206e89baabfe1bc8792c009bfcff'))
print(make_doc_address('general2', 'docname'))
