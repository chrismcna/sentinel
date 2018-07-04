# -*- coding: utf-8 -*-
import pytest
import sys
import os
import time
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../test_sentinel.conf'))
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../../lib')))
import misc
import config
from models import GovernanceObject, Proposal, Vote


# clear DB tables before each execution
def setup():
    # clear tables first
    Vote.delete().execute()
    Proposal.delete().execute()
    GovernanceObject.delete().execute()


def teardown():
    pass


# list of proposal govobjs to import for testing
@pytest.fixture
def go_list_proposals():
    items = [
        {u'AbsoluteYesCount': 1000,
         u'AbstainCount': 7,
         u'CollateralHash': u'744bb5190b9416a755517e727fbc2605ce5537c3f6e132195f09bac4bd2d691f',
         u'DataHex': u'5b5b2270726f706f73616c222c7b22656e645f65706f6368223a313531313936353931362c226e616d65223a2267756e732d6e2d726f736573222c227061796d656e745f61646472657373223a225a484a56376a684257676142317578617a6256736e5155354855444171583134427a222c227061796d656e745f616d6f756e74223a3331352e37352c2273746172745f65706f6368223a313531313936323335312c2274797065223a312c2275726c223a22687474703a2f2f636861696e636f696e2e6f72672f70726f706f73616c2f3635343332227d5d5d',
         u'DataString': u'[["proposal", {"end_epoch": 2122520400, "name": "guns-n-roses", "payment_address": "ZHJV7jhBWgaB1uxazbVsnQU5HUDAqX14Bz", "payment_amount": 315.75, "start_epoch": 1511962351, "type": 1, "url": "http://chaincoin.org/proposal/65432"}]]',
         u'Hash': u'7fa2798fee8ea74c3a369db72ae872096bd4e4714f1f5027c730ccfbf58aac02',
         u'IsValidReason': u'',
         u'NoCount': 25,
         u'YesCount': 1025,
         u'fBlockchainValidity': True,
         u'fCachedDelete': False,
         u'fCachedEndorsed': False,
         u'fCachedFunding': False,
         u'fCachedValid': True},
        {u'AbsoluteYesCount': 1000,
         u'AbstainCount': 29,
         u'CollateralHash': u'3170ed7b3a0ede65fb9ffb3068d299d6bb786a5a6527351692a44aba1f3e67b7',
         u'DataHex': u'5b5b2270726f706f73616c222c7b22656e645f65706f6368223a313531313936383432332c226e616d65223a227069737461636368696f2d37363235222c227061796d656e745f61646472657373223a225a483662743935736b4756636f3274336752754867676353557274525a3542557372222c227061796d656e745f616d6f756e74223a32312e39352c2273746172745f65706f6368223a313531313936343835382c2274797065223a312c2275726c223a22687474703a2f2f636861696e636f696e2e6f72672f70726f706f73616c2f3636343333227d5d5d',
         u'DataString': u'[["proposal", {"end_epoch": 2122520400, "name": "pistacchio-7625", "payment_address": "ZH6bt95skGVco2t3gRuHggcSUrtRZ5BUsr", "payment_amount": 21.95, "start_epoch": 1474261086, "type": 1, "url": "http://chaincoin.org/proposal/66433"}]]',
         u'Hash': u'd1ce73527d7cd6f2218f8ca893990bc7d5c6b9334791ce7973bfa22f155f826e',
         u'IsValidReason': u'',
         u'NoCount': 56,
         u'YesCount': 1056,
         u'fBlockchainValidity': True,
         u'fCachedDelete': False,
         u'fCachedEndorsed': False,
         u'fCachedFunding': False,
         u'fCachedValid': True},
    ]

    return items


# Proposal
@pytest.fixture
def proposal():
    # NOTE: no governance_object_id is set
    pobj = Proposal(
        start_epoch=1483250400,  # 2017-01-01
        end_epoch=2122520400,
        name="wine-n-cheeze-party",
        url="https://chaincoin.org/wine-n-cheeze-party",
        payment_address="ZHJV7jhBWgaB1uxazbVsnQU5HUDAqX14Bz",
        payment_amount=13
    )

    # NOTE: this object is (intentionally) not saved yet.
    #       We want to return an built, but unsaved, object
    return pobj



def test_proposal_is_expired(proposal):
    cycle = 24  # testnet
    now = misc.now()

    proposal.start_epoch = now - (86400 * 2)  # two days ago
    proposal.end_epoch = now - (60 * 60)  # expired one hour ago
    assert proposal.is_expired(superblockcycle=cycle) is False

    # fudge factor + a 24-block cycle == an expiry window of 8280, so...
    proposal.end_epoch = now - 8279
    assert proposal.is_expired(superblockcycle=cycle) is False

    proposal.end_epoch = now - 8281
    assert proposal.is_expired(superblockcycle=cycle) is True


# deterministic ordering
def test_approved_and_ranked(go_list_proposals):
    from chaincoind import ChaincoinDaemon
    chaincoind = ChaincoinDaemon.from_chaincoin_conf(config.chaincoin_conf)

    for item in go_list_proposals:
        (go, subobj) = GovernanceObject.import_gobject_from_chaincoind(chaincoind, item)

    prop_list = Proposal.approved_and_ranked(chaincoind,proposal_quorum=1, next_superblock_max_budget=384)

    assert prop_list[0].object_hash == u'd1ce73527d7cd6f2218f8ca893990bc7d5c6b9334791ce7973bfa22f155f826e'
    assert prop_list[1].object_hash == u'7fa2798fee8ea74c3a369db72ae872096bd4e4714f1f5027c730ccfbf58aac02'

