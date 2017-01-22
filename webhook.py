#!/usr/bin/env python

import os
import bottle
import pprint
import logging
import subprocess
from bottle import Bottle, run, request

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# create console handler
handler = logging.StreamHandler()
handler.setLevel(logging.ERROR)

# create logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

# this service reads from environment
# the following vars:
# LISTEN_ADDRESS, LISTEN_PORT, REPO_FULL_NAME,
# REPO_BRANCH & REPO_PATH

LISTEN_ADDRESS = os.environ['LISTEN_ADDRESS']
LISTEN_PORT = os.environ['LISTEN_PORT']
REPO_FULL_NAME = os.environ['REPO_FULL_NAME']
REPO_PATH = os.environ['REPO_PATH']
CMD = ['cd', REPO_PATH, '&&', 'git', 'pull', '--rebase']

app = bottle.app()

@bottle.post('/webhook')
def hook():
    pp = pprint.PrettyPrinter(indent=4)
    payload = request.json
    logger.debug(pp.pprint(payload))
    name = payload['repository']['full_name'] # not sure that that's the right key
    logger.info('Receive request for %s', name)
    if name == REPO_FULL_NAME:
        logger.info('Execute %s', CMD)
        subprocess.Popen(CMD)
    else:
        logger.error('Request is for different repo than %s', REPO_FULL_NAME)


def main():
    bottle.run(app=app, host=LISTEN_ADDRESS, port=LISTEN_PORT, quiet=False, debug=True)


if __name__ == '__main__':
    main()
