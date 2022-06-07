from .models import *
from .utils import *


def handle_new_document(context, content):
    doc = DocumentVersion(**content)
    doc.validate()

    _insert_doc_version(context, doc)
    _add_doc_to_author(context, doc)
    _add_doc_to_signers(context, doc)

    return


def _insert_doc_version(context, doc: DocumentVersion):

    address = make_doc_address(doc.category, doc.documentName, doc.version)

    LOGGER.debug('doc address:')
    LOGGER.debug(address)

    state = get_state_data(context, address)
    if not(state == {} or state == None):
        raise InvalidTransaction("doc version already exists! %s %s %d" % (
            doc.documentName, doc.category, doc.version))

    state = doc._asdict()
    set_state_data(context, state, address)


def _add_doc_to_author(context, doc: DocumentVersion):

    address = make_user_address(doc.author)
    LOGGER.debug('author address:')
    LOGGER.debug(address)

    state = get_state_data(context, address)

    if state == {} or state is None:
        user = User(signed=[], authored=[])
    else:
        user = User(**state)

    docAddr = make_doc_address(doc.category, doc.documentName, doc.version)
    user.authored.append(docAddr)

    LOGGER.debug('updated user:')
    LOGGER.debug(user)

    set_state_data(context, user._asdict(), address)


def _add_doc_to_signers(context, doc: DocumentVersion):
    docAddr = make_doc_address(doc.category, doc.documentName, doc.version)

    for signer in doc.signers:
        address = make_user_address(signer)

        LOGGER.debug('signer address:')
        LOGGER.debug(address)

        state = get_state_data(context, address)

        if state == {} or state is None:
            user = User(signed=[], authored=[])
        else:
            user = User(**state)

        user.signed.append(docAddr)

        LOGGER.debug('updated signer:')
        LOGGER.debug(user)

        set_state_data(context, user._asdict(), address)
