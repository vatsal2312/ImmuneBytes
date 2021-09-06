'''
This script tests basic accessibility restrictions for functions in the Tournament Contract that 
should only be executable by admin accounts.

Note: There should be at least 10 unlocked accounts for this test to run.
'''

import pytest, string,time
from brownie import Tournament, Token, accounts, reverts, web3
from brownie import Airdrop
from hashlib import sha256
import random 

CONTEST_DURATION = 4
DECIMALS = 1000000000000000000 #(1e18)
SPONSOR_AMOUNT = 3000000 * DECIMALS
REG_FEE = 5 * DECIMALS
AIRDROP_AMOUNT = 1000 * DECIMALS

# @pytest.fixture
def setup():
    print(accounts)

    token = accounts[0].deploy(Token,"RockCap Token", "Token",required_confs=1)
    tournament = accounts[0].deploy(Tournament, REG_FEE, token,required_confs=1)

    print('Token contract deployed at {}'.format(token))
    print('Tournament contract deployed at {}'.format(tournament))

    rci_admin = accounts[0]
    token.mint(rci_admin.address, SPONSOR_AMOUNT * 10, {'from': rci_admin})

    # Airdrop all accounts
    for a in accounts:
        token.mint(a.address, AIRDROP_AMOUNT, {'from': rci_admin})
    
    return token, tournament

def getRandomString(n = 128, seed = 7):
    return ''.join(random.choice(string.ascii_letters) for i in range(n))

def grantAdminRights(tournament, grantee, granter):
    tournament.grantRole(0, grantee.address, {'from': granter})

def revokeAdminRights(tournament, revokee, revoker):
    tournament.grantRole(0, revokee.address, {'from': revoker})

def test_tournament_admin_access(setup):
    token, tournament = setup
    rci_admin = accounts[0]

    # function updateSubmissionFee(uint256 newFee) 
    regFee = tournament.getSubmissionFee({'from': rci_admin})
    regFee *= 2
    tournament.updateSubmissionFee(regFee, {'from': rci_admin})
    newRegFee = tournament.getSubmissionFee({'from': rci_admin})
    assert regFee == newRegFee

    badAccount = accounts[random.randint(1,10)]
    oldRegFee = newRegFee
    regFee *= 2
    with reverts():
        tournament.updateSubmissionFee(regFee, {'from': badAccount})
    newRegFee = tournament.getSubmissionFee({'from': rci_admin})
    assert oldRegFee == newRegFee

    token.increaseAllowance(tournament.address, SPONSOR_AMOUNT * 3, {'from': rci_admin})
    tournament.sponsor(SPONSOR_AMOUNT * 3,{'from': rci_admin})

    # function openPhase(bytes32 dataset_ref) external override returns (uint32 phaseIndex)
    content = getRandomString()
    datasetHash = sha256(content.encode('utf-8')).hexdigest()
    oldPhaseIndex = tournament.getLastPhaseIndex()
    with reverts():
        tournament.openPhase(datasetHash, {'from': badAccount})
    newPhaseIndex = tournament.getLastPhaseIndex()
    assert oldPhaseIndex == newPhaseIndex
    tournament.openPhase(datasetHash, {'from': rci_admin})
    phaseIndex = tournament.getLastPhaseIndex()

    # function updatePhaseDataset(uint32 phaseIndex, bytes32 dataset_old, bytes32 dataset_new) external override returns (bool success)
    content = getRandomString()
    inputNewDatasetHash = sha256(content.encode('utf-8')).hexdigest()
    oldDatasetHash = tournament.getPhaseDatasetHash(phaseIndex)
    with reverts():
        tournament.updatePhaseDataset(oldDatasetHash, inputNewDatasetHash, {'from': badAccount})
    newDatasetHash = tournament.getPhaseDatasetHash(phaseIndex)
    assert oldDatasetHash == newDatasetHash
    tournament.updatePhaseDataset(oldDatasetHash, inputNewDatasetHash, {'from': rci_admin})
    newDatasetHash = tournament.getPhaseDatasetHash(phaseIndex)
    assert oldDatasetHash != newDatasetHash

    # function closePhase(uint32 phaseIndex, bytes32 resultsHash) external override
    content = getRandomString()
    resultsHash = sha256(content.encode('utf-8')).hexdigest()
    phaseStatus = tournament.getPhaseStatus(phaseIndex)
    assert phaseStatus == True
    with reverts():
        tournament.closePhase({'from': badAccount})
    phaseStatus = tournament.getPhaseStatus(phaseIndex)
    assert phaseStatus == True
    tournament.closePhase({'from': rci_admin})
    phaseStatus = tournament.getPhaseStatus(phaseIndex)
    assert phaseStatus == False

    # function updatePhaseResults(uint32 phaseIndex, bytes32 oldResultsHash, bytes32 newResultsHash) public override
    content = getRandomString()
    inputNewResultsHash = sha256(content.encode('utf-8')).hexdigest()
    oldResultsHash = tournament.getPhaseResultsHash(phaseIndex)
    with reverts():
        tournament.updatePhaseResults(oldResultsHash, inputNewResultsHash, {'from': badAccount})
    newResultsHash = tournament.getPhaseResultsHash(phaseIndex)
    assert oldResultsHash == newResultsHash
    tournament.updatePhaseResults(oldResultsHash, inputNewResultsHash, {'from': rci_admin})
    oldResultsHash = newResultsHash
    newResultsHash = tournament.getPhaseResultsHash(phaseIndex)
    assert oldResultsHash != newResultsHash

    tournament.payRewards([accounts[0], accounts[1]], [1] * 2)
    tournament.resolveStakes([accounts[0], accounts[1]], [True] * 2, [1] * 2)

    # let the rest of the phases be opened and then closed.
    for i in range(CONTEST_DURATION - 1):
        content = getRandomString()
        datasetHash = sha256(content.encode('utf-8')).hexdigest()
        tournament.openPhase(datasetHash, {'from': rci_admin})
        phaseIndex = tournament.getLastPhaseIndex()
        content = getRandomString()
        resultsHash = sha256(content.encode('utf-8')).hexdigest()
        tournament.closePhase({'from': rci_admin})
        tournament.submitPhaseResults(resultsHash)
        tournament.payRewards([accounts[0], accounts[1]], [1] * 2)
        tournament.resolveStakes([accounts[0], accounts[1]], [True] * 2, [1] * 2)
        if random.randint(1,3) == 1:
            content = getRandomString()
            newResultsHash = sha256(content.encode('utf-8')).hexdigest()
            tournament.updatePhaseResults(resultsHash, newResultsHash)

    # function payout(uint32 contestIndex, address[] calldata winners, uint256[] calldata rewards) external override returns (bool success)
    numWinners = 5
    phaseIndex = tournament.getLastPhaseIndex()
    winners = accounts[5: 5+numWinners]
    rewards = [random.randint(1,10) * DECIMALS for i in range(numWinners)]

    oldBalances = []
    for i in range(numWinners):
        oldBalances.append(tournament.getBalance(winners[i].address))
    with reverts():
        tournament.payRewards(winners, rewards, {'from': badAccount})
    newBalances = []
    for i in range(numWinners):
        newBalances.append(tournament.getBalance(winners[i].address))
    assert oldBalances == newBalances

    tournament.payRewards(winners, rewards, {'from': rci_admin})
    for i in range(numWinners):
        newBal = tournament.getBalance(winners[i].address)
        assert newBal > oldBalances[i]