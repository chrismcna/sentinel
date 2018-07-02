import pytest
import sys
import os
import time
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../test_sentinel.conf'))
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../../lib')))
import misc
import config
from models import GovernanceObject, Proposal, Superblock, Vote


# clear DB tables before each execution
def setup():
    # clear tables first...
    Vote.delete().execute()
    Proposal.delete().execute()
    Superblock.delete().execute()
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


# list of superblock govobjs to import for testing
@pytest.fixture
def go_list_superblocks():
    items = [
        {u'AbsoluteYesCount': 1,
         u'AbstainCount': 0,
         u'CollateralHash': u'0000000000000000000000000000000000000000000000000000000000000000',
         u'DataHex': u'5b5b2274726967676572222c207b226576656e745f626c6f636b5f686569676874223a2037323639362c20227061796d656e745f616464726573736573223a2022795965384b77796155753559737753596d42337133727978385854557539793755697c795965384b77796155753559737753596d4233713372797838585455753979375569222c20227061796d656e745f616d6f756e7473223a202232352e37353030303030307c32352e3735303030303030222c202274797065223a20327d5d5d',
         u'DataString': u'[["trigger", {"event_block_height": 72696, "payment_addresses": "yYe8KwyaUu5YswSYmB3q3ryx8XTUu9y7Ui|yYe8KwyaUu5YswSYmB3q3ryx8XTUu9y7Ui", "payment_amounts": "25.75000000|25.7575000000", "type": 2}]]',
         u'Hash': u'667c4a53eb81ba14d02860fdb4779e830eb8e98306f9145f3789d347cbeb0721',
         u'IsValidReason': u'',
         u'NoCount': 0,
         u'YesCount': 1,
         u'fBlockchainValidity': True,
         u'fCachedDelete': False,
         u'fCachedEndorsed': False,
         u'fCachedFunding': False,
         u'fCachedValid': True},
        {u'AbsoluteYesCount': 1,
         u'AbstainCount': 0,
         u'CollateralHash': u'0000000000000000000000000000000000000000000000000000000000000000',
         u'DataHex': u'5b5b2274726967676572222c207b226576656e745f626c6f636b5f686569676874223a2037323639362c20227061796d656e745f616464726573736573223a2022795965384b77796155753559737753596d42337133727978385854557539793755697c795965384b77796155753559737753596d4233713372797838585455753979375569222c20227061796d656e745f616d6f756e7473223a202232352e37353030303030307c32352e3735303030303030222c202274797065223a20327d5d5d',
         u'DataString': u'[["trigger", {"event_block_height": 72696, "payment_addresses": "yYe8KwyaUu5YswSYmB3q3ryx8XTUu9y7Ui|yYe8KwyaUu5YswSYmB3q3ryx8XTUu9y7Ui", "payment_amounts": "25.75000000|25.75000000", "type": 2}]]',
         u'Hash': u'8f91ffb105739ec7d5b6c0b12000210fcfcc0837d3bb8ca6333ba93ab5fc0bdf',
         u'IsValidReason': u'',
         u'NoCount': 0,
         u'YesCount': 1,
         u'fBlockchainValidity': True,
         u'fCachedDelete': False,
         u'fCachedEndorsed': False,
         u'fCachedFunding': False,
         u'fCachedValid': True},
        {u'AbsoluteYesCount': 1,
         u'AbstainCount': 0,
         u'CollateralHash': u'0000000000000000000000000000000000000000000000000000000000000000',
         u'DataHex': u'5b5b2274726967676572222c207b226576656e745f626c6f636b5f686569676874223a2037323639362c20227061796d656e745f616464726573736573223a2022795965384b77796155753559737753596d42337133727978385854557539793755697c795965384b77796155753559737753596d4233713372797838585455753979375569222c20227061796d656e745f616d6f756e7473223a202232352e37353030303030307c32352e3735303030303030222c202274797065223a20327d5d5d',
         u'DataString': u'[["trigger", {"event_block_height": 72696, "payment_addresses": "yYe8KwyaUu5YswSYmB3q3ryx8XTUu9y7Ui|yYe8KwyaUu5YswSYmB3q3ryx8XTUu9y7Ui", "payment_amounts": "25.75000000|25.75000000", "type": 2}]]',
         u'Hash': u'bc2834f357da7504138566727c838e6ada74d079e63b6104701f4f8eb05dae36',
         u'IsValidReason': u'',
         u'NoCount': 0,
         u'YesCount': 1,
         u'fBlockchainValidity': True,
         u'fCachedDelete': False,
         u'fCachedEndorsed': False,
         u'fCachedFunding': False,
         u'fCachedValid': True},
    ]

    return items


@pytest.fixture
def superblock():
    sb = Superblock(
        event_block_height=62500,
        payment_addresses='ZHJV7jhBWgaB1uxazbVsnQU5HUDAqX14Bz|ZH6bt95skGVco2t3gRuHggcSUrtRZ5BUsr',
        payment_amounts='5|3',
        proposal_hashes='7fa2798fee8ea74c3a369db72ae872096bd4e4714f1f5027c730ccfbf58aac02|d1ce73527d7cd6f2218f8ca893990bc7d5c6b9334791ce7973bfa22f155f826e',
    )
    return sb


def test_superblock_is_valid(superblock):
    from chaincoind import ChaincoinDaemon
    chaincoind = ChaincoinDaemon.from_chaincoin_conf(config.chaincoin_conf)

    orig = Superblock(**superblock.get_dict())  # make a copy

    # original as-is should be valid
    assert orig.is_valid(chaincoind) is True

    # mess with payment amounts
    superblock.payment_amounts = '7|yyzx'
    assert superblock.is_valid(chaincoind) is False

    superblock.payment_amounts = '7,|yzx'
    assert superblock.is_valid(chaincoind) is False

    superblock.payment_amounts = '7|8'
    assert superblock.is_valid(chaincoind) is True

    superblock.payment_amounts = ' 7|8'
    assert superblock.is_valid(chaincoind) is False

    superblock.payment_amounts = '7|8 '
    assert superblock.is_valid(chaincoind) is False

    superblock.payment_amounts = ' 7|8 '
    assert superblock.is_valid(chaincoind) is False

    # reset
    superblock = Superblock(**orig.get_dict())
    assert superblock.is_valid(chaincoind) is True

    # mess with payment addresses
    superblock.payment_addresses = 'ZHJV7jhBWgaB1uxazbVsnQU5HUDAqX14Bz|1234 Anywhere ST, Chicago, USA'
    assert superblock.is_valid(chaincoind) is False

    # leading spaces in payment addresses
    superblock.payment_addresses = ' yTC62huR4YQEPn9AJHjnQxxreHSbgAoatV'
    superblock.payment_amounts = '5.00'
    assert superblock.is_valid(chaincoind) is False

    # trailing spaces in payment addresses
    superblock.payment_addresses = 'yTC62huR4YQEPn9AJHjnQxxreHSbgAoatV '
    superblock.payment_amounts = '5.00'
    assert superblock.is_valid(chaincoind) is False

    # leading & trailing spaces in payment addresses
    superblock.payment_addresses = ' yTC62huR4YQEPn9AJHjnQxxreHSbgAoatV '
    superblock.payment_amounts = '5.00'
    assert superblock.is_valid(chaincoind) is False

    # single payment addr/amt is ok
    superblock.payment_addresses = 'ZHJV7jhBWgaB1uxazbVsnQU5HUDAqX14Bz'
    superblock.payment_amounts = '5.00'
    assert superblock.is_valid(chaincoind) is True

    # ensure number of payment addresses matches number of payments
    superblock.payment_addresses = 'ZHJV7jhBWgaB1uxazbVsnQU5HUDAqX14Bz'
    superblock.payment_amounts = '37.00|23.24'
    assert superblock.is_valid(chaincoind) is False

    superblock.payment_addresses = 'ZHJV7jhBWgaB1uxazbVsnQU5HUDAqX14Bz|ZH6bt95skGVco2t3gRuHggcSUrtRZ5BUsr'
    superblock.payment_amounts = '37.00'
    assert superblock.is_valid(chaincoind) is False

    # ensure amounts greater than zero
    superblock.payment_addresses = 'ZHJV7jhBWgaB1uxazbVsnQU5HUDAqX14Bz'
    superblock.payment_amounts = '-37.00'
    assert superblock.is_valid(chaincoind) is False

    # reset
    superblock = Superblock(**orig.get_dict())
    assert superblock.is_valid(chaincoind) is True

    # mess with proposal hashes
    superblock.proposal_hashes = '7|yyzx'
    assert superblock.is_valid(chaincoind) is False

    superblock.proposal_hashes = '7,|yyzx'
    assert superblock.is_valid(chaincoind) is False

    superblock.proposal_hashes = '0|1'
    assert superblock.is_valid(chaincoind) is False

    superblock.proposal_hashes = '0000000000000000000000000000000000000000000000000000000000000000|1111111111111111111111111111111111111111111111111111111111111111'
    assert superblock.is_valid(chaincoind) is True

    # reset
    superblock = Superblock(**orig.get_dict())
    assert superblock.is_valid(chaincoind) is True


def test_serialisable_fields():
    s1 = ['event_block_height', 'payment_addresses', 'payment_amounts', 'proposal_hashes']
    s2 = Superblock.serialisable_fields()

    s1.sort()
    s2.sort()

    assert s2 == s1


def test_deterministic_superblock_creation(go_list_proposals):
    import chaincoinlib
    import misc
    from chaincoind import ChaincoinDaemon
    chaincoind = ChaincoinDaemon.from_chaincoin_conf(config.chaincoin_conf)
    for item in go_list_proposals:
        (go, subobj) = GovernanceObject.import_gobject_from_chaincoind(chaincoind, item)

    max_budget = 384
    prop_list = Proposal.approved_and_ranked(chaincoind, proposal_quorum=1, next_superblock_max_budget=max_budget)

    # MAX_GOVERNANCE_OBJECT_DATA_SIZE defined in governance-object.h
    maxgovobjdatasize = 16 * 1024
    sb = chaincoinlib.create_superblock(prop_list, 72000, max_budget, misc.now(), maxgovobjdatasize)

    assert sb.event_block_height == 72000
    assert sb.payment_addresses == 'ZHJV7jhBWgaB1uxazbVsnQU5HUDAqX14Bz|ZH6bt95skGVco2t3gRuHggcSUrtRZ5BUsr'
    assert sb.payment_amounts == '315.75000000|21.05000000'
    assert sb.proposal_hashes == '7fa2798fee8ea74c3a369db72ae872096bd4e4714f1f5027c730ccfbf58aac02|d1ce73527d7cd6f2218f8ca893990bc7d5c6b9334791ce7973bfa22f155f826e'

    assert sb.hex_hash() == 'bb3f33ccf95415c396bd09d35325dbcbc7b067010d51c7ccf772a9e839c1e414'


def test_superblock_size_limit(go_list_proposals):
    import chaincoinlib
    import misc
    from chaincoind import ChaincoinDaemon
    chaincoind = ChaincoinDaemon.from_chaincoin_conf(config.chaincoin_conf)
    for item in go_list_proposals:
        (go, subobj) = GovernanceObject.import_gobject_from_chaincoind(chaincoind, item)

    max_budget = 60
    prop_list = Proposal.approved_and_ranked(chaincoind, proposal_quorum=1, next_superblock_max_budget=max_budget)

    # mock maxgovobjdatasize by setting equal to the size of a trigger
    # (serialized) if only the first proposal had been included... anything
    # larger should break the limit
    single_proposal_sb = Superblock(
        event_block_height=72000,
        payment_addresses=prop_list[0].payment_address,
        payment_amounts="{0:.8f}".format(prop_list[0].payment_amount),
        proposal_hashes=prop_list[0].object_hash,
    )
    maxgovobjdatasize = len(single_proposal_sb.serialise())

    # now try and create a Superblock with the entire proposal list
    sb = chaincoinlib.create_superblock(prop_list, 72000, max_budget, misc.now(), maxgovobjdatasize)

    # two proposals in the list, but...
    assert len(prop_list) == 2

    # only one should have been included in the SB, because the 2nd one is over the size limit
    assert sb.event_block_height == 72000
    assert sb.payment_addresses == 'ZHJV7jhBWgaB1uxazbVsnQU5HUDAqX14Bz|ZH6bt95skGVco2t3gRuHggcSUrtRZ5BUsr'
    assert sb.payment_amounts == '315.75000000|21.05000000'
    assert sb.proposal_hashes == '7fa2798fee8ea74c3a369db72ae872096bd4e4714f1f5027c730ccfbf58aac02|d1ce73527d7cd6f2218f8ca893990bc7d5c6b9334791ce7973bfa22f155f826e'

    assert sb.hex_hash() == 'bb3f33ccf95415c396bd09d35325dbcbc7b067010d51c7ccf772a9e839c1e414'


def test_deterministic_superblock_selection(go_list_superblocks):
    from chaincoind import ChaincoinDaemon
    chaincoind = ChaincoinDaemon.from_chaincoin_conf(config.chaincoin_conf)

    for item in go_list_superblocks:
        (go, subobj) = GovernanceObject.import_gobject_from_chaincoind(chaincoind, item)

    # highest hash wins if same -- so just order by hash
    sb = Superblock.find_highest_deterministic('542f4433e438bdd64697b8381fda1a7a9b7a111c3a4e32fad524d1821d820394')
    assert sb.object_hash == 'bc2834f357da7504138566727c838e6ada74d079e63b6104701f4f8eb05dae36'
