#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import json
import re
import traceback
import requests
import threading
from slacksocket import SlackSocket
from slackclient import SlackClient
from block_io import BlockIo
version = 2  # API version
from key_pin import *

from slackbotutils import *

block_io_doge = BlockIo(blockio_api_doge_key, blockio_secret_pin,version)
block_io_btc = BlockIo(blockio_api_btc_key, blockio_secret_pin, version)
block_io_ltc = BlockIo(blockio_api_ltc_key, blockio_secret_pin, version)
ss = SlackSocket(slack_token, translate=False)  # translate will lookup and replace user and channel IDs with their human-readable names. default true.
sc = SlackClient(slack_token)
url = 'https://shapeshift.io/shift'
coincap_doge = 'http://www.coincap.io/page/DOGE'
coincap_btc = 'http://www.coincap.io/page/BTC'
coincap_ltc = 'http://www.coincap.io/page/LTC'
cryptocomp_doge = \
    'https://www.cryptocompare.com/api/data/price?fsym=DOGE&tsyms=USD'
cryptocomp_btc = \
    'https://www.cryptocompare.com/api/data/price?fsym=BTC&tsyms=USD'
cryptocomp_ltc = \
    'https://www.cryptocompare.com/api/data/price?fsym=LTC&tsyms=USD'
shapeshift_pubkey = \
    '06c04cfc9f18632d50ca546ba4f3dc49edcaf6217e3cefe73ed98d92cc2f37e764df8371fc3d23847aee4a4d65bdaa2defd30ca43311378827a94146feb017cb'
min_amount = {'doge': 2.0, 'ltc': 0.002, 'btc': 0.0002}


# Logging things to a file makes it easier to find where the bot had errors
# and puts major errors in a pernament place

def log(line):
    print line
    logFile = open('slackbot.log', 'ab+')
    logFile.write(line)
    logFile.close()


def main():
    time.sleep(1)
    for event in ss.events():
        j = json.loads(event.json)
        if j['type'] != 'message':
            continue

        if '!tipbot' not in j['text']:
            continue

        print j['text']

        # user name/id lookups

        id2name = {}
        name2id = {}
        try:
            users = sc.api_call('users.list')
            for user in users['members']:
                id2name[user['id']] = user['name']
                name2id[user['name']] = user['id']
        except:

            # Log an error and stop the current loop if you cant build the user lookups

            log('ERROR: Failed to build user lookups')
            break

        # split message and find '!tipbot'

        splitmessage = j['text'].split()
        log('PROGRESS: found message ' + str(splitmessage))
        tipindex = 0
        for i in range(0, len(splitmessage), 1):
            if splitmessage[i] == '!tipbot':
                tipindex = i
                break
        try:
            command = splitmessage[tipindex + 1]
        except:
            # Log an error if the command can't be found and stop.
            log('ERROR: Command could not be found')
            break
        # !tipbot tip
        if command == 'tip':
            tip(command, splitmessage, tipindex, id2name, name2id)
        elif command == 'make':
        # !tipbot make it rain
            rain(command, splitmessage, tipindex, id2name, name2id)
        elif command == 'withdraw':
            withdraw(command, splitmessage, tipindex, id2name, name2id)
        elif command == 'shift':
        # tipbot shift
            shift(command, splitmessage, tipindex, id2name, name2id)
        elif command == 'addresses':
        # !tipbot addresses
            addresses(command, splitmessage, tipindex, id2name, name2id)
        elif command == 'register':
        # !tipbot register
            try:
                block_io_doge.get_new_address(label=j['user'])
            except:
                traceback.print_exc()
                log('ERROR: failed to create doge address for '
                    + id2name[j['user']] + ' (' + j['user'] + ')')
            try:
                block_io_ltc.get_new_address(label=j['user'])
            except:
                traceback.print_exc()
                log('ERROR: failed to create ltc address for '
                    + id2name[j['user']] + ' (' + j['user'] + ')')
            try:
                block_io_btc.get_new_address(label=j['user'])
            except:
                traceback.print_exc()
                log('ERROR: failed to create btc address for '
                    + id2name[j['user']] + ' (' + j['user'] + ')')

            log('PROGRESS: ' + sc.api_call('chat.postMessage',
                channel=j['channel'], text=id2name[j['user']]
                + ' registered!  :tada:', username='pybot',
                icon_emoji=':robot_face:'))
        elif command == 'check':
        # !tipbot check
            check()
        elif command == 'help':
        # !tipbot help
            log('PROGRESS: ' + sc.api_call('chat.postMessage',
                channel=j['channel'],
                text='https://github.com/peoplma/slacktipbot',
                username='pybot', icon_emoji=':robot_face:'))


def secondary():
    try:
        while True:
            main()
    except:
        log("ERROR: "+str(traceback.print_exc()))
        log('ERROR: Resuming in 2sec...')
        time.sleep(2)
        log('ERROR: Resumed')


while True:
    secondary()
