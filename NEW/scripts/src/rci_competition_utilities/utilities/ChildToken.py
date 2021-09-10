class ChildToken:
    def __init__(self, json_path, w3, address, controlling_account, verbose=True, deploy=False, deploy_args_list = [], gas_price_in_wei=None) :       
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
            print('Deploying ChildToken Contract.')
            address = w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval).contractAddress
            print('ChildToken Contract deployed at {}.'.format(address))

        self.w3 = w3
        self.contract = contract(address=address)
        if type(controlling_account) is str:
            self.controlling_account_address = controlling_account
        else:
            self.controlling_account_address = controlling_account.address
        self.controlling_account = controlling_account
        self.verbose = verbose
        self.eventSignatureToName = self.esInit()  

    def constructor(self,name,symbol,childChainManagerProxy_,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.constructor(name,symbol,childChainManagerProxy_).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def constructor_signature(self):
        return '0x21d5dae3d99a6178d3e07301a315a074f34716ef2e60f4f1fd62683286038bf1'

    def Approval(self,owner,spender,value,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.Approval(owner,spender,value).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def Approval_signature(self):
        return '0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925'

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

    def Transfer(self,from_,to,value,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.Transfer(from_,to,value).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def Transfer_signature(self):
        return '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'

    def DEFAULT_ADMIN_ROLE(self):
        return self.contract.functions.DEFAULT_ADMIN_ROLE().call({'from': self.controlling_account_address})

    def DEFAULT_ADMIN_ROLE_signature(self):
        return '0xa217fddfde7807bb766525e432eeeecaaf4de889a05e8df9fb827257fb978cf4'

    def allowance(self,owner,spender):
        return self.contract.functions.allowance(owner,spender).call({'from': self.controlling_account_address})

    def allowance_signature(self):
        return '0xdd62ed3e90e97b3d417db9c0c7522647811bafca5afc6694f143588d255fdfb4'

    def approve(self,spender,amount,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.approve(spender,amount).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def approve_signature(self):
        return '0x95ea7b334ae44009aa867bfb386f5c3b4b443ac6f0ee573fa91c4608fbadfba'

    def balanceOf(self,account):
        return self.contract.functions.balanceOf(account).call({'from': self.controlling_account_address})

    def balanceOf_signature(self):
        return '0x70a08231b98ef4ca268c9cc3f6b4590e4bfec28280db06bb5d45e689f2a360be'

    def burn(self,amount,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.burn(amount).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def burn_signature(self):
        return '0x42966c689b5afe9b9b3f8a7103b2a19980d59629bfd6a20a60972312ed41d836'

    def burnFrom(self,account,amount,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.burnFrom(account,amount).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def burnFrom_signature(self):
        return '0x79cc679044ee9a2021f0a26c0fdec02ac39179cd005bb971a471b7f9f17c576c'

    def childChainManagerProxy(self):
        return self.contract.functions.childChainManagerProxy().call({'from': self.controlling_account_address})

    def childChainManagerProxy_signature(self):
        return '0x62f629e7ccb5d92e301172f3d06a9a34ea9e8e73615c13123862dd5b3f05324a'

    def decimals(self):
        return self.contract.functions.decimals().call({'from': self.controlling_account_address})

    def decimals_signature(self):
        return '0x313ce567add4d438edf58b94ff345d7d38c45b17dfc0f947988d7819dca364f9'

    def decreaseAllowance(self,spender,subtractedValue,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.decreaseAllowance(spender,subtractedValue).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def decreaseAllowance_signature(self):
        return '0xa457c2d77307f80ff2f3ac810ec99eb18ae2cffee13b29c90c9324546e374be5'

    def deposit(self,user,depositData,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.deposit(user,depositData).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def deposit_signature(self):
        return '0xcf2c52cb270523401b1315843d96c82d4615f4cde181c7c487b55d8568ed7300'

    def getRoleAdmin(self,role):
        return self.contract.functions.getRoleAdmin(role).call({'from': self.controlling_account_address})

    def getRoleAdmin_signature(self):
        return '0x248a9ca39e7e298ea3bbd193e7d36b87492efea84ff513fd03940aaa5bc0d98f'

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

    def increaseAllowance(self,spender,addedValue,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.increaseAllowance(spender,addedValue).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def increaseAllowance_signature(self):
        return '0x39509351d3325647dde3fdd3c8b249adfe89ef4f16d76d83768e6df7a5cd81d6'

    def name(self):
        return self.contract.functions.name().call({'from': self.controlling_account_address})

    def name_signature(self):
        return '0x6fdde0383f15d582d1a74511486c9ddf862a882fb7904b3d9fe9b8b8e58a796'

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

    def supportsInterface(self,interfaceId):
        return self.contract.functions.supportsInterface(interfaceId).call({'from': self.controlling_account_address})

    def supportsInterface_signature(self):
        return '0x1ffc9a7a5cef8baa21ed3c5c0d7e23accb804b619e9333b597f47a0d84076e2'

    def symbol(self):
        return self.contract.functions.symbol().call({'from': self.controlling_account_address})

    def symbol_signature(self):
        return '0x95d89b41e2f5f391a79ec54e9d87c79d6e777c63e32c28da95b4e9e4a79250ec'

    def totalSupply(self):
        return self.contract.functions.totalSupply().call({'from': self.controlling_account_address})

    def totalSupply_signature(self):
        return '0x18160ddd7f15c72528c2f94fd8dfe3c8d5aa26e2c50c7d81f4bc7bee8d4b7932'

    def transfer(self,recipient,amount,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.transfer(recipient,amount).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def transfer_signature(self):
        return '0xa9059cbb2ab09eb219583f4a59a5d0623ade346d962bcd4e46b11da047c9049b'

    def transferFrom(self,sender,recipient,amount,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.transferFrom(sender,recipient,amount).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def transferFrom_signature(self):
        return '0x23b872dd7302113369cda2901243429419bec145408fa8b352b3dd92b66c680b'

    def updateChildChainManager(self,newChildChainManagerProxy,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.updateChildChainManager(newChildChainManagerProxy).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def updateChildChainManager_signature(self):
        return '0x445a67971437e7c65d6ea27e3618123e50b67f03b9998e9ba5a572d7a68b3b62'

    def withdraw(self,amount,gas_price_in_wei=None):
        if gas_price_in_wei==None: gas_price_in_wei = self.w3.eth.gas_price
        tx_data = self.contract.functions.withdraw(amount).buildTransaction({'from': self.controlling_account_address, 'gasPrice': int(gas_price_in_wei), 'nonce': self.w3.eth.getTransactionCount(self.controlling_account_address)})
        signed_tx = self.w3.eth.account.sign_transaction(tx_data, self.controlling_account.privateKey)
        tx_id = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction, self.timeout, self.interval)
        if self.verbose: print('Sending transaction {}'.format(tx_id.hex()))
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_id, self.timeout, self.interval)
        if self.verbose: print('Transaction sent. Tx ID: {}'.format(tx_id.hex()))
        return tx_receipt

    def withdraw_signature(self):
        return '0x2e1a7d4d13322e7b96f9a57413e1525c250fb7a9021cf91d1540d5b69f16a49f'

    def esInit(self):
        es = {}
        es['0x21d5dae3d99a6178d3e07301a315a074f34716ef2e60f4f1fd62683286038bf1'] = 'constructor(name,symbol,childChainManagerProxy_)'
        es['0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925'] = 'Approval(owner,spender,value)'
        es['0xbd79b86ffe0ab8e8776151514217cd7cacd52c909f66475c3af44e129f0b00ff'] = 'RoleAdminChanged(role,previousAdminRole,newAdminRole)'
        es['0x2f8788117e7eff1d82e926ec794901d17c78024a50270940304540a733656f0d'] = 'RoleGranted(role,account,sender)'
        es['0xf6391f5c32d9c69d2a47ea670b442974b53935d1edc7fd64eb21e047a839171b'] = 'RoleRevoked(role,account,sender)'
        es['0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'] = 'Transfer(from_,to,value)'
        es['0xa217fddfde7807bb766525e432eeeecaaf4de889a05e8df9fb827257fb978cf4'] = 'DEFAULT_ADMIN_ROLE()'
        es['0xdd62ed3e90e97b3d417db9c0c7522647811bafca5afc6694f143588d255fdfb4'] = 'allowance(owner,spender)'
        es['0x95ea7b334ae44009aa867bfb386f5c3b4b443ac6f0ee573fa91c4608fbadfba'] = 'approve(spender,amount)'
        es['0x70a08231b98ef4ca268c9cc3f6b4590e4bfec28280db06bb5d45e689f2a360be'] = 'balanceOf(account)'
        es['0x62f629e7ccb5d92e301172f3d06a9a34ea9e8e73615c13123862dd5b3f05324a'] = 'childChainManagerProxy()'
        es['0x313ce567add4d438edf58b94ff345d7d38c45b17dfc0f947988d7819dca364f9'] = 'decimals()'
        es['0xa457c2d77307f80ff2f3ac810ec99eb18ae2cffee13b29c90c9324546e374be5'] = 'decreaseAllowance(spender,subtractedValue)'
        es['0xcf2c52cb270523401b1315843d96c82d4615f4cde181c7c487b55d8568ed7300'] = 'deposit(user,depositData)'
        es['0x248a9ca39e7e298ea3bbd193e7d36b87492efea84ff513fd03940aaa5bc0d98f'] = 'getRoleAdmin(role)'
        es['0x2f2ff15deca029b64bbc0874ae59c8f39be024a95aa718b4c13ca407db350be8'] = 'grantRole(role,account)'
        es['0x91d1485424b278bc736d5d34907ed48280c7188845bc82b33370da2b4dc1194e'] = 'hasRole(role,account)'
        es['0x39509351d3325647dde3fdd3c8b249adfe89ef4f16d76d83768e6df7a5cd81d6'] = 'increaseAllowance(spender,addedValue)'
        es['0x6fdde0383f15d582d1a74511486c9ddf862a882fb7904b3d9fe9b8b8e58a796'] = 'name()'
        es['0x36568abe2c7e6c1d662bad0fe1760ac72cf2f9478a86be824d68ec83895c49e9'] = 'renounceRole(role,account)'
        es['0xd547741fd8d55981251e167708119763c372f2b41e85a1468b0a759b055a009f'] = 'revokeRole(role,account)'
        es['0x1ffc9a7a5cef8baa21ed3c5c0d7e23accb804b619e9333b597f47a0d84076e2'] = 'supportsInterface(interfaceId)'
        es['0x95d89b41e2f5f391a79ec54e9d87c79d6e777c63e32c28da95b4e9e4a79250ec'] = 'symbol()'
        es['0x18160ddd7f15c72528c2f94fd8dfe3c8d5aa26e2c50c7d81f4bc7bee8d4b7932'] = 'totalSupply()'
        es['0xa9059cbb2ab09eb219583f4a59a5d0623ade346d962bcd4e46b11da047c9049b'] = 'transfer(recipient,amount)'
        es['0x23b872dd7302113369cda2901243429419bec145408fa8b352b3dd92b66c680b'] = 'transferFrom(sender,recipient,amount)'
        es['0x445a67971437e7c65d6ea27e3618123e50b67f03b9998e9ba5a572d7a68b3b62'] = 'updateChildChainManager(newChildChainManagerProxy)'
        es['0x2e1a7d4d13322e7b96f9a57413e1525c250fb7a9021cf91d1540d5b69f16a49f'] = 'withdraw(amount)'
        return es

    def address(self):
        return self.contract.address
        
    def getEventNameFromSig(self, hash):
        return self.eventSignatureToName[hash]