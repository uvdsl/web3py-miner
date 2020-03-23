from web3 import Web3, HTTPProvider
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
    print('==', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '==', message)


def checkWork(web3, threads, check_alive):
    sleep_time = 15
    if len(web3.eth.getBlock('pending').transactions) > 0:
        if not web3.eth.mining:
            log('Pending transactions! Mining ...')
            pool = web3.geth.txpool.status()
            log('Pool: ' + pool.get('pending') +
                ' (pending), ' + pool.get('queued') + ' (queued)')
            web3.geth.miner.start(threads)
        sleep_time = 1
    else:
        if web3.eth.mining:
            web3.geth.miner.stop()
            log('Latest Block: ' + str(web3.eth.blockNumber))
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


CONNECTION = 'http://localhost:8543'
THREADS = 2


while True:
    time.sleep(5)
    try:
        log('Connecting to Geth ...')
        w3 = Web3(HTTPProvider(CONNECTION))
        log('Connected at block: ' + str(w3.eth.blockNumber))
    except:
        log('Did not reach Geth ...')
    else:
        try:
            sleepAtWork(w3, THREADS)
        except:
            log('Lost connection to Geth ...')
