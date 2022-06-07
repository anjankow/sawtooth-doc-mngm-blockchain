from .models import *


def handle_new_document(context, content):
    transactionInput = _decode_new_doc_version(content)
    transactionInput.validate()

    _insert_doc_version(context, transactionInput)
    _add_doc_author(context, transactionInput)
    _add_doc_to_signers(context, transactionInput)

    return


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
