from typing import List, NamedTuple
from sawtooth_sdk.processor.exceptions import InvalidTransaction

STATUS_ACCEPTED = 'accepted'
STATUS_REMOVED = 'removed'
VALID_STATUSES = STATUS_ACCEPTED, STATUS_REMOVED


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
        if self.proposedStatus not in VALID_STATUSES:
            err += 'invalid proposedStatus: '+self.proposedStatus+'; '
        if self.contentHash == '' and self.proposedStatus != STATUS_REMOVED:
            err += 'contentHash is missing; '
        if self.author == '':
            err += 'author is missing; '

        if err != '':
            raise InvalidTransaction('validation error: '+err)


class StoredProposal(NamedTuple):
    proposalID: str
    author: str
    proposedStatus: str
    contentHash: str
