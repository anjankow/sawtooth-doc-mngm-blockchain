from sawtooth_sdk.processor.exceptions import InvalidTransaction
from .models import *
from .utils import *

LOGGER = logging.getLogger(__name__)


def invalidate_doc(context, content):
    address = content['address']
    if address == '':
        raise InvalidTransaction(
            'address parameter is missing, can\'t invalidate the transaction')

    state = get_state_data(context, address)
    if state == {} or state == None:
        LOGGER.info("can't invalidate, the document doesn't exist: "+address)

    doc = DocumentVersion(**state)
    updated = doc.set_status(STATUS_INVALID)

    set_state_data(context, updated._asdict(), address)
