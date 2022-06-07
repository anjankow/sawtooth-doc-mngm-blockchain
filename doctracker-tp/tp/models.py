import hashlib
from typing import Dict, List, NamedTuple
from sawtooth_sdk.processor.exceptions import InvalidTransaction

FAMILY_NAME = 'doctracker'

FAMILY_ADDR_PREFIX = hashlib.sha512(
    FAMILY_NAME.encode('utf-8')).hexdigest()[0:6]


# to hold ids of documents created by this user
# and those that the user signed
USER_PREFIX = 'user'
# to hold a version of a document
DOC_PREFIX = 'doc'


STATUS_REMOVED = 'removed'
STATUS_ACTIVE = 'active'
STATUS_INVALID = 'invalid'


class DocumentVersion(NamedTuple):
    documentName: str
    category: str
    author: str
    contentHash: str
    version: int
    status: str
    proposalID: str
    signers: List[str]

    def set_status(self, status):
        dic = self._asdict()
        dic['status'] = status
        return DocumentVersion(**dic)


class User(NamedTuple):
    authored: List[str]
    signed: List[str]


def make_doc_address(category, docName, version) -> str:
    return FAMILY_ADDR_PREFIX + \
        hashlib.sha512(DOC_PREFIX.encode('utf-8')).hexdigest()[0:6] + \
        hashlib.sha512(category.encode('utf-8')).hexdigest()[0:6] + \
        hashlib.sha512(docName.encode('utf-8')).hexdigest()[0:48] + \
        ("%04d" % version)


def make_user_address(user) -> str:
    return FAMILY_ADDR_PREFIX + \
        hashlib.sha512(USER_PREFIX.encode('utf-8')).hexdigest()[0:6] + \
        hashlib.sha512(user.encode('utf-8')).hexdigest()[0:58]
