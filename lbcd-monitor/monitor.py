#!/usr/bin/python
# -*- coding: utf-8 -*-

# cribbed from https://gist.github.com/ageis/a0623ae6ec9cfc72e5cb6bde5754ab1f

import json
import time
import subprocess
import sys
import os
from prometheus_client import start_http_server, Gauge, Counter

# Create Prometheus metrics to track bitcoind stats.
LBCD_BLOCKS = Gauge('lbcd_blocks', 'Block height')
LBCD_DIFFICULTY = Gauge('lbcd_difficulty', 'Difficulty')
LBCD_PEERS = Gauge('lbcd_peers', 'Number of peers')
LBCD_HASHPS = Gauge('lbcd_hashps', 'Estimated network hash rate per second')

LBCD_ERRORS = Counter('lbcd_errors', 'Number of errors detected')
LBCD_UPTIME = Gauge('lbcd_uptime', 'Number of seconds the Bitcoin daemon has been running')

LBCD_MEMPOOL_BYTES = Gauge('lbcd_mempool_bytes', 'Size of mempool in bytes')
LBCD_MEMPOOL_SIZE = Gauge('lbcd_mempool_size', 'Number of unconfirmed transactions in mempool')

LBCD_LATEST_BLOCK_SIZE = Gauge('lbcd_latest_block_size', 'Size of latest block in bytes')
LBCD_LATEST_BLOCK_TXS = Gauge('lbcd_latest_block_txs', 'Number of transactions in latest block')

LBCD_NUM_CHAINTIPS = Gauge('lbcd_num_chaintips', 'Number of known blockchain branches')

LBCD_TOTAL_BYTES_RECV = Gauge('lbcd_total_bytes_recv', 'Total bytes received')
LBCD_TOTAL_BYTES_SENT = Gauge('lbcd_total_bytes_sent', 'Total bytes sent')

LBCD_LATEST_BLOCK_INPUTS = Gauge('lbcd_latest_block_inputs', 'Number of inputs in transactions of latest block')
LBCD_LATEST_BLOCK_OUTPUTS = Gauge('lbcd_latest_block_outputs', 'Number of outputs in transactions of latest block')



PORT = int(os.getenv('PROMETHEUS_PORT', 2112))
LBCCTL_PATH = os.getenv('LBCCTL_PATH')
if LBCCTL_PATH is None:
    raise Exception("LBCCTL_PATH env var required")



def lbcd(cmd):
    p = subprocess.Popen([LBCCTL_PATH, cmd], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p.communicate()[0]
    return json.loads(output.decode('utf-8'))


def lbcctl(cmd):
    p = subprocess.Popen([LBCCTL_PATH, cmd], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p.communicate()[0]
    return output.decode('utf-8')


def get_block(block_height):
    try:
        blockhash = subprocess.check_output([LBCCTL_PATH, 'getblockhash', block_height]).rstrip()
        block = subprocess.check_output([LBCCTL_PATH, 'getblock', blockhash]).rstrip()
    except Exception as e:
        print(e)
        print('Error: Can\'t retrieve block number ' + block_height + ' from lbcd.')
        return None
    return json.loads(block.decode('utf-8'))


def get_raw_tx(txid):
    try:
        rawtx = subprocess.check_output([LBCCTL_PATH, 'getrawtransaction', txid, '1'])
    except Exception as e:
        print(e)
        print('Error: Can\'t retrieve raw transaction ' + txid + ' from lbcd.')
        return None
    return json.loads(rawtx.decode('utf-8'))


def main():
    # Start up the server to expose the metrics.
    start_http_server(PORT)
    while True:
        info = lbcd('getinfo')
        LBCD_BLOCKS.set(info['blocks'])
        LBCD_PEERS.set(info['connections'])
        LBCD_DIFFICULTY.set(info['difficulty'])

        if info['errors']:
            LBCD_ERRORS.inc()

        LBCD_HASHPS.set(float(lbcctl('getnetworkhashps')))
        LBCD_UPTIME.set(int(lbcctl('uptime')))
 
        #chaintips = len(lbcd('getchaintips'))
        #LBCD_NUM_CHAINTIPS.set(chaintips)

        mempool = lbcd('getmempoolinfo')
        LBCD_MEMPOOL_BYTES.set(mempool['bytes'])
        LBCD_MEMPOOL_SIZE.set(mempool['size'])

        nettotals = lbcd('getnettotals')
        LBCD_TOTAL_BYTES_RECV.set(nettotals['totalbytesrecv'])
        LBCD_TOTAL_BYTES_SENT.set(nettotals['totalbytessent'])

        latest_block = get_block(str(info['blocks']))
        if latest_block:
            LBCD_LATEST_BLOCK_SIZE.set(latest_block['size'])
            LBCD_LATEST_BLOCK_TXS.set(len(latest_block['tx']))
            inputs, outputs = 0, 0
            # counting transaction inputs and outputs requires txindex=1
            # to be enabled, which may also necessitate reindex=1 in lbcd.conf
            for tx in latest_block['tx']:
                rawtx = get_raw_tx(tx)
                if not rawtx:
                    continue
                inputs += len(rawtx['vin'])
                outputs += len(rawtx['vout'])

            LBCD_LATEST_BLOCK_INPUTS.set(inputs)
            LBCD_LATEST_BLOCK_OUTPUTS.set(outputs)

        time.sleep(60)

if __name__ == '__main__':
    main()
