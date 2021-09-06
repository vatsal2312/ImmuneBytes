import getopt
import sys

import eth_abi

from src.rci_competition_utilities.utilities.Competition import Competition
from src.rci_competition_utilities.utilities.Token import Token
from src.rci_competition_utilities.utilities.Vault import Vault
from src.rci_competition_utilities.utilities.Registry import Registry
from src.rci_competition_utilities.organizer import Organizer
from src.rci_competition_utilities.utilities.rci_utilities import *
import web3, json, random, string, subprocess,time
from hashlib import sha256
from web3 import exceptions as w3exceptions
import pandas as pd

TOTAL_SUPPLY = int((1e8)) * int((1e18))

random.seed(55)

class Human(Organizer):
    def __init__(self, address, token_address=None, vault_address=None, comp_address=None, registry_address=None):
        self.address = address
        self.privateKey = keys['private_keys'][address.lower()]
        Organizer.this_account = w3.eth.account.from_key(self.privateKey)
        assert Organizer.this_account.address == address, 'Private key does not match account {}.'.format(
            address)
        Organizer.my_gas_price_in_wei = 1 * int(1e9)
        Organizer.w3 = w3
        Organizer.verbose = False

        if token_address and vault_address and comp_address:
            super(Human,self).token_init(token_address)
            super(Human,self).vault_init(vault_address)
            super(Human,self).registry_init(registry_address)
            super(Human,self).competition_init(comp_address)

def should_fail(fn, args_list=[]):
    try:
        fn(*args_list)
        assert False, '{} should fail but did not!'.format(fn.__name__)
    except w3exceptions.ContractLogicError as e:
        pass

def getRandomString(n=128):
    return ''.join(random.choice(string.ascii_letters) for i in range(n))

def getRandomSelection(array, min_num = 1):
    return random.sample(array, random.randint(min_num, len(array)))

def getRandomAmount(human):
    balance = human.token.balanceOf(human.address)
    if balance > int(8.5e18):
        return random.randint(int(8.5e18), balance)
    else:
        if balance > 10:
            return balance//3
        else:
            return 1

def getHash():
    content = getRandomString()
    return sha256(content.encode('utf-8')).hexdigest()

def staking_should_fail(p, admin):
    should_fail(p.competition.increaseStake,[1])
    should_fail(p.competition.decreaseStake, [1])
    should_fail(p.competition.setStake, [1])

def unauthorized_actions_should_fail(p, admin):
    should_fail(p.competition.revokeRole, [b'0x0', admin.address])
    should_fail(p.competition.grantRole, [b'0x0', p.address])
    should_fail(p.competition.renounceRole, [b'0x0', admin.address])
    should_fail(p.competition.updateRewardsThreshold, [1])
    should_fail(p.competition.updateVaultAddress, [admin.address])
    should_fail(p.competition.updateStakeThreshold, [1])
    should_fail(p.competition.updateChallengeRewardsPercentageInWei, [1])
    should_fail(p.competition.updateTournamentRewardsPercentageInWei, [1])
    should_fail(p.competition.openChallenge, [getHash(), getHash()])
    challenge_number = p.competition.getLatestChallengeNumber()
    should_fail(p.competition.updateDataset, [p.competition.getDatasetHash(challenge_number), getHash()])
    should_fail(p.competition.updateKey, [p.competition.getKeyHash(challenge_number), getHash()])
    should_fail(p.competition.closeSubmission)
    should_fail(p.competition.submitResults, [getHash()])
    should_fail(p.competition.updateResults, [p.competition.getResultsHash(challenge_number), getHash()])
    should_fail(p.competition.payStakingRewards, [[p.address], [1]])
    should_fail(p.competition.payChallengeAndTournamentRewards, [[p.address], [1], [1]])
    should_fail(p.competition.updateInformationBatch, [challenge_number, [p.address], 1, [1]])
    # should_fail(p.competition.updateInformationSingle, [challenge_number, p.address, 1, 1])
    should_fail(p.competition.advanceToPhase, [p.competition.getPhase(challenge_number) + 1])

def setup(ip='0.0.0.0', port='8023', http=True):
    if http:
        return web3.Web3(web3.Web3.HTTPProvider("http://" + ip + ":" + port))
    return web3.Web3(web3.Web3.WebsocketProvider("ws://" + ip + ":" + port))

def progress_bar(work_done, prefix=''):
    print("\r"+prefix+"Progress: [{0:50s}] {1:.1f}%".format('#' * int(work_done * 50), work_done * 100), end="", flush=True)
    if work_done == 1:
        print()

def dec(value):
    chunk = 32
    length = value[32:64].hex()
    length = int(length,16)
    s = ''
    remaining = length
    for i in range(64, len(value), chunk):
        try:
            if remaining >= chunk:
                s += value[i:i+chunk].decode()
                remaining -= chunk
            else:
                s += value[i:i + remaining].decode()
                remaining = 0
        except:
            continue
    return s

if __name__ == '__main__':
    argv = sys.argv[1:]
    num_participants = 0
    num_rounds = 0
    try:
        opts, args = getopt.getopt(argv, "hp:r:", ["num_participants=", "num_rounds="])
    except getopt.GetoptError:
        print
        'full_cycle.py -p <num_participants> -r <num_rounds>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print
            'full_cycle.py -p <num_participants> -r <num_rounds>'
            sys.exit()
        elif opt in ("-p", "--num_participants"):
            num_participants = int(arg)
        elif opt in ("-r", "--num_rounds"):
            num_rounds = int(arg)

    if num_participants==0 or num_rounds ==0:
        while True:
            try:
                num_participants = 10# int(input('Please enter desired number of participants.'))
                num_rounds = 3#int(input('Please enter the desired number of challenge rounds.'))
                break
            except:
                continue

    start = time.time()
    num_accounts = num_participants + 10
    port = random.randint(7000, 8051)
    print('Setting up Ganache with {} accounts...'.format(num_accounts))
    cmd = 'ganache-cli -a {} -e 100000 -p {} -h 0.0.0.0 -g 1000000000000 -d -m "mnemonic" --account_keys_path keys.json'.format(num_accounts, port)
    # cmd += ' --verbose'
    # cmd += ' -b 1'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL)
    with open('keys.json', 'r') as f:
        keys = json.load(f)
    w3 = setup(ip='0.0.0.0', port='{}'.format(port), http=True)
    while True:
        try:
            time.sleep(3)
            accounts = w3.geth.personal.list_accounts()
            break
        except:
            continue
    print('Time taken for setup: {:.2f}s'.format(time.time()-start))

    admin = Human(accounts[0])
    stake_threshold = 10
    challenge_rewards_threshold = 20

    # deploy
    admin.registry_deploy()
    admin.token_deploy('Rome', 'ROME')
    admin.vault_deploy()
    admin.competition_deploy(stake_threshold, challenge_rewards_threshold, admin.token.address(), admin.vault.address())

    admin.vault.authorizeCompetition(admin.competition.address(), 0)
    admin.registry.registerNewCompetition('Euro2020',admin.competition.address(), admin.vault.address(), getHash())
    admin.registry.changeTokenAddress(admin.token.address())
    print(admin.registry.getTokenAddress())

    investors = Human(accounts[1], admin.token.address(), admin.vault.address(), admin.competition.address(), admin.registry.address())

    team = Human(accounts[2], admin.token.address(), admin.vault.address(), admin.competition.address(), registry_address=admin.registry.address())

    reserve = Human(accounts[3], admin.token.address(), admin.vault.address(), admin.competition.address(), registry_address=admin.registry.address())

    participants = []

    print(len(accounts))

    for i in range(4, 4 + num_participants):
        p = Human(accounts[i], admin.token.address(), admin.vault.address(), admin.competition.address(), admin.registry.address())
        participants.append(p)
        progress_bar((i-3)/num_participants, prefix='Initializing Participants In ')

    admin.token.transfer(investors.address, 25 * TOTAL_SUPPLY // 100)
    admin.token.transfer(team.address, 10 * TOTAL_SUPPLY // 100)
    admin.token.transfer(reserve.address, 10 * TOTAL_SUPPLY // 100)

    # airdrop

    for i in range(0, num_participants):
        tx = admin.token.transfer(participants[i].address, 20 * TOTAL_SUPPLY // 100 // num_participants)
        progress_bar(i/(num_participants-1), prefix='Airdropping In ')

    admin.token.grantPermission(admin.competition.address())

    user1 = participants[0]
    user2 = participants[1]

    admin.token.transfer(user1.address, int(1000e18))
    admin.token.transfer(user2.address, int(1000e18))

    user1.token.grantPermission(admin.competition.address())
    user2.token.grantPermission(admin.competition.address())

    user1.competition.setStake(int(50e18))
    user2.competition.setStake(int(77e18))

    cn = user1.competition.getLatestChallengeNumber()
    print('cn', cn)
    print(user1.competition.getPhase(cn))

    for i in range(1, 12):
        admin.competition.sponsor(int(200e18))
        dataset = getHash()
        key = getHash()

        admin.competition.openChallenge(dataset, key)
        admin.competition.updateMessage("{}00 degrees that's why they call me mr farenheit.".format(i))
        pool = admin.conversion_to_float(admin.competition.getCompetitionPool())

        print('Dataset: {} | Key: {} | Pool {}'.format(dataset, key, pool))

        data = []
        address = []

        d = admin.token.contract.encodeABI(fn_name="getPermission", args=[admin.competition.address()])
        data.append(d)
        address.append(admin.token.address())
        d = user1.token.contract.encodeABI(fn_name="getPermission", args=[admin.competition.address()])
        data.append(d)
        address.append(user1.token.address())
        d = user2.registry.contract.encodeABI(fn_name="getCompetitionAddress", args=["Euro2020"])
        data.append(d)
        address.append(admin.registry.address())
        d = admin.competition.contract.encodeABI(fn_name="getPhase", args=[i])
        data.append(d)
        address.append(admin.competition.address())
        d = admin.competition.contract.encodeABI(fn_name="getLatestChallengeNumber", args=[])
        data.append(d)
        address.append(admin.competition.address())
        d = admin.competition.contract.encodeABI(fn_name="getMessage", args=[])
        data.append(d)
        address.append(admin.competition.address())
        d = admin.competition.contract.encodeABI(fn_name="getCompetitionPool", args=[])
        data.append(d)
        address.append(admin.competition.address())
        d = admin.competition.contract.encodeABI(fn_name="getDatasetHash", args=[i])
        data.append(d)
        address.append(admin.competition.address())
        d = admin.competition.contract.encodeABI(fn_name="getKeyHash", args=[i])
        data.append(d)
        address.append(admin.competition.address())
        d = admin.competition.contract.encodeABI(fn_name="getStake", args=[user1.address])
        data.append(d)
        address.append(admin.competition.address())
        d = admin.competition.contract.encodeABI(fn_name="getStake", args=[user2.address])
        data.append(d)
        address.append(admin.competition.address())

        print('RESULTS - must be handled seprately for each return type')
        res = user1.registry.batchCall(address, data)
        res[0] = int(res[0].hex(), 16)
        res[1] = int(res[1].hex(), 16)
        res[2] = '0x' + res[2].hex()[-40:]
        assert res[2] == admin.competition.address().lower(), "Competition address in registry incorrect."
        res[3] = int(res[3].hex(), 16)
        res[4] = int(res[4].hex(), 16)
        res[5] = dec(res[5])
        res[6] = admin.conversion_to_float(int(res[6].hex(), 16))
        res[7] = res[7].hex()
        res[8] = res[8].hex()
        res[9] = admin.conversion_to_float(int(res[9].hex(),16))
        res[10] = admin.conversion_to_float(int(res[10].hex(),16))

        for r in res:
            print(r)

        admin.competition.closeSubmission()
        admin.competition.advanceToPhase(3)
        admin.competition.advanceToPhase(4)

