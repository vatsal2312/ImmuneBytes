class Competition:
    def __init__(self, json_path, w3, address, controlling_account=None, verbose=True, deploy=False, deploy_args_list = [], gas_price_in_wei=None) :       
        import json, os
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        json_path = '{}/{}'.format(dir_path, json_path)
        with open(json_path) as f:
            compiled = json.load(f)
        abi = compiled['abi']
        bytecode = compiled['bytecode']
        contract = w3.eth.contract(abi=abi, bytecode=bytecode)

        self.timeout = 600
        self.interval = 15
        
        if deploy:
            tx_data = contract.constructor(*deploy_args_list).buildTransaction({'from': controlling_account.address, 'gasPrice': int(gas_price_in_wei), 'nonce': w3.eth.getTransactionCount(controlling_account.address)})
            signed_tx = w3.eth.account.sign_transaction(tx_data, controlling_account.privateKey)
            tx_id = w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
            print('Deploying Competition Contract.')
            address = w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval).contractAddress
            print('Competition Contract deployed at {}.'.format(address))

        self.w3 = w3
        self.contract = contract(address=address)
        if type(controlling_account) is str:
            self.controlling_account_address = controlling_account
        else:
            self.controlling_account_address = controlling_account.address
        self.controlling_account = controlling_account
        self.verbose = verbose
        self.eventSignatureToName = self.esInit()  

    def constructor(self,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.constructor().buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def constructor_signature(self):
        return '0x90fa17bb11fb41b369ce056a8d718bb44439a353f1e9646fcc59ebb502997d48'

    def BatchInformationUpdated(self,challengeNumber,itemNumber,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.BatchInformationUpdated(challengeNumber,itemNumber).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def BatchInformationUpdated_signature(self):
        return '0xdfc0e8d429222115bcdeae8834d5fbcecc360f743768fc2a9693a30a379999e9'

    def ChallengeAndTournamentScoresUpdated(self,challengeNumber,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.ChallengeAndTournamentScoresUpdated(challengeNumber).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def ChallengeAndTournamentScoresUpdated_signature(self):
        return '0x6fa7224843e16ab8c76a13b984cfcf54de67707a118bf52ce93e0e5be3589871'

    def ChallengeOpened(self,challengeNumber,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.ChallengeOpened(challengeNumber).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def ChallengeOpened_signature(self):
        return '0x9da6f4cd0f617f153c3ebc9840a08792cff9f0fd8c796ce09c5d2006f42da6d9'

    def ChallengeRewardsPercentageInWeiUpdated(self,newPercentage,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.ChallengeRewardsPercentageInWeiUpdated(newPercentage).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def ChallengeRewardsPercentageInWeiUpdated_signature(self):
        return '0x94327140b3bb3bb989865fef53b345cd1ddd7991b30e3233137ab646448fbeb5'

    def DatasetUpdated(self,challengeNumber,oldDatasetHash,newDatasetHash,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.DatasetUpdated(challengeNumber,oldDatasetHash,newDatasetHash).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def DatasetUpdated_signature(self):
        return '0xb4ad7e2453c3c06a28c5cfe29a3067c6edde6eb03be4df2a461f9d806cb747e'

    def KeyUpdated(self,challengeNumber,oldKeyHash,newKeyHash,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.KeyUpdated(challengeNumber,oldKeyHash,newKeyHash).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def KeyUpdated_signature(self):
        return '0x7a2b6b0f48d13449d72d8fd2c1fae94cd13c970cc0dc738abd0bae8d50ce81c6'

    def MessageUpdated(self,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.MessageUpdated().buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def MessageUpdated_signature(self):
        return '0x89dbe1e8a053a391becc713b9c088b57cf1855cf857803e49eaae2f8fbc3b1cd'

    def RemainderMovedToPool(self,remainder,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.RemainderMovedToPool(remainder).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def RemainderMovedToPool_signature(self):
        return '0xda446d0471a795498335ed4bc219b34921a12ccb87136a9aa03964adc83eadf3'

    def ResultsUpdated(self,challengeNumber,oldResultsHash,newResultsHash,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.ResultsUpdated(challengeNumber,oldResultsHash,newResultsHash).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def ResultsUpdated_signature(self):
        return '0xfb7d772905d44c5fdd59d4ab87c7f40281e09f93e2e189d03737c6d82b154ea'

    def RewardsPayment(self,submitter,stakingReward,challengeReward,tournamentReward,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.RewardsPayment(submitter,stakingReward,challengeReward,tournamentReward).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def RewardsPayment_signature(self):
        return '0x477dc5f7f393ee9f6c7e7723662b2b8baf8f4035f59afb91d507a48ced102414'

    def RewardsThresholdUpdated(self,newThreshold,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.RewardsThresholdUpdated(newThreshold).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def RewardsThresholdUpdated_signature(self):
        return '0x73e002420a7defb91818836f9aaa83222b749a40c213c7c0fbccaacdd259e052'

    def RoleAdminChanged(self,role,previousAdminRole,newAdminRole,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.RoleAdminChanged(role,previousAdminRole,newAdminRole).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def RoleAdminChanged_signature(self):
        return '0xbd79b86ffe0ab8e8776151514217cd7cacd52c909f66475c3af44e129f0b00ff'

    def RoleGranted(self,role,account,sender,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.RoleGranted(role,account,sender).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def RoleGranted_signature(self):
        return '0x2f8788117e7eff1d82e926ec794901d17c78024a50270940304540a733656f0d'

    def RoleRevoked(self,role,account,sender,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.RoleRevoked(role,account,sender).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def RoleRevoked_signature(self):
        return '0xf6391f5c32d9c69d2a47ea670b442974b53935d1edc7fd64eb21e047a839171b'

    def Sponsor(self,sponsorAddress,sponsorAmount,poolTotal,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.Sponsor(sponsorAddress,sponsorAmount,poolTotal).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def Sponsor_signature(self):
        return '0x64939930c3fd0a1fe9e7fb9810272db7730a0f02b900972787bcb79fb6fd3d2d'

    def StakeDecreased(self,sender,amount,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.StakeDecreased(sender,amount).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def StakeDecreased_signature(self):
        return '0x700865370ffb2a65a2b0242e6a64b21ac907ed5ecd46c9cffc729c177b2b1c69'

    def StakeIncreased(self,sender,amount,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.StakeIncreased(sender,amount).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def StakeIncreased_signature(self):
        return '0x8b0ed825817a2e696c9a931715af4609fc60e1701f09c89ee7645130e937eb2d'

    def StakeThresholdUpdated(self,newStakeThreshold,adminAddress,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.StakeThresholdUpdated(newStakeThreshold,adminAddress).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def StakeThresholdUpdated_signature(self):
        return '0xc3dad8d972694b8a948b4205b1bb45cbb2c73729f86630689e1e41c36a2965fa'

    def StakingRewardsPaid(self,challengeNumber,totalAmount,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.StakingRewardsPaid(challengeNumber,totalAmount).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def StakingRewardsPaid_signature(self):
        return '0xc3168f2e7fdefcb5cb67cfb93778f32d4b25929f83d45e1bb44339f2161ba7f6'

    def StakingRewardsPayment(self,participant,rewardAmount,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.StakingRewardsPayment(participant,rewardAmount).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def StakingRewardsPayment_signature(self):
        return '0x6132076a840070359367c4279185181db454eae48a2c6c661e56f50ff312e044'

    def SubmissionClosed(self,challengeNumber,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.SubmissionClosed(challengeNumber).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def SubmissionClosed_signature(self):
        return '0xaa5ebdc7900b87a79257aabbab219af255ada0be7148632ce5afcd622df7a88b'

    def SubmissionUpdated(self,challengeNumber,participantAddress,newSubmissionHash,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.SubmissionUpdated(challengeNumber,participantAddress,newSubmissionHash).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def SubmissionUpdated_signature(self):
        return '0x953e3b79bb71898776bb2ef8bb919748c883b8b27c42e334de1ecdbf79d472bb'

    def TotalRewardsPaid(self,challengeNumber,totalStakingAmount,totalChallengeAmount,totalTournamentAmount,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.TotalRewardsPaid(challengeNumber,totalStakingAmount,totalChallengeAmount,totalTournamentAmount).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def TotalRewardsPaid_signature(self):
        return '0x17db0090e1a5606c55a062c8168003b4709555ded702adf58612ccfe1b5ef72f'

    def TournamentRewardsPercentageInWeiUpdated(self,newPercentage,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.TournamentRewardsPercentageInWeiUpdated(newPercentage).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def TournamentRewardsPercentageInWeiUpdated_signature(self):
        return '0x211318e1b6942c96eaad65d5f6c4c520722236466093427de4dacb729bd36dfb'

    def DEFAULT_ADMIN_ROLE(self):
        return self.contract.functions.DEFAULT_ADMIN_ROLE().call({'from': self.controlling_account_address})

    def DEFAULT_ADMIN_ROLE_signature(self):
        return '0xa217fddfde7807bb766525e432eeeecaaf4de889a05e8df9fb827257fb978cf4'

    def RCI_CHILD_ADMIN(self):
        return self.contract.functions.RCI_CHILD_ADMIN().call({'from': self.controlling_account_address})

    def RCI_CHILD_ADMIN_signature(self):
        return '0x1442b868d2f8018bc8d42545315eaf4cc147c61478feb7c4bea741088bcc606b'

    def RCI_MAIN_ADMIN(self):
        return self.contract.functions.RCI_MAIN_ADMIN().call({'from': self.controlling_account_address})

    def RCI_MAIN_ADMIN_signature(self):
        return '0x18b125d1a509951ab885282b7714b08ed849768106e32e433beb7a704d7db908'

    def advanceToPhase(self,phase,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.advanceToPhase(phase).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def advanceToPhase_signature(self):
        return '0xdc9f76eb4d55e54402dae5449f850093d7e41ddb03c19f12d69a643e0a89022c'

    def closeSubmission(self,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.closeSubmission().buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def closeSubmission_signature(self):
        return '0xffc6ff1e03e42248bd1fd91651f00e0eb1e056ac28afdea1e97d34f042b5c529'

    def computeStakingReward(self,participant):
        return self.contract.functions.computeStakingReward(participant).call({'from': self.controlling_account_address})

    def computeStakingReward_signature(self):
        return '0x7bf68a3b82a86385ff13524f44456cf0d04ffa386b8c71b9ea831f78d2e246c7'

    def decreaseStake(self,staker,amountToken,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.decreaseStake(staker,amountToken).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def decreaseStake_signature(self):
        return '0x1a73ba01d85313ec153146459d5a578e6ae7f7a19820500a07d9dd9a991bbf7c'

    def getChallengeRewards(self,challengeNumber,participant):
        return self.contract.functions.getChallengeRewards(challengeNumber,participant).call({'from': self.controlling_account_address})

    def getChallengeRewards_signature(self):
        return '0x3cbcb53a83939614eec6464f798d4426b0aba4e4d98e55fc71dce1cc11b2dcf6'

    def getChallengeRewardsPercentageInWei(self):
        return self.contract.functions.getChallengeRewardsPercentageInWei().call({'from': self.controlling_account_address})

    def getChallengeRewardsPercentageInWei_signature(self):
        return '0x93a9dac7868cff88be6ba5997079d258233bec6725d7f81995e1905b845eba2d'

    def getChallengeScores(self,challengeNumber,participant):
        return self.contract.functions.getChallengeScores(challengeNumber,participant).call({'from': self.controlling_account_address})

    def getChallengeScores_signature(self):
        return '0xd885e39b3794407d7aaa59c1c6b4d4cd93f9d66577501462bc3e219cc53a5935'

    def getCompetitionPool(self):
        return self.contract.functions.getCompetitionPool().call({'from': self.controlling_account_address})

    def getCompetitionPool_signature(self):
        return '0xd4f4b806e153ce83a6a91553e5334f659253f310b3a1161e27ec63de0a0169c5'

    def getCurrentChallengeRewardsBudget(self):
        return self.contract.functions.getCurrentChallengeRewardsBudget().call({'from': self.controlling_account_address})

    def getCurrentChallengeRewardsBudget_signature(self):
        return '0xd68a7c00c2e3d4a313dbc5be88fccf14dae6c1c667192e3b3f64388bfcd90f7d'

    def getCurrentStakingRewardsBudget(self):
        return self.contract.functions.getCurrentStakingRewardsBudget().call({'from': self.controlling_account_address})

    def getCurrentStakingRewardsBudget_signature(self):
        return '0x1e2ff711835ce68e3e4c25895511dd039c8d7f79b7f94f657bbd08441d22586e'

    def getCurrentTotalStaked(self):
        return self.contract.functions.getCurrentTotalStaked().call({'from': self.controlling_account_address})

    def getCurrentTotalStaked_signature(self):
        return '0x25b067461fadf3c0cb8169ec223a9964320845d428e65fa1474f4123ce3d8c5d'

    def getCurrentTournamentRewardsBudget(self):
        return self.contract.functions.getCurrentTournamentRewardsBudget().call({'from': self.controlling_account_address})

    def getCurrentTournamentRewardsBudget_signature(self):
        return '0x3228cf728085e656303b783c5248ed82c37eb2354d6015f1f1fc5d998fa7d1ef'

    def getDatasetHash(self,challengeNumber):
        return self.contract.functions.getDatasetHash(challengeNumber).call({'from': self.controlling_account_address})

    def getDatasetHash_signature(self):
        return '0x39e287774455340b77e7c4f62dc30977c7fadb0169f3f8b40fc253216cc59cfa'

    def getDeadlines(self,challengeNumber,index):
        return self.contract.functions.getDeadlines(challengeNumber,index).call({'from': self.controlling_account_address})

    def getDeadlines_signature(self):
        return '0x57d0cf586665801895da5830ec1daa9cf22202c7d0bd27df16b1ba8da8e32d19'

    def getInformation(self,challengeNumber,participant,itemNumber):
        return self.contract.functions.getInformation(challengeNumber,participant,itemNumber).call({'from': self.controlling_account_address})

    def getInformation_signature(self):
        return '0xe7d5c4ea5ae61d45533def5fe209b92d44a37966c01fc590e3b494843facf3cf'

    def getKeyHash(self,challengeNumber):
        return self.contract.functions.getKeyHash(challengeNumber).call({'from': self.controlling_account_address})

    def getKeyHash_signature(self):
        return '0x15343c1149ad47c37dbec962979924a43a63d42c59fad3b76737b12c7b563ff1'

    def getLatestChallengeNumber(self):
        return self.contract.functions.getLatestChallengeNumber().call({'from': self.controlling_account_address})

    def getLatestChallengeNumber_signature(self):
        return '0x736d8c91fbb0b5468fa6d8be7585ac9ff8a9054fa82fb28c5a124c5305f4cc29'

    def getMessage(self,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.getMessage().buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def getMessage_signature(self):
        return '0xce6d41ded42f6d0a66dabb48cfad96ba3a4c556d343ed726c03045e45f7d8d50'

    def getOverallRewards(self,challengeNumber,participant):
        return self.contract.functions.getOverallRewards(challengeNumber,participant).call({'from': self.controlling_account_address})

    def getOverallRewards_signature(self):
        return '0x97d9abb8cec17e7363b2d299f5ae4ab69adcbf45b8b759d65dd1e522d6a8e04b'

    def getPhase(self,challengeNumber):
        return self.contract.functions.getPhase(challengeNumber).call({'from': self.controlling_account_address})

    def getPhase_signature(self):
        return '0xaf976fecef2c0e63b8d0c9384b1fb1dd75478aa8f49fdbdfe4985c6fab267635'

    def getPrivateKeyHash(self,challengeNumber):
        return self.contract.functions.getPrivateKeyHash(challengeNumber).call({'from': self.controlling_account_address})

    def getPrivateKeyHash_signature(self):
        return '0x4169293bcadd05765e9125224b01978d1ff30f8c407b36dbe081ed3e5153d5ef'

    def getRemainder(self):
        return self.contract.functions.getRemainder().call({'from': self.controlling_account_address})

    def getRemainder_signature(self):
        return '0xf109a6242d5380435de033d69aa037f946aa2d9d11d6e23ffca857576eb04b54'

    def getResultsHash(self,challengeNumber):
        return self.contract.functions.getResultsHash(challengeNumber).call({'from': self.controlling_account_address})

    def getResultsHash_signature(self):
        return '0xeecfc33fce50690f011acedbc51b64ecb793eabfbe07a82dfbd79d41ac932ed9'

    def getRewardsThreshold(self):
        return self.contract.functions.getRewardsThreshold().call({'from': self.controlling_account_address})

    def getRewardsThreshold_signature(self):
        return '0x18829fc3912d97dd763926a97f9d60ddaa1c52196043bffdf9da410407f929e8'

    def getRoleAdmin(self,role):
        return self.contract.functions.getRoleAdmin(role).call({'from': self.controlling_account_address})

    def getRoleAdmin_signature(self):
        return '0x248a9ca39e7e298ea3bbd193e7d36b87492efea84ff513fd03940aaa5bc0d98f'

    def getStake(self,participant):
        return self.contract.functions.getStake(participant).call({'from': self.controlling_account_address})

    def getStake_signature(self):
        return '0x7a7664602914e9220bf98c40cd78d8cd0036a1692fcc95af2bf47047bec10e22'

    def getStakeThreshold(self):
        return self.contract.functions.getStakeThreshold().call({'from': self.controlling_account_address})

    def getStakeThreshold_signature(self):
        return '0x343cb6be617b02f33dd798570aa4e64ad086c7a71bd0dc5ae441bc5136732f2d'

    def getStakedAmountForChallenge(self,challengeNumber,participant):
        return self.contract.functions.getStakedAmountForChallenge(challengeNumber,participant).call({'from': self.controlling_account_address})

    def getStakedAmountForChallenge_signature(self):
        return '0xe6184ab8c773b884df21d90dcb427f67cf5b6baad1b741191afbfcd0e4185695'

    def getStakingRewards(self,challengeNumber,participant):
        return self.contract.functions.getStakingRewards(challengeNumber,participant).call({'from': self.controlling_account_address})

    def getStakingRewards_signature(self):
        return '0x6c981570045e54484207c0ffd4f71d7c3d19c1963c65cb7c363bdeee45694a1e'

    def getSubmission(self,challengeNumber,participant):
        return self.contract.functions.getSubmission(challengeNumber,participant).call({'from': self.controlling_account_address})

    def getSubmission_signature(self):
        return '0x60cdb6cc07ec0d9ecc2a81c30124369f88e5271c6fc508ec2e5470ae60ca1abe'

    def getSubmissionCounter(self,challengeNumber):
        return self.contract.functions.getSubmissionCounter(challengeNumber).call({'from': self.controlling_account_address})

    def getSubmissionCounter_signature(self):
        return '0xc8f971df54214df825dba009c0ea0d4718d79c0b6ce98768a6f3430b114fa00d'

    def getSubmitters(self,challengeNumber,startIndex,endIndex):
        return self.contract.functions.getSubmitters(challengeNumber,startIndex,endIndex).call({'from': self.controlling_account_address})

    def getSubmitters_signature(self):
        return '0xe0bc9611b976f79bf4255505f92496c2be8fa5fc37a3b7f29a773de5cdce618d'

    def getTokenAddress(self):
        return self.contract.functions.getTokenAddress().call({'from': self.controlling_account_address})

    def getTokenAddress_signature(self):
        return '0x10fe9ae8450cc9747a16e2c97fe6ff3415bf382292603d127913b4087e08e2a7'

    def getTotalStakesLockedForChallenge(self,challengeNumber):
        return self.contract.functions.getTotalStakesLockedForChallenge(challengeNumber).call({'from': self.controlling_account_address})

    def getTotalStakesLockedForChallenge_signature(self):
        return '0x934d9012192701d48a93c50664d9835b098c3a094c4b537df41e8da0dcc02ac0'

    def getTournamentRewards(self,challengeNumber,participant):
        return self.contract.functions.getTournamentRewards(challengeNumber,participant).call({'from': self.controlling_account_address})

    def getTournamentRewards_signature(self):
        return '0xaa658b69fb869aa05a13a7f1d844d0c90be83898e513962827474d469bb80038'

    def getTournamentRewardsPercentageInWei(self):
        return self.contract.functions.getTournamentRewardsPercentageInWei().call({'from': self.controlling_account_address})

    def getTournamentRewardsPercentageInWei_signature(self):
        return '0x920920ba21e2abfae128f70e5b227dc2b86a07d21fbac0acaa975d20511b661c'

    def getTournamentScores(self,challengeNumber,participant):
        return self.contract.functions.getTournamentScores(challengeNumber,participant).call({'from': self.controlling_account_address})

    def getTournamentScores_signature(self):
        return '0x7a378430039bc48edbc4ce5c060e3e75cc8413a71b805eec0c7cb421499ca560'

    def grantRole(self,role,account,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.grantRole(role,account).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def grantRole_signature(self):
        return '0x2f2ff15deca029b64bbc0874ae59c8f39be024a95aa718b4c13ca407db350be8'

    def hasRole(self,role,account):
        return self.contract.functions.hasRole(role,account).call({'from': self.controlling_account_address})

    def hasRole_signature(self):
        return '0x91d1485424b278bc736d5d34907ed48280c7188845bc82b33370da2b4dc1194e'

    def increaseStake(self,staker,amountToken,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.increaseStake(staker,amountToken).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def increaseStake_signature(self):
        return '0x5d7e9467ee2ba0d5ad5863d1a906aaaccb100b31a17ebd2045e4d5ad1b36a6c6'

    def initialize(self,stakeThreshold_,rewardsThreshold_,tokenAddress_,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.initialize(stakeThreshold_,rewardsThreshold_,tokenAddress_).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def initialize_signature(self):
        return '0xa6ab36f2daf8836f3a53521075ec1a72cd6d9ac224c8a30540aee2f068f031a2'

    def moveRemainderToPool(self,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.moveRemainderToPool().buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def moveRemainderToPool_signature(self):
        return '0x37d6b9971a09ef4ae005f3f9643d00b69d9d0d2109e63890f1deb62a232378c4'

    def openChallenge(self,datasetHash,keyHash,submissionCloseDeadline,nextChallengeDeadline,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.openChallenge(datasetHash,keyHash,submissionCloseDeadline,nextChallengeDeadline).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def openChallenge_signature(self):
        return '0x1bd4f4c3623240194ef8af3c1a9ea72a396412483984a92169ce4a48e7a0dad2'

    def payRewards(self,challengeNumber,submitters,stakingRewards,challengeRewards,tournamentRewards,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.payRewards(challengeNumber,submitters,stakingRewards,challengeRewards,tournamentRewards).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def payRewards_signature(self):
        return '0xa5d9657790e80d0532e03297db9ace6c1d74239e7a71ed0422e56c31db2b8301'

    def payRewards(self,submitters,stakingRewards,challengeRewards,tournamentRewards,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.payRewards(submitters,stakingRewards,challengeRewards,tournamentRewards).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def payRewards_signature(self):
        return '0x343ae338a3f3a08c0c5da2c93d89479a551401708050f096d706b7d2c0b94be5'

    def payStakingRewards(self,challengeNumber,participants,rewards,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.payStakingRewards(challengeNumber,participants,rewards).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def payStakingRewards_signature(self):
        return '0xb2ad7d954c81428242be8ef9d7919def115a88d453bda1dc7e1298ae9187432f'

    def payStakingRewards(self,participants,rewards,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.payStakingRewards(participants,rewards).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def payStakingRewards_signature(self):
        return '0xd3d11c62a094afdc497edaa1aeb9f9c038922f477f2cbb6e6b4e0712740c9964'

    def renounceRole(self,role,account,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.renounceRole(role,account).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def renounceRole_signature(self):
        return '0x36568abe2c7e6c1d662bad0fe1760ac72cf2f9478a86be824d68ec83895c49e9'

    def revokeRole(self,role,account,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.revokeRole(role,account).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def revokeRole_signature(self):
        return '0xd547741fd8d55981251e167708119763c372f2b41e85a1468b0a759b055a009f'

    def sponsor(self,amountToken,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.sponsor(amountToken).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def sponsor_signature(self):
        return '0xb6cce5e2472d56a8309d36a7440d57cc5647ec73590def8772718ac12cde4d45'

    def submitNewPredictions(self,submissionHash,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.submitNewPredictions(submissionHash).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def submitNewPredictions_signature(self):
        return '0x9f2492a2bb4ac7d2220b3fe414349959f681b59a8853c1cc7c39ea3bf9a2faf9'

    def submitResults(self,resultsHash,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.submitResults(resultsHash).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def submitResults_signature(self):
        return '0x315c455e4ed50a5d1cac927ecf72c61242096a17aa464ef1bbd3791f1d1605fb'

    def supportsInterface(self,interfaceId):
        return self.contract.functions.supportsInterface(interfaceId).call({'from': self.controlling_account_address})

    def supportsInterface_signature(self):
        return '0x1ffc9a7a5cef8baa21ed3c5c0d7e23accb804b619e9333b597f47a0d84076e2'

    def updateChallengeAndTournamentScores(self,participants,challengeScores,tournamentScores,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.updateChallengeAndTournamentScores(participants,challengeScores,tournamentScores).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def updateChallengeRewardsPercentageInWei(self,newPercentage,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.updateChallengeRewardsPercentageInWei(newPercentage).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def updateChallengeRewardsPercentageInWei_signature(self):
        return '0x7bfc90b29e21e6e679bc3c85067962b92b59993548754944f0f870c79e342e9c'

    def updateDataset(self,oldDatasetHash,newDatasetHash,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.updateDataset(oldDatasetHash,newDatasetHash).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def updateDataset_signature(self):
        return '0x3f23091537c0236ed10021bcbb495f48bccbbdb4e5bd8712319d321fff122431'

    def updateDeadlines(self,challengeNumber,index,timestamp,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.updateDeadlines(challengeNumber,index,timestamp).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def updateDeadlines_signature(self):
        return '0x2d071f1a4c12cea8ceb62a22153b5aab02856e5a90f6f9ce7a906d39ad3c9c40'

    def updateInformationBatch(self,challengeNumber,participants,itemNumber,values,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.updateInformationBatch(challengeNumber,participants,itemNumber,values).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def updateInformationBatch_signature(self):
        return '0x50ab63e8b95c1dc05e7643983b4194b8e5f5b801537fc89954042380e202cfc4'

    def updateKey(self,oldKeyHash,newKeyHash,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.updateKey(oldKeyHash,newKeyHash).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def updateKey_signature(self):
        return '0x73af67456af5389848e42130a3c0e5c68bb95b63e978e5131ee9f3d90809dae9'

    def updateMessage(self,newMessage,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.updateMessage(newMessage).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def updateMessage_signature(self):
        return '0x1923be241274f10213e894f06e4bd7fae3abb965bd7d01e2d78998f3e474264e'

    def updatePrivateKey(self,challengeNumber,newKeyHash,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.updatePrivateKey(challengeNumber,newKeyHash).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def updatePrivateKey_signature(self):
        return '0x2881b528b1d3b6f3ff736e480ce6cd9af0f67354bc5be22402048d55f581abf'

    def updateResults(self,oldResultsHash,newResultsHash,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.updateResults(oldResultsHash,newResultsHash).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def updateResults_signature(self):
        return '0xc55e86b1df2a5e73b96977fc532565e29e42b6e497358bc86eb8115d81266283'

    def updateRewardsThreshold(self,newThreshold,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.updateRewardsThreshold(newThreshold).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def updateRewardsThreshold_signature(self):
        return '0x572c686ace241734c479e4aeeb0e376b256fcaad87126de7a9e0141e12783f70'

    def updateStakeThreshold(self,newStakeThreshold,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.updateStakeThreshold(newStakeThreshold).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def updateStakeThreshold_signature(self):
        return '0x5ef5332953c1293c50fc17bc527fe2e723e729e97d5b74a181b4a3070bd51ff1'

    def updateSubmission(self,oldSubmissionHash,newSubmissionHash,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.updateSubmission(oldSubmissionHash,newSubmissionHash).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def updateSubmission_signature(self):
        return '0xf7fb373d4f0f78a037f8fce6ba873536d542d26082f8c1548668700e748089df'

    def updateTournamentRewardsPercentageInWei(self,newPercentage,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.updateTournamentRewardsPercentageInWei(newPercentage).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def updateTournamentRewardsPercentageInWei_signature(self):
        return '0x5e35d4987a216d190e7a782fb096e5f9bffba1cf87784160d439395a0f1db198'

    def esInit(self):
        es = {}
        es['0x90fa17bb11fb41b369ce056a8d718bb44439a353f1e9646fcc59ebb502997d48'] = 'constructor()'
        es['0xdfc0e8d429222115bcdeae8834d5fbcecc360f743768fc2a9693a30a379999e9'] = 'BatchInformationUpdated(challengeNumber,itemNumber)'
        es['0x6fa7224843e16ab8c76a13b984cfcf54de67707a118bf52ce93e0e5be3589871'] = 'ChallengeAndTournamentScoresUpdated(challengeNumber)'
        es['0x9da6f4cd0f617f153c3ebc9840a08792cff9f0fd8c796ce09c5d2006f42da6d9'] = 'ChallengeOpened(challengeNumber)'
        es['0x94327140b3bb3bb989865fef53b345cd1ddd7991b30e3233137ab646448fbeb5'] = 'ChallengeRewardsPercentageInWeiUpdated(newPercentage)'
        es['0xb4ad7e2453c3c06a28c5cfe29a3067c6edde6eb03be4df2a461f9d806cb747e'] = 'DatasetUpdated(challengeNumber,oldDatasetHash,newDatasetHash)'
        es['0x7a2b6b0f48d13449d72d8fd2c1fae94cd13c970cc0dc738abd0bae8d50ce81c6'] = 'KeyUpdated(challengeNumber,oldKeyHash,newKeyHash)'
        es['0x89dbe1e8a053a391becc713b9c088b57cf1855cf857803e49eaae2f8fbc3b1cd'] = 'MessageUpdated()'
        es['0xda446d0471a795498335ed4bc219b34921a12ccb87136a9aa03964adc83eadf3'] = 'RemainderMovedToPool(remainder)'
        es['0xfb7d772905d44c5fdd59d4ab87c7f40281e09f93e2e189d03737c6d82b154ea'] = 'ResultsUpdated(challengeNumber,oldResultsHash,newResultsHash)'
        es['0x477dc5f7f393ee9f6c7e7723662b2b8baf8f4035f59afb91d507a48ced102414'] = 'RewardsPayment(submitter,stakingReward,challengeReward,tournamentReward)'
        es['0x73e002420a7defb91818836f9aaa83222b749a40c213c7c0fbccaacdd259e052'] = 'RewardsThresholdUpdated(newThreshold)'
        es['0xbd79b86ffe0ab8e8776151514217cd7cacd52c909f66475c3af44e129f0b00ff'] = 'RoleAdminChanged(role,previousAdminRole,newAdminRole)'
        es['0x2f8788117e7eff1d82e926ec794901d17c78024a50270940304540a733656f0d'] = 'RoleGranted(role,account,sender)'
        es['0xf6391f5c32d9c69d2a47ea670b442974b53935d1edc7fd64eb21e047a839171b'] = 'RoleRevoked(role,account,sender)'
        es['0x64939930c3fd0a1fe9e7fb9810272db7730a0f02b900972787bcb79fb6fd3d2d'] = 'Sponsor(sponsorAddress,sponsorAmount,poolTotal)'
        es['0x700865370ffb2a65a2b0242e6a64b21ac907ed5ecd46c9cffc729c177b2b1c69'] = 'StakeDecreased(sender,amount)'
        es['0x8b0ed825817a2e696c9a931715af4609fc60e1701f09c89ee7645130e937eb2d'] = 'StakeIncreased(sender,amount)'
        es['0xc3dad8d972694b8a948b4205b1bb45cbb2c73729f86630689e1e41c36a2965fa'] = 'StakeThresholdUpdated(newStakeThreshold,adminAddress)'
        es['0xc3168f2e7fdefcb5cb67cfb93778f32d4b25929f83d45e1bb44339f2161ba7f6'] = 'StakingRewardsPaid(challengeNumber,totalAmount)'
        es['0x6132076a840070359367c4279185181db454eae48a2c6c661e56f50ff312e044'] = 'StakingRewardsPayment(participant,rewardAmount)'
        es['0xaa5ebdc7900b87a79257aabbab219af255ada0be7148632ce5afcd622df7a88b'] = 'SubmissionClosed(challengeNumber)'
        es['0x953e3b79bb71898776bb2ef8bb919748c883b8b27c42e334de1ecdbf79d472bb'] = 'SubmissionUpdated(challengeNumber,participantAddress,newSubmissionHash)'
        es['0x17db0090e1a5606c55a062c8168003b4709555ded702adf58612ccfe1b5ef72f'] = 'TotalRewardsPaid(challengeNumber,totalStakingAmount,totalChallengeAmount,totalTournamentAmount)'
        es['0x211318e1b6942c96eaad65d5f6c4c520722236466093427de4dacb729bd36dfb'] = 'TournamentRewardsPercentageInWeiUpdated(newPercentage)'
        es['0xa217fddfde7807bb766525e432eeeecaaf4de889a05e8df9fb827257fb978cf4'] = 'DEFAULT_ADMIN_ROLE()'
        es['0x1442b868d2f8018bc8d42545315eaf4cc147c61478feb7c4bea741088bcc606b'] = 'RCI_CHILD_ADMIN()'
        es['0x18b125d1a509951ab885282b7714b08ed849768106e32e433beb7a704d7db908'] = 'RCI_MAIN_ADMIN()'
        es['0xdc9f76eb4d55e54402dae5449f850093d7e41ddb03c19f12d69a643e0a89022c'] = 'advanceToPhase(phase)'
        es['0xffc6ff1e03e42248bd1fd91651f00e0eb1e056ac28afdea1e97d34f042b5c529'] = 'closeSubmission()'
        es['0x7bf68a3b82a86385ff13524f44456cf0d04ffa386b8c71b9ea831f78d2e246c7'] = 'computeStakingReward(participant)'
        es['0x1a73ba01d85313ec153146459d5a578e6ae7f7a19820500a07d9dd9a991bbf7c'] = 'decreaseStake(staker,amountToken)'
        es['0x3cbcb53a83939614eec6464f798d4426b0aba4e4d98e55fc71dce1cc11b2dcf6'] = 'getChallengeRewards(challengeNumber,participant)'
        es['0x93a9dac7868cff88be6ba5997079d258233bec6725d7f81995e1905b845eba2d'] = 'getChallengeRewardsPercentageInWei()'
        es['0xd885e39b3794407d7aaa59c1c6b4d4cd93f9d66577501462bc3e219cc53a5935'] = 'getChallengeScores(challengeNumber,participant)'
        es['0xd4f4b806e153ce83a6a91553e5334f659253f310b3a1161e27ec63de0a0169c5'] = 'getCompetitionPool()'
        es['0xd68a7c00c2e3d4a313dbc5be88fccf14dae6c1c667192e3b3f64388bfcd90f7d'] = 'getCurrentChallengeRewardsBudget()'
        es['0x1e2ff711835ce68e3e4c25895511dd039c8d7f79b7f94f657bbd08441d22586e'] = 'getCurrentStakingRewardsBudget()'
        es['0x25b067461fadf3c0cb8169ec223a9964320845d428e65fa1474f4123ce3d8c5d'] = 'getCurrentTotalStaked()'
        es['0x3228cf728085e656303b783c5248ed82c37eb2354d6015f1f1fc5d998fa7d1ef'] = 'getCurrentTournamentRewardsBudget()'
        es['0x39e287774455340b77e7c4f62dc30977c7fadb0169f3f8b40fc253216cc59cfa'] = 'getDatasetHash(challengeNumber)'
        es['0x57d0cf586665801895da5830ec1daa9cf22202c7d0bd27df16b1ba8da8e32d19'] = 'getDeadlines(challengeNumber,index)'
        es['0xe7d5c4ea5ae61d45533def5fe209b92d44a37966c01fc590e3b494843facf3cf'] = 'getInformation(challengeNumber,participant,itemNumber)'
        es['0x15343c1149ad47c37dbec962979924a43a63d42c59fad3b76737b12c7b563ff1'] = 'getKeyHash(challengeNumber)'
        es['0x736d8c91fbb0b5468fa6d8be7585ac9ff8a9054fa82fb28c5a124c5305f4cc29'] = 'getLatestChallengeNumber()'
        es['0xce6d41ded42f6d0a66dabb48cfad96ba3a4c556d343ed726c03045e45f7d8d50'] = 'getMessage()'
        es['0x97d9abb8cec17e7363b2d299f5ae4ab69adcbf45b8b759d65dd1e522d6a8e04b'] = 'getOverallRewards(challengeNumber,participant)'
        es['0xaf976fecef2c0e63b8d0c9384b1fb1dd75478aa8f49fdbdfe4985c6fab267635'] = 'getPhase(challengeNumber)'
        es['0x4169293bcadd05765e9125224b01978d1ff30f8c407b36dbe081ed3e5153d5ef'] = 'getPrivateKeyHash(challengeNumber)'
        es['0xf109a6242d5380435de033d69aa037f946aa2d9d11d6e23ffca857576eb04b54'] = 'getRemainder()'
        es['0xeecfc33fce50690f011acedbc51b64ecb793eabfbe07a82dfbd79d41ac932ed9'] = 'getResultsHash(challengeNumber)'
        es['0x18829fc3912d97dd763926a97f9d60ddaa1c52196043bffdf9da410407f929e8'] = 'getRewardsThreshold()'
        es['0x248a9ca39e7e298ea3bbd193e7d36b87492efea84ff513fd03940aaa5bc0d98f'] = 'getRoleAdmin(role)'
        es['0x7a7664602914e9220bf98c40cd78d8cd0036a1692fcc95af2bf47047bec10e22'] = 'getStake(participant)'
        es['0x343cb6be617b02f33dd798570aa4e64ad086c7a71bd0dc5ae441bc5136732f2d'] = 'getStakeThreshold()'
        es['0xe6184ab8c773b884df21d90dcb427f67cf5b6baad1b741191afbfcd0e4185695'] = 'getStakedAmountForChallenge(challengeNumber,participant)'
        es['0x6c981570045e54484207c0ffd4f71d7c3d19c1963c65cb7c363bdeee45694a1e'] = 'getStakingRewards(challengeNumber,participant)'
        es['0x60cdb6cc07ec0d9ecc2a81c30124369f88e5271c6fc508ec2e5470ae60ca1abe'] = 'getSubmission(challengeNumber,participant)'
        es['0xc8f971df54214df825dba009c0ea0d4718d79c0b6ce98768a6f3430b114fa00d'] = 'getSubmissionCounter(challengeNumber)'
        es['0xe0bc9611b976f79bf4255505f92496c2be8fa5fc37a3b7f29a773de5cdce618d'] = 'getSubmitters(challengeNumber,startIndex,endIndex)'
        es['0x10fe9ae8450cc9747a16e2c97fe6ff3415bf382292603d127913b4087e08e2a7'] = 'getTokenAddress()'
        es['0x934d9012192701d48a93c50664d9835b098c3a094c4b537df41e8da0dcc02ac0'] = 'getTotalStakesLockedForChallenge(challengeNumber)'
        es['0xaa658b69fb869aa05a13a7f1d844d0c90be83898e513962827474d469bb80038'] = 'getTournamentRewards(challengeNumber,participant)'
        es['0x920920ba21e2abfae128f70e5b227dc2b86a07d21fbac0acaa975d20511b661c'] = 'getTournamentRewardsPercentageInWei()'
        es['0x7a378430039bc48edbc4ce5c060e3e75cc8413a71b805eec0c7cb421499ca560'] = 'getTournamentScores(challengeNumber,participant)'
        es['0x2f2ff15deca029b64bbc0874ae59c8f39be024a95aa718b4c13ca407db350be8'] = 'grantRole(role,account)'
        es['0x91d1485424b278bc736d5d34907ed48280c7188845bc82b33370da2b4dc1194e'] = 'hasRole(role,account)'
        es['0x5d7e9467ee2ba0d5ad5863d1a906aaaccb100b31a17ebd2045e4d5ad1b36a6c6'] = 'increaseStake(staker,amountToken)'
        es['0xa6ab36f2daf8836f3a53521075ec1a72cd6d9ac224c8a30540aee2f068f031a2'] = 'initialize(stakeThreshold_,rewardsThreshold_,tokenAddress_)'
        es['0x37d6b9971a09ef4ae005f3f9643d00b69d9d0d2109e63890f1deb62a232378c4'] = 'moveRemainderToPool()'
        es['0x1bd4f4c3623240194ef8af3c1a9ea72a396412483984a92169ce4a48e7a0dad2'] = 'openChallenge(datasetHash,keyHash,submissionCloseDeadline,nextChallengeDeadline)'
        es['0xa5d9657790e80d0532e03297db9ace6c1d74239e7a71ed0422e56c31db2b8301'] = 'payRewards(challengeNumber,submitters,stakingRewards,challengeRewards,tournamentRewards)'
        es['0x343ae338a3f3a08c0c5da2c93d89479a551401708050f096d706b7d2c0b94be5'] = 'payRewards(submitters,stakingRewards,challengeRewards,tournamentRewards)'
        es['0xb2ad7d954c81428242be8ef9d7919def115a88d453bda1dc7e1298ae9187432f'] = 'payStakingRewards(challengeNumber,participants,rewards)'
        es['0xd3d11c62a094afdc497edaa1aeb9f9c038922f477f2cbb6e6b4e0712740c9964'] = 'payStakingRewards(participants,rewards)'
        es['0x36568abe2c7e6c1d662bad0fe1760ac72cf2f9478a86be824d68ec83895c49e9'] = 'renounceRole(role,account)'
        es['0xd547741fd8d55981251e167708119763c372f2b41e85a1468b0a759b055a009f'] = 'revokeRole(role,account)'
        es['0xb6cce5e2472d56a8309d36a7440d57cc5647ec73590def8772718ac12cde4d45'] = 'sponsor(amountToken)'
        es['0x9f2492a2bb4ac7d2220b3fe414349959f681b59a8853c1cc7c39ea3bf9a2faf9'] = 'submitNewPredictions(submissionHash)'
        es['0x315c455e4ed50a5d1cac927ecf72c61242096a17aa464ef1bbd3791f1d1605fb'] = 'submitResults(resultsHash)'
        es['0x1ffc9a7a5cef8baa21ed3c5c0d7e23accb804b619e9333b597f47a0d84076e2'] = 'supportsInterface(interfaceId)'
        es['0x97a9ff39599e0a0521850c21e1c705c83584a92b7ef8abed6e0da4ab9d48a449'] = 'updateChallengeAndTournamentScores(participants,challengeScores,tournamentScores)'
        es['0xb627fc85cf21ed7af4a234deb231699bba3034c736397a7775dd03c0e860f091'] = 'updateChallengeAndTournamentScores(challengeNumber,participants,challengeScores,tournamentScores)'
        es['0x7bfc90b29e21e6e679bc3c85067962b92b59993548754944f0f870c79e342e9c'] = 'updateChallengeRewardsPercentageInWei(newPercentage)'
        es['0x3f23091537c0236ed10021bcbb495f48bccbbdb4e5bd8712319d321fff122431'] = 'updateDataset(oldDatasetHash,newDatasetHash)'
        es['0x2d071f1a4c12cea8ceb62a22153b5aab02856e5a90f6f9ce7a906d39ad3c9c40'] = 'updateDeadlines(challengeNumber,index,timestamp)'
        es['0x50ab63e8b95c1dc05e7643983b4194b8e5f5b801537fc89954042380e202cfc4'] = 'updateInformationBatch(challengeNumber,participants,itemNumber,values)'
        es['0x73af67456af5389848e42130a3c0e5c68bb95b63e978e5131ee9f3d90809dae9'] = 'updateKey(oldKeyHash,newKeyHash)'
        es['0x1923be241274f10213e894f06e4bd7fae3abb965bd7d01e2d78998f3e474264e'] = 'updateMessage(newMessage)'
        es['0x2881b528b1d3b6f3ff736e480ce6cd9af0f67354bc5be22402048d55f581abf'] = 'updatePrivateKey(challengeNumber,newKeyHash)'
        es['0xc55e86b1df2a5e73b96977fc532565e29e42b6e497358bc86eb8115d81266283'] = 'updateResults(oldResultsHash,newResultsHash)'
        es['0x572c686ace241734c479e4aeeb0e376b256fcaad87126de7a9e0141e12783f70'] = 'updateRewardsThreshold(newThreshold)'
        es['0x5ef5332953c1293c50fc17bc527fe2e723e729e97d5b74a181b4a3070bd51ff1'] = 'updateStakeThreshold(newStakeThreshold)'
        es['0xf7fb373d4f0f78a037f8fce6ba873536d542d26082f8c1548668700e748089df'] = 'updateSubmission(oldSubmissionHash,newSubmissionHash)'
        es['0x5e35d4987a216d190e7a782fb096e5f9bffba1cf87784160d439395a0f1db198'] = 'updateTournamentRewardsPercentageInWei(newPercentage)'
        return es

    def address(self):
        return self.contract.address
        
    def getEventNameFromSig(self, hash):
        return self.eventSignatureToName[hash]