#!/bin/python3
# based on https://github.com/sharan98/sawtooth-voting/blob/master/client/vote.py

import hashlib
import sys
from datetime import datetime
import random
import requests
import logging
import time
import yaml

from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from sawtooth_signing import ParseError
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey

from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.batch_pb2 import BatchList
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
from sawtooth_sdk.protobuf.batch_pb2 import Batch


base_url = 'http://localhost:8008'


def hash(data):
    return hashlib.sha512(data.encode()).hexdigest()


def send_to_rest_api(suffix, data=None, content_type=None):
    url = "{}/{}".format(base_url, suffix)
    headers = {}
    logging.debug('sending to ' + url)
    if content_type is not None:
        headers['Content-Type'] = content_type

    try:
        if data is not None:
            logging.debug("sending request POST")
            result = requests.post(url, headers=headers,
                                   data=data, allow_redirects=True)
            logging.info("request sent POST")
        else:
            result = requests.get(url, headers=headers)
        if not result.ok:
            logging.debug("Error {}: {}".format(
                result.status_code, result.reason))
            raise Exception("Error {}: {}".format(
                result.status_code, result.reason))
    except requests.ConnectionError as err:
        logging.debug('Failed to connect to {}: {}'.format(url, str(err)))
        raise Exception('Failed to connect to {}: {}'.format(url, str(err)))
    except BaseException as err:
        raise Exception(err)
    return result.text


def wait_for_status(batch_id, result, wait=10):
    '''Wait until transaction status is not PENDING (COMMITTED or error).
        'wait' is time to wait for status, in seconds.
    '''
    if wait and wait > 0:
        waited = 0
        start_time = time.time()
        logging.info('url : ' + base_url +
                     "/batch_statuses?id={}&wait={}".format(batch_id, wait))
        while waited < wait:
            result = send_to_rest_api(
                "batch_statuses?id={}&wait={}".format(batch_id, wait))
            status = yaml.safe_load(result)['data'][0]['status']
            waited = time.time() - start_time

            if status != 'PENDING':
                return result
        logging.debug(
            "Transaction timed out after waiting {} seconds.".format(wait))
        return "Transaction timed out after waiting {} seconds.".format(wait)
    else:
        return result


def main():
    familyName = "doctracker"
    familyNameHash = hash(familyName)[:6]
    category = "general"
    categoryHash = hash(category)[:6]
    docContent = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    docID = "doc1"
    author = "Agatka"
    proposedState = "accepted"

    if len(sys.argv) > 1:
        # argument 1: doc ID
        docID = sys.argv[1]
    if len(sys.argv) > 2:
        # argument 2: author
        author = sys.argv[2]
    if len(sys.argv) > 3:
        # argument 3: docContent
        docContent = sys.argv[3]

    docHash = hash(docContent)
    docIDHash = hash(docID)[:58]
    
    DOC_ADDRESS = familyNameHash + categoryHash + docIDHash

    context = create_context('secp256k1')
    private_key = context.new_random_private_key()
    signer = CryptoFactory(context).new_signer(private_key)
    public_key = signer.get_public_key().as_hex()

    payload = ";".join([category, proposedState, author, docHash])
    logging.debug("payload: "+payload)

    input_address_list = [DOC_ADDRESS]
    output_address_list = [DOC_ADDRESS]
    # Create a TransactionHeader.
    header = TransactionHeader(
        batcher_public_key=public_key,
        family_name=familyName,
        family_version="1.0",
        inputs=input_address_list,
        outputs=output_address_list,
        nonce=random.random().hex().encode(),
        payload_sha512=hash(payload),
        signer_public_key=public_key,
    ).SerializeToString()

    # Create a Transaction from the header and payload above.
    transaction = Transaction(
        header=header,
        payload=payload.encode(),                 # encode the payload
        header_signature=signer.sign(header)
    )

    transaction_list = [transaction]

    # Create a BatchHeader from transaction_list above.
    header = BatchHeader(
        signer_public_key=public_key,
        transaction_ids=[txn.header_signature for txn in transaction_list]
    ).SerializeToString()

    # Create Batch using the BatchHeader and transaction_list above.
    batch = Batch(
        header=header,
        transactions=transaction_list,
        header_signature=signer.sign(header)
    )

    # Create a Batch List from Batch above
    batch_list = BatchList(batches=[batch])
    batch_id = batch_list.batches[0].header_signature

    # Send batch_list to the REST API
    result = send_to_rest_api(
        "batches", batch_list.SerializeToString(), 'application/octet-stream')

    logging.debug('waiting for result')
    # Wait until transaction status is COMMITTED, error, or timed out
    logging.info('result: ' + wait_for_status(batch_id, result))


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ])
    main()
