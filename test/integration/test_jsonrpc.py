import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from chaincoind import ChaincoinDaemon
from chaincoin_config import ChaincoinConfig


def test_chaincoind():
    config_text = ChaincoinConfig.slurp_config_file(config.chaincoin_conf)
    network = 'mainnet'
    chain = 'main'
    is_testnet = False
    genesis_hash = u'00000f639db5734b2b861ef8dbccc33aebd7de44d13de000a12d093bcc866c64'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            chain = 'test'
            is_testnet = True
            genesis_hash = u'0000082f5939c2154dbcba35f784530d12e9d72472fcfaf29674ea312cdf4c83'

    creds = ChaincoinConfig.get_rpc_creds(config_text, network)
    chaincoind = ChaincoinDaemon(**creds)
    assert chaincoind.rpc_command is not None

    assert hasattr(chaincoind, 'rpc_connection')

    # Chaincoin testnet block 0 hash == 0000082f5939c2154dbcba35f784530d12e9d72472fcfaf29674ea312cdf4c83
    # test commands without arguments
    info = chaincoind.rpc_command('getblockchaininfo')
    info_keys = [
        'chain',
        'blocks',
        'headers',
        'bestblockhash',
        'difficulty',
        'mediantime',
        'verificationprogress',
        'initialblockdownload',
        'chainwork',
        'size_on_disk',
        'pruned',
        'softforks'
    ]
    for key in info_keys:
        assert key in info
    assert info['chain'] == chain

    # test commands with args
    assert chaincoind.rpc_command('getblockhash', 0) == genesis_hash
