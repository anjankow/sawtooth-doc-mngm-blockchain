from sawtooth_sdk.processor.core import TransactionProcessor
from tp.handler import ProposalsHandler

import logging
import sys

def main():
    logging.info('proposals-tp start!')
    processor = TransactionProcessor(url='tcp://validator:4004')

    handler = ProposalsHandler('org')

    processor.add_handler(handler)

    processor.start()
    
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ])
    main()