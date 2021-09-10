from src.rci_competition_utilities.organizer import Organizer
from src.rci_competition_utilities.utilities.rci_utilities import *
import web3, json, random, string, subprocess,time, getopt, sys, traceback
from hashlib import sha256
from web3 import exceptions as w3exceptions
from decimal import Decimal
import pandas as pd

TOTAL_SUPPLY = int((1e8)) * int((1e18))

random.seed(55)

class Human(Organizer):
    def __init__(self, address, token_address=None, comp_address=None, registry_address=None):
        self.address = address
        self.privateKey = keys['private_keys'][address.lower()]
        self.this_account = w3.eth.account.from_key(self.privateKey)
        assert self.this_account.address == address, 'Private key does not match account {}.'.format(
            address)
        self.my_gas_price_in_wei = 1 * int(1e9)
        self.w3 = w3
        self.verbose = False

        if token_address and comp_address:
            self.token_init(token_address)
            self.registry_init(registry_address)
            self.competition_init(comp_address)

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
    should_fail(p.competition.increaseStake,[p.address, 1])
    should_fail(p.competition.decreaseStake, [p.address, 1])
    should_fail(p.token.increaseStake,[p.competition.address(), 1])
    should_fail(p.token.decreaseStake, [p.competition.address(), 1])
    should_fail(p.token.setStake, [p.competition.address(), 1])


def unauthorized_actions_should_fail(p, admin):
    child_admin_hash = p.competition.RCI_CHILD_ADMIN().hex()
    should_fail(p.competition.revokeRole, [child_admin_hash, admin.address])
    should_fail(p.competition.grantRole, [child_admin_hash, p.address])
    should_fail(p.competition.renounceRole, [child_admin_hash, admin.address])
    should_fail(p.competition.updateRewardsThreshold, [1])
    should_fail(p.competition.updateStakeThreshold, [1])
    should_fail(p.competition.updateChallengeRewardsPercentageInWei, [1])
    should_fail(p.competition.updateTournamentRewardsPercentageInWei, [1])
    should_fail(p.competition.openChallenge, [getHash(), getHash(), getTimestamp(), getTimestamp()])
    challenge_number = p.competition.getLatestChallengeNumber()
    should_fail(p.competition.updateDataset, [p.competition.getDatasetHash(challenge_number), getHash()])
    should_fail(p.competition.updateKey, [p.competition.getKeyHash(challenge_number), getHash()])
    should_fail(p.competition.closeSubmission)
    should_fail(p.competition.submitResults, [getHash()])
    should_fail(p.competition.updateResults, [p.competition.getResultsHash(challenge_number), getHash()])
    should_fail(p.competition.payStakingRewards, [[p.address], [1]])
    should_fail(p.competition.payRewards, [[p.address], [1], [1], [1]])
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

def getTimestamp():
    now = int(time.time() * 1000)
    return now + random.randint(86400000, 864000000)

if __name__ == '__main__':
    try:
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
                    num_participants = 20#int(input('Please enter desired number of participants.'))
                    num_rounds = 3 #int(input('Please enter the desired number of challenge rounds.'))
                    break
                except:
                    continue

        start = time.time()
        num_accounts = num_participants + 20
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

        stake_threshold = 10 * int(1e18)
        challenge_rewards_threshold = 10 * int(1e18)

        # deploy
        admin.registry_deploy()
        admin.token_deploy('Rome', 'ROME')
        admin.proxy_admin_deploy()
        admin.competition_deploy()

        owners = [admin]
        owners_addresses = [admin.address]
        for i in range(1,10):
            o = Human(accounts[i])
            o.registry_init(admin.registry.address())
            o.token_init(admin.token.address())
            o.proxy_admin_init(admin.proxy_admin.address())
            o.competition_init(admin.competition.address())
            owners.append(o)
            owners_addresses.append(o.address)

        admin.multisig_deploy(owners_addresses, required=6)

        for o in owners:
            o.multisig_init(admin.multisig.address())

        data = admin.competition.contract.encodeABI(fn_name='initialize',
                                                    args=[stake_threshold, challenge_rewards_threshold,
                                                          admin.token.address()])
        impl_address = admin.competition.address()
        admin.proxy_upgradeable_deploy(impl_addr=admin.competition.address(), admin_addr=admin.proxy_admin.address(),
                                       data=data)
        before_addr = admin.competition.address()
        print('before', admin.competition.address())
        admin.competition_init(admin.proxy_upgradeable.address())
        print('after', admin.competition.address())
        assert before_addr != admin.competition.address(), "Competition proxy address not set properly!"

        admin.token.authorizeCompetition(admin.competition.address())

        # admin.competition.initialize(stake_threshold, challenge_rewards_threshold, admin.token.address(), admin.vault.address())

        # should_fail(admin.competition.initialize, [stake_threshold, challenge_rewards_threshold, admin.token.address(), admin.vault.address()])

        # admin.vault.authorizeCompetition(admin.competition.address(), 0)
        admin.registry.registerNewCompetition('Euro2020',admin.competition.address(), rulesLocation=getHash())

        investors = Human(accounts[11], admin.token.address(), admin.competition.address(), admin.registry.address())

        team = Human(accounts[12], admin.token.address(), admin.competition.address(), registry_address=admin.registry.address())

        reserve = Human(accounts[13], admin.token.address(), admin.competition.address(), registry_address=admin.registry.address())

        participants = []

        for i in range(17, 17 + num_participants):
            p = Human(accounts[i], admin.token.address(), admin.competition.address(), admin.registry.address())
            participants.append(p)
            progress_bar((i-3)/num_participants, prefix='Initializing Participants In ')

        admin.token.transfer(investors.address, 25 * TOTAL_SUPPLY // 100)
        admin.token.transfer(team.address, 10 * TOTAL_SUPPLY // 100)
        admin.token.transfer(reserve.address, 10 * TOTAL_SUPPLY // 100)

        # airdrop

        for i in range(0, num_participants):
            tx = admin.token.transfer(participants[i].address, 20 * TOTAL_SUPPLY // 100 // num_participants)
            progress_bar(i/(num_participants-1), prefix='Airdropping In ')

        admin.token.increaseAllowance(admin.competition.address(), int(100000 * 1e18))
        # print(admin.token.allowance(admin.address, admin.competition.address()))

        for challenge_round in range(num_rounds):
            progress_bar(challenge_round / (num_rounds - 1), "Competition In ")

            # Sponsor Challenge Round
            # tx = admin.competition.sponsor(100*int(1e18))

            should_fail(admin.competition.openChallenge, [getHash(), getHash(), getTimestamp(), getTimestamp()])

            leftover = admin.competition.getCompetitionPool()

            tx = admin.competition.sponsor(int(1.1 * challenge_rewards_threshold))

            # staking_should_fail(participants[0], admin)
            unauthorized_actions_should_fail(participants[0], admin)
            should_fail(participants[0].competition.submitNewPredictions, [getHash()])
            should_fail(admin.competition.closeSubmission)

            challenge_number = admin.competition.getLatestChallengeNumber()
            assert admin.competition.getPhase(challenge_number) == 4, 'Challenge is in wrong phase! Should be in 4.'

            #############################
            ########## PHASE 1 ##########
            #############################
            dataset_hash = getHash()
            key_hash = getHash()

            old_cr = admin.competition.getCurrentChallengeRewardsBudget()
            old_tr = admin.competition.getCurrentTournamentRewardsBudget()

            tx = admin.competition.openChallenge(dataset_hash, key_hash, getTimestamp(), getTimestamp())
            challenge_number = admin.competition.getLatestChallengeNumber()

            current_cr = Decimal(admin.competition.getCurrentChallengeRewardsBudget())
            current_tr = admin.competition.getCurrentTournamentRewardsBudget()

            # assert old_cr != current_cr
            # assert old_tr != current_tr
            assert current_cr == int(Decimal(admin.competition.getCompetitionPool()) * Decimal('0.20'))
            assert current_tr == int(Decimal(admin.competition.getCompetitionPool()) * Decimal('0.60'))

            assert admin.competition.getPhase(challenge_number) == 1, 'Challenge is in wrong phase! Should be in 1.'
            assert admin.competition.getDatasetHash(challenge_number).hex() == dataset_hash, 'Dataset hash incorrect.'
            # assert admin.competition.getDatasetHashList(challenge_number, challenge_number)[0].hex() == dataset_hash, 'Dataset hash list incorrect.'
            assert admin.competition.getKeyHash(challenge_number).hex() == key_hash, 'Key hash incorrect.'
            # assert admin.competition.getKeyHashList(challenge_number, challenge_number)[0].hex() == key_hash, 'Key hash incorrect.'

            #####
            # test new staking and submissions logic
            #####

            p = participants[-1]
            try:
                p.token.setStake(p.competition.address(), 0)
            except:
                pass
            should_fail(p.competition.submitNewPredictions, [getHash()]) # submitNewPrediction 0, 0, 0
            should_fail(p.competition.updateSubmission,
                [p.competition.getSubmission(challenge_number, p.address).hex(),
                 getHash()])                                            # updateSubmission 0, 0, 0
            p.token.setStake(p.competition.address(), stake_threshold)  # increaseStake 0, 0, 1
            p.token.setStake(p.competition.address(),
                             stake_threshold - 1)                       # decreaseStake 1, 0, 1
            p.token.setStake(p.competition.address(), 0)                # decreaseStake 0, 0, 1
            p.token.setStake(p.competition.address(), stake_threshold)
            p.token.setStake(p.competition.address(),
                             stake_threshold + 1)                       # increaseStake 1, 0, 1
            should_fail(p.competition.updateSubmission,
                        [p.competition.getSubmission(challenge_number, p.address).hex(),
                         getHash()])                                    # updateSubmission 1, 0, 0
            p.competition.submitNewPredictions(getHash())               # submitNewPrediction 1, 0, 1
            should_fail(p.competition.submitNewPredictions,
                        [getHash()])                                    # submitNewPrediction 1, 1, 0
            p.token.setStake(p.competition.address(),
                             stake_threshold + 2)                       # increaseStake 1, 1, 1
            p.token.setStake(p.competition.address(), stake_threshold)    # decreaseStake 1, 1, 1 final stake >= threshold
            should_fail(p.token.setStake,
                        [p.competition.address(), stake_threshold-1])    # decreaseStake 1, 1, 0 final stake < threshold
            p.competition.updateSubmission(p.competition.getSubmission(challenge_number, p.address).hex(),
                         getHash())                                    # updateSubmission 1, 1, 1

            ## Withdraw
            length_of_submitters = admin.competition.getSubmissionCounter(challenge_number)
            p.competition.updateSubmission(p.competition.getSubmission(challenge_number, p.address).hex(),
                                           bytes(0))
            new_length_of_submitters = admin.competition.getSubmissionCounter(challenge_number)
            assert length_of_submitters == new_length_of_submitters + 1

            p.token.setStake(p.competition.address(), 0)
            # one more round after withdraw
            should_fail(p.competition.submitNewPredictions, [getHash()])  # submitNewPrediction 0, 0, 0
            should_fail(p.competition.updateSubmission,
                        [p.competition.getSubmission(challenge_number, p.address).hex(),
                         getHash()])  # updateSubmission 0, 0, 0
            p.token.setStake(p.competition.address(), stake_threshold)  # increaseStake 0, 0, 1
            p.token.setStake(p.competition.address(),
                             stake_threshold - 1)  # decreaseStake 1, 0, 1
            p.token.setStake(p.competition.address(), 0)  # decreaseStake 0, 0, 1
            p.token.setStake(p.competition.address(), stake_threshold)
            p.token.setStake(p.competition.address(),
                             stake_threshold + 1)  # increaseStake 1, 0, 1
            should_fail(p.competition.updateSubmission,
                        [p.competition.getSubmission(challenge_number, p.address).hex(),
                         getHash()])  # updateSubmission 1, 0, 0
            p.competition.submitNewPredictions(getHash())  # submitNewPrediction 1, 0, 1
            should_fail(p.competition.submitNewPredictions,
                        [getHash()])  # submitNewPrediction 1, 1, 0
            p.token.setStake(p.competition.address(),
                             stake_threshold + 2)  # increaseStake 1, 1, 1
            p.token.setStake(p.competition.address(), stake_threshold)  # decreaseStake 1, 1, 1 final stake >= threshold
            should_fail(p.token.setStake,
                        [p.competition.address(), stake_threshold - 1])  # decreaseStake 1, 1, 0 final stake < threshold
            p.competition.updateSubmission(p.competition.getSubmission(challenge_number, p.address).hex(),
                                           getHash())  # updateSubmission 1, 1, 1
            # Reset
            p.competition.updateSubmission(p.competition.getSubmission(challenge_number, p.address).hex(),
                                           bytes(0))
            p.token.setStake(p.competition.address(), 0)


            stakers = getRandomSelection(participants, min_num=len(participants) * 3 // 4)

            # Increase Stake
            for i in range(len(stakers)):
                p = stakers[i]
                stake_amount = getRandomAmount(p)
                # if p.token.getPermission(p.address, admin.competition.address()):
                #     should_fail(p.token.grantPermission, [admin.competition.address()])
                # else:
                #     tx0 = p.token.grantPermission(admin.competition.address())

                if random.choice([True, False]):
                    tx1 = p.token.setStake(p.competition.address(), stake_amount)
                    assert p.competition.getStake(p.address) == stake_amount == p.token.getStake(p.competition.address(), p.address)
                else:
                    current_stake = p.competition.getStake(p.address)
                    should_fail(p.competition.increaseStake, [p.address, stake_amount])
                    tx1 = p.token.increaseStake(p.competition.address(), stake_amount)
                    assert p.competition.getStake(p.address) == (current_stake + stake_amount) == p.token.getStake(p.competition.address(), p.address)

            # Decrease Stake
            random_stakers = getRandomSelection(stakers)

            for i in range(len(random_stakers)):
                p = random_stakers[i]
                staked = p.competition.getStake(p.address)
                decrease_amt = random.randint(0, staked)

                if random.choice([True, False]):
                    tx = p.token.setStake(p.competition.address(), decrease_amt)
                    assert p.competition.getStake(p.address) == decrease_amt == p.token.getStake(p.competition.address(), p.address)
                else:
                    current_stake = p.competition.getStake(p.address)
                    should_fail(p.competition.decreaseStake, [p.address, stake_amount])
                    tx = p.token.decreaseStake(p.competition.address(), decrease_amt)
                    assert p.competition.getStake(p.address) == (current_stake - decrease_amt) == p.token.getStake(p.competition.address(), p.address)

            # Send Submission
            submitters = getRandomSelection(stakers, min_num=len(stakers) * 9 // 10)
            stake_min = admin.competition.getStakeThreshold()

            for p in submitters:
                staked = p.competition.getStake(p.address)
                p.competition.getDatasetHash(challenge_number)
                if staked >= stake_min:
                    stake_before = p.competition.getStake(p.address)
                    tx = p.competition.submitNewPredictions(getHash())
                    # staking_should_fail(p, admin)

                    assert p.competition.getStake(p.address) == p.competition.getStakedAmountForChallenge(challenge_number, p.address)

                    should_fail(p.token.setStake, [p.competition.address(), stake_threshold - 1])
                    should_fail(p.token.decreaseStake, [p.competition.address(), p.token.getStake(p.competition.address(), p.address)-stake_threshold+1])

                else:
                    should_fail(p.competition.submitNewPredictions, [getHash()])


            for p in participants:
                submission = p.competition.getSubmission(challenge_number, p.address)
                if int(submission.hex(), 16) != 0:
                    p.competition.updateSubmission(submission, getHash())
                    assert p.competition.getStake(p.address) == p.competition.getStakedAmountForChallenge(
                        challenge_number, p.address)
                    # staking_should_fail(p, admin)

                    should_fail(p.token.setStake, [p.competition.address(), stake_threshold - 1])
                    should_fail(p.token.decreaseStake,
                                [p.competition.address(), p.token.getStake(p.competition.address(), p.address) - stake_threshold + 1])
                else:
                    should_fail(p.competition.updateSubmission, [submission, getHash()])

            # Invariant - Verify stake record
            for p in participants:
                submission = p.competition.getSubmission(challenge_number, p.address)
                if int(submission.hex(), 16) != 0:
                    # print('submission hash', submission.hex())
                    recorded_stake = admin.competition.getStake(p.address)
                    recorded_stake_b = admin.token.getStake(admin.competition.address(), p.address)
                    recorded_stake_c = admin.competition.getStakedAmountForChallenge(challenge_number, p.address)

                    assert recorded_stake == recorded_stake_b == recorded_stake_c, '{} : {} : {}'.format(
                        recorded_stake,
                        recorded_stake_b,
                        recorded_stake_c)
                else:
                    assert admin.competition.getStakedAmountForChallenge(challenge_number, p.address) == 0

            # Increase Stake should still work at this point regardless of submission
            for p in participants:
                stake_amount = getRandomAmount(p)

                if random.choice([True, False]):
                    tx1 = p.token.setStake(p.competition.address(), stake_amount)
                    assert p.competition.getStake(p.address) == stake_amount == p.token.getStake(
                        p.competition.address(), p.address)
                    submission = p.competition.getSubmission(challenge_number, p.address)
                    if int(submission.hex(), 16) != 0:
                        assert p.competition.getStake(p.address) == p.competition.getStakedAmountForChallenge(
                            challenge_number, p.address), '{} | {}'.format(p.competition.getStake(p.address), p.competition.getStakedAmountForChallenge(
                            challenge_number, p.address))
                else:
                    current_stake = p.competition.getStake(p.address)
                    should_fail(p.competition.increaseStake, [p.address, stake_amount])
                    tx1 = p.token.increaseStake(p.competition.address(), stake_amount)
                    assert p.competition.getStake(p.address) == (current_stake + stake_amount) == p.token.getStake(
                        p.competition.address(), p.address)
                    submission = p.competition.getSubmission(challenge_number, p.address)
                    if int(submission.hex(), 16) != 0:
                        assert p.competition.getStake(p.address) == p.competition.getStakedAmountForChallenge(
                            challenge_number, p.address)

            # Test Withdrawals
            # withdrawers = getRandomSelection(submitters, min_num=1)
            # print('withdrawers', withdrawers)

            # submitters = list(set(submitters).difference(set(withdrawers)))

            unauthorized_actions_should_fail(stakers[0], admin)
            # should_fail(stakers[0].competition.submitNewPredictions, [getHash()])
            # should_fail(stakers[0].competition.updateSubmission, [admin.competition.getSubmission(challenge_number, stakers[0].address), getHash()])

            should_fail(admin.competition.openChallenge, [getHash(), getHash(), getTimestamp(), getTimestamp()])
            should_fail(admin.competition.sponsor, [1])
            should_fail(admin.competition.submitResults, [getHash()])
            challenge_number = admin.competition.getLatestChallengeNumber()
            should_fail(admin.competition.updateResults, [admin.competition.getResultsHash(challenge_number), getHash()])
            should_fail(p.competition.payRewards, [[p.address],[1], [1], [1]])
            should_fail(admin.competition.payStakingRewards, [[admin.address], [1]])
            should_fail(admin.competition.advanceToPhase, [3])
            should_fail(admin.competition.advanceToPhase, [4])

            #############################
            ########## PHASE 2 ##########
            #############################
            tx = admin.competition.closeSubmission()
            challenge_number = admin.competition.getLatestChallengeNumber()

            unauthorized_actions_should_fail(stakers[0], admin)
            staking_should_fail(random.choice(participants), admin)
            should_fail(submitters[0].competition.submitNewPredictions, [getHash()])
            should_fail(submitters[0].competition.updateSubmission,
                        [submitters[0].competition.getSubmission(challenge_number, submitters[0].address), getHash()])

            should_fail(admin.competition.closeSubmission)
            should_fail(admin.competition.openChallenge, [getHash(), getHash(), getTimestamp(), getTimestamp()])
            should_fail(admin.competition.sponsor, [1])
            should_fail(admin.competition.updateDataset, [admin.competition.getDatasetHash(challenge_number), getHash()])
            should_fail(admin.competition.submitResults, [getHash()])
            challenge_number = admin.competition.getLatestChallengeNumber()
            should_fail(admin.competition.updateResults, [admin.competition.getResultsHash(challenge_number), getHash()])
            should_fail(p.competition.payRewards, [[p.address], [1], [1], [1]])
            # should_fail(admin.competition.payStakingRewards, [[admin.address], [1]])
            # should_fail(admin.competition.advanceToPhase, [3])
            should_fail(admin.competition.advanceToPhase, [4])

            assert admin.competition.getPhase(challenge_number) == 2, 'Challenge is in wrong phase! Should be in 2.'

            submitters_list = admin.competition.getSubmitters(challenge_number, 0, admin.competition.getSubmissionCounter(challenge_number))

            # Verify Submitters
            assert admin.competition.getSubmissionCounter(challenge_number) == len(submitters), "Submitters length incorrect!"
            assert set(map(lambda x: x.address, submitters)) == set(submitters_list), "Problem with the set of submitters!"

            participation_rewards_list = []
            for s in submitters_list:
                participation_rewards_list.append(admin.competition.computeStakingReward(s))

            # Invariant - Verify stake record
            for p in participants:
                submission = p.competition.getSubmission(challenge_number, p.address)
                if int(submission.hex(), 16) != 0:
                    recorded_stake = admin.competition.getStake(p.address)
                    recorded_stake_b = admin.token.getStake(admin.competition.address(), p.address)
                    recorded_stake_c = admin.competition.getStakedAmountForChallenge(challenge_number, p.address)

                    assert recorded_stake == recorded_stake_b == recorded_stake_c, '{} : {} : {}'.format(
                        recorded_stake,
                        recorded_stake_b,
                        recorded_stake_c)
                else:
                    assert admin.competition.getStakedAmountForChallenge(challenge_number, p.address) == 0

            # tx = admin.competition.payStakingRewards(submitters_list, participation_rewards_list)
                # print(tx['gasUsed'])


            # Verify participation rewards payment.
            for i in range(len(submitters_list)):
                s = submitters_list[i]
                current_stake = admin.competition.getStake(s)
                staked = admin.competition.getStakedAmountForChallenge(challenge_number, s)
                reward = 0 #participation_rewards_list[i]
                assert current_stake-staked == reward, "{} != {}".format(current_stake-staked, reward)

            #############################
            ########## PHASE 3 ##########
            #############################
            tx = admin.competition.advanceToPhase(3)
            challenge_number = admin.competition.getLatestChallengeNumber()
            assert admin.competition.getPhase(challenge_number) == 3, 'Challenge is in wrong phase! Should be in 3.'

            unauthorized_actions_should_fail(stakers[0], admin)
            # staking_should_fail(submitters[0], admin)
            should_fail(submitters[0].competition.submitNewPredictions, [getHash()])
            should_fail(submitters[0].competition.updateSubmission, [submitters[0].competition.getSubmission(challenge_number,submitters[0].address), getHash()])

            should_fail(admin.competition.closeSubmission)
            should_fail(admin.competition.openChallenge, [getHash(), getHash(), getTimestamp(), getTimestamp()])
            should_fail(admin.competition.sponsor, [1])
            should_fail(admin.competition.updateDataset, [admin.competition.getDatasetHash(challenge_number), getHash()])
            # should_fail(admin.competition.submitResults, [getHash()])
            challenge_number = admin.competition.getLatestChallengeNumber()
            # should_fail(admin.competition.updateResults, [admin.competition.getResultsHash(challenge_number), getHash()])
            # should_fail(admin.competition.payPerformanceRewards, [[admin.address], [1]])
            should_fail(admin.competition.payStakingRewards, [[admin.address], [1]])
            should_fail(admin.competition.advanceToPhase, [3])
            # should_fail(admin.competition.advanceToPhase, [4])

            tx = admin.competition.submitResults(getHash())
            admin.competition.updateResults(admin.competition.getResultsHash(challenge_number), getHash())

            # make rewards payment
            staking_rewards_budget = admin.competition.getCurrentStakingRewardsBudget()
            challenge_rewards_budget = admin.competition.getCurrentChallengeRewardsBudget()
            tournament_rewards_budget = admin.competition.getCurrentTournamentRewardsBudget()

            awardees = getRandomSelection(submitters, min_num= len(submitters) * 1 // 2)
            winners = []
            staking_rewards = []
            challenge_rewards = []
            tournament_rewards = []
            challenge_scores = []
            tournament_scores = []
            proportion = random.randint(0, 95)
            rand_ceil = 95 - proportion
            for a in awardees[:-1]:
                winners.append(a.address)
                staking_rewards.append(int(proportion * staking_rewards_budget // 100))
                challenge_rewards.append(int(proportion * challenge_rewards_budget // 100))
                tournament_rewards.append(int(proportion * tournament_rewards_budget // 100))
                challenge_scores.append(int(random.random() * 1e18))
                tournament_scores.append(int(random.random() * 1e18))
                proportion = random.randint(0, rand_ceil)
                rand_ceil = rand_ceil - proportion

            winners.append(awardees[-1].address)
            total_rewards = sum(staking_rewards)
            staking_rewards.append(int(staking_rewards_budget - total_rewards))
            total_rewards = sum(challenge_rewards)
            challenge_rewards.append(int(challenge_rewards_budget - total_rewards))
            total_rewards = sum(tournament_rewards)
            tournament_rewards.append(int(tournament_rewards_budget - total_rewards))
            challenge_scores.append(int(random.random() * 1e18))
            tournament_scores.append(int(random.random() * 1e18))

            tx = admin.competition.payRewards(winners, staking_rewards, challenge_rewards, tournament_rewards)
            tx = admin.competition.updateChallengeAndTournamentScores(winners, challenge_scores, tournament_scores)

            for i in range(len(winners)):
                assert staking_rewards[i] == admin.competition.getStakingRewards(challenge_number, winners[i])
                assert challenge_rewards[i] == admin.competition.getChallengeRewards(challenge_number, winners[i])
                assert tournament_rewards[i] == admin.competition.getTournamentRewards(challenge_number, winners[i])
                assert challenge_scores[i] == admin.competition.getChallengeScores(challenge_number, winners[i])
                assert tournament_scores[i] == admin.competition.getTournamentScores(challenge_number, winners[i])

            #############################
            ########## PHASE 4 ##########
            #############################
            tx = admin.competition.advanceToPhase(4)

            should_fail(admin.competition.closeSubmission)
            should_fail(admin.competition.openChallenge, [getHash(), getHash(), getTimestamp(), getTimestamp()])
            should_fail(admin.competition.updateDataset, [admin.competition.getDatasetHash(challenge_number), getHash()])
            should_fail(admin.competition.submitResults, [getHash()])
            challenge_number = admin.competition.getLatestChallengeNumber()
            # should_fail(admin.competition.updateResults, [admin.competition.getResultsHash(challenge_number), getHash()])
            # should_fail(admin.competition.payPerformanceRewards, [[admin.address], [1]])
            should_fail(admin.competition.payStakingRewards, [[admin.address], [1]])
            should_fail(admin.competition.advanceToPhase, [3])
            should_fail(admin.competition.advanceToPhase, [4])
            should_fail(admin.competition.advanceToPhase, [2])
            should_fail(admin.competition.advanceToPhase, [1])
            assert admin.competition.getPhase(challenge_number) == 4, 'Challenge is in wrong phase! Should be in 4.'
            priv_key = getHash()
            admin.competition.updatePrivateKey(challenge_number, priv_key)
            read_priv_key = admin.competition.getPrivateKeyHash(challenge_number).hex()
            assert priv_key == read_priv_key, "Private key incorrect. {} vs {}".format(priv_key, read_priv_key)

        print('###### Upgrading contract ######')

        admin.old_competition_deploy()
        # data = admin.old_competition.contract.encodeABI(fn_name= 'initialize', args= [stake_threshold, challenge_rewards_threshold, admin.token.address()])

        check_values = [admin.competition.getCompetitionPool(),
                        admin.competition.getSubmission(1, participants[1].address),
                        admin.competition.getStake(participants[1].address),
                        admin.competition.getCurrentTotalStaked(),
                        admin.competition.getSubmitters(1, 0 , 1)
        ]

        # admin.proxy_admin.upgrade(admin.proxy_upgradeable.address(), admin.old_competition.address())

        ## Check MultiSig ###
        print('Using MultiSig as Proxy admin...')

        assert admin.proxy_admin.getProxyImplementation(admin.proxy_upgradeable.address()) == before_addr

        admin.proxy_admin.transferOwnership(admin.multisig.address())
        should_fail(admin.proxy_admin.upgrade, [admin.proxy_upgradeable.address(), admin.old_competition.address()])
        should_fail(owners[2].proxy_admin.upgrade, [admin.proxy_upgradeable.address(), admin.old_competition.address()])

        data = admin.proxy_admin.contract.encodeABI(fn_name='upgrade', args=[admin.proxy_upgradeable.address(), admin.old_competition.address()])

        assert int(admin.multisig.transactionCount()) == 0

        owners[1].multisig.submitTransaction(destination=admin.proxy_admin.address(),value=0,data=data)

        tx_list = owners[0].multisig.getTransactionIds(0, admin.multisig.transactionCount(), pending=True, executed=False)
        latest_tx_id = tx_list[-1]
        tx = owners[0].multisig.transactions(latest_tx_id)
        dst = tx[0]
        val = tx[1]
        dta = tx[2]
        exd = tx[3]

        assert dst == admin.proxy_admin.address(), '{} != {}'.format(dst, admin.proxy_admin.address())
        assert val == 0
        assert '0x{}'.format(dta.hex()) == data, '{} vs {}'.format('0x{}'.format(dta.hex()), data)
        assert exd == False

        owners[2].multisig.confirmTransaction(latest_tx_id)
        owners[3].multisig.confirmTransaction(latest_tx_id)
        owners[4].multisig.confirmTransaction(latest_tx_id)
        owners[5].multisig.confirmTransaction(latest_tx_id)

        tx = owners[0].multisig.transactions(latest_tx_id)
        assert tx[3] == False

        assert admin.proxy_admin.getProxyImplementation(admin.proxy_upgradeable.address()) == impl_address
        owners[6].multisig.confirmTransaction(latest_tx_id)
        tx = owners[0].multisig.transactions(latest_tx_id)
        assert tx[3] == True

        assert admin.proxy_admin.getProxyImplementation(admin.proxy_upgradeable.address()) == admin.old_competition.address()
        admin.old_competition_init(admin.proxy_upgradeable.address())

        check_values_upgraded = [admin.old_competition.getCompetitionPool(),
                        admin.old_competition.getSubmission(1, participants[1].address),
                        admin.old_competition.getStake(participants[1].address),
                        admin.old_competition.getCurrentTotalStaked(),
                        admin.old_competition.getSubmitters(1, 0 ,1)
        ]

        assert check_values == check_values_upgraded

        print('{} challenge rounds completed for this competition.'.format(challenge_round+1))
        print('Total time taken: {}s.'.format(int(time.time()-start)))




    except:
        print(traceback.format_exc())
    #
    finally:
        print('Total time taken: {}s.'.format(int(time.time() - start)))
        proc.kill()

        while True:
            if proc.poll() is None:
                time.sleep(2)
            else:
                break