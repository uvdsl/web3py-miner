import argparse
from web3 import Web3, HTTPProvider, WebsocketProvider
from datetime import datetime
from random import random, choice
import time


PUNS = [
    'Still alive and lazy!',
    'I\'m considering getting into the steel and mining business\t' +
    '... just need to iron out the details.',
    'Asteroid mining!\t' +
    'It is on the horizon...',
    'I really wanted to be a mining engineer.\t' +
    'But I was lousy adit...',
    'What do you call it when two mining companies merge?\t' +
    'A COALition.',
    'What do you get when you drop a piano down a mine shaft?\t' +
    'A flat miner.',
    'I regret getting into the mine alone...\t' +
    'Deeply.',
]


def getLazyAnswer():
    if random() > 0.975:
        return choice(PUNS)
    return PUNS[0]


def log(message):
    print('== {} == {}'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))


def checkWork(web3, threads, check_alive):
    sleep_time = 15
    if len(web3.eth.getBlock('pending').transactions) > 0:
        if not web3.eth.mining:
            log('Pending transactions! Mining ...')
            pool = web3.geth.txpool.status()
            log('Pool: {} (pending), {} (queued)'.format(pool.get('pending'), pool.get('queued')))
            web3.geth.miner.start(threads)
        sleep_time = 1
    else:
        if web3.eth.mining:
            web3.geth.miner.stop()
            log('Latest Block: {}'.format(web3.eth.blockNumber))
            log('No transactions! Mining stopped.')
        if check_alive == 0:
            log(getLazyAnswer())
    return sleep_time


def sleepAtWork(web3, threads):
    check_alive = 0
    while True:
        sleep_time = checkWork(web3, threads, check_alive)
        time.sleep(sleep_time)
        check_alive += 1
        checks_in_a_minute = 60 / sleep_time
        if(check_alive >= 1*checks_in_a_minute):
            check_alive = 0


####################
### BEGIN SCRIPT ###
####################

DEFAULT_CONNECTION = 'ws://localhost:8546'
provider = WebsocketProvider(DEFAULT_CONNECTION) # default
threads = 1 # default

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", help="Geth connection endpoint, default: {}".format(DEFAULT_CONNECTION))
parser.add_argument("-t", "--threads", help="Number of threads to mine with, default: 1")
args = parser.parse_args()

if args.endpoint:
    if args.endpoint.startswith('http://'):
        provider = HTTPProvider(args.endpoint)
    elif args.endpoint.startswith('ws://'):
        provider = WebsocketProvider(args.endpoint)
    else:
        log("What is this endpoint? Falling back to default ... ")

if args.threads:
    threads = int(args.threads)

log(provider)
plural = "" if threads <= 1 else "s"
log('Mining with {} worker thread{}.'.format(threads, plural))

while True:
    try:
        log('Connecting to Geth ...')
        w3 = Web3(provider)
        log('Connected at block: {}'.format(w3.eth.blockNumber))
    except:
        log('Did not reach Geth ...')
    else:
        try:
            sleepAtWork(w3, threads)
        except:
            log('Lost connection to Geth ...')
    time.sleep(2)
