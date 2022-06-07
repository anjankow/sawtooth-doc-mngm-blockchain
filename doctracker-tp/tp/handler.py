import logging
import cbor
import hashlib
from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError

from .handler_insert import *
from .handler_invalidate import *


from sawtooth_sdk.processor.handler import TransactionHandler

LOGGER = logging.getLogger(__name__)

ACTION_INSERT_DOC = 'insert'
ACTION_INVALIDATE = 'invalidate'


class DocTrackerHandler(TransactionHandler):
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

            if action == ACTION_INSERT_DOC:
                LOGGER.info('inserting new document')
                handle_new_document(context, content)
            elif action == ACTION_INVALIDATE:
                LOGGER.info('invalidating the doc')
                invalidate_doc(context, content)

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

    return action, content
