from src.rci_competition_utilities.utilities.Competition import Competition
from src.rci_competition_utilities.utilities.Token import Token
from src.rci_competition_utilities.utilities.rci_utilities import *


class Participant:
    def __init__(self, read_only, network_url, infura_id, account_address):

        w3 = connect(ip=network_url, port=None, infuraID=infura_id)
        if not read_only:
            PRIVATE_KEY = input(
                'Please paste your private key here and press "Enter". Your private key is a 32-byte hexadecimal string.\nPlease keep your private key secure and store it somewhere safe.\n')
            if PRIVATE_KEY[:2] == '0x': PRIVATE_KEY = PRIVATE_KEY[2:]
            this_account = w3.eth.account.from_key(PRIVATE_KEY)
            assert this_account.address == account_address, 'Private key does not match account {}.'.format(
                account_address)
        else:
            this_account = account_address
        self.w3 = w3
        self.this_account = this_account
        self.set_gas_price_in_gwei()
        self.verbose = True

    def set_gas_price_in_gwei(self, gas_price_in_gwei = 1):
        self.my_gas_price_in_wei = int(gas_price_in_gwei) * int(1e9)

    def conversion_to_uint(self, amount):
        return token_float_to_uint(amount, self.token)

    def conversion_to_float(self, amount):
        return token_uint_to_float(amount, self.token)

    # Instantiate an existing token contract.
    def token_init(self, token_contract_address):
        token = Token('contracts/Token.json', self.w3, token_contract_address, self.this_account, self.verbose)
        self.token = token
        
    # Instantiate an existing competition contract.
    def competition_init(self, competition_contract_address):
        competition = Competition('contracts/Competition.json', self.w3, competition_contract_address, self.this_account, self.verbose)
        self.competition = competition

    def grant_permission(self):
        self.token.grantPermission(self.competition.address(), gas_price_in_wei=self.my_gas_price_in_wei)

    def set_stake(self, amount_in_float):
        self.competition.setStake(token_float_to_uint(amount_in_float, self.token), gas_price_in_wei=self.my_gas_price_in_wei)
        
    def increase_stake(self, amount_in_float):
        self.competition.increaseStake(token_float_to_uint(amount_in_float, self.token), gas_price_in_wei=self.my_gas_price_in_wei)
        
    def decrease_stake(self, amount_in_float):
        self.competition.decreaseStake(token_float_to_uint(amount_in_float, self.token), gas_price_in_wei=self.my_gas_price_in_wei)
        
    def transfer_stake(self, recipient, amount_in_float):
        self.competition.transferStake(recipient ,token_float_to_uint(amount_in_float, self.token), gas_price_in_wei=self.my_gas_price_in_wei)

    def transfer_my_personal_token_balance(self, recipient, amount_in_float):
        self.token.transfer(recipient, token_float_to_uint(amount_in_float, self.token), gas_price_in_wei=self.my_gas_price_in_wei)

    def retrieve_dataset(self, challenge_number, destination_folder = 'retrieved_dataset'):
        dataset_cid = self.get_dataset_cid(challenge_number)
        if dataset_cid != None:
            retrieve_file(dataset_cid, destination_folder+'.zip')
            unzip_dir(destination_folder+'.zip', destination_folder)

    def retrieve_results(self, challenge_number, destination_file = 'retrieved_results'):
        results_cid = self.get_result_cid(challenge_number)
        if results_cid != None:
            retrieve_file(results_cid, destination_file + '.csv')

    def upload_submission(self, submission_file_path, zip_folder_name, challenge_number):
        # TODO: read a submission csv file and checks the number of rows and columns

        # Generate a symmetric key
        key = get_random_bytes(16)

        # Encrypt submission file
        encrypted_file_path, symmetric_key_file = encrypt_file(submission_file_path, key=key)

        # Create and encrypt originator address file.
        try:
            address = self.this_account.address
        except:
            address = self.this_account
        enc_originator_path, placeholder = encrypt_file('originator', key=key, data=address)

        if challenge_number is None:
            challenge_number = self.get_latest_challenge_number()

        key_cid = hash_to_cid(self.competition.getKeyHash(challenge_number).hex())
        pub_key = retrieve_file(key_cid)

        # Encrypt symmetric key using RCI public key
        encrypted_participant_key_path = encrypt_participant_key(pub_key, symmetric_key_file)

        # Create folder for zipping
        dir_path = os.path.join(os.getcwd(), zip_folder_name)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.mkdir(zip_folder_name)

        # Move files into folder for zipping
        filename = encrypted_file_path.split('/')
        if len(filename) > 1: filename = filename[-1]
        copy_file(encrypted_file_path, zip_folder_name + '//' + filename)

        copy_file(enc_originator_path, zip_folder_name + '//' + 'originator.bin')

        filename = encrypted_participant_key_path.split('/')
        if len(filename) > 1: filename = filename[-1]
        copy_file(encrypted_participant_key_path, zip_folder_name + '//' + filename)

        # Zip folder
        zip_file(zip_folder_name)

        # Put on IPFS
        submission_cid = pin_file_to_ipfs(zip_folder_name + '.zip')

        return submission_cid

    def send_submission(self, submission_file_path, zip_folder_name, challenge_number=None):
        submission_cid = self.upload_submission(submission_file_path, zip_folder_name, challenge_number)
        self.competition.submitNewPredictions(cid_to_hash(submission_cid), gas_price_in_wei = self.my_gas_price_in_wei)
        return submission_cid

    def update_submission(self, submission_file_path, rci_public_key_path, zip_folder_name, old_submission_cid):
        new_submission_cid = self.upload_submission(submission_file_path, rci_public_key_path, zip_folder_name)
        self.competition.updateSubmission(cid_to_hash(old_submission_cid), cid_to_hash(new_submission_cid), gas_price_in_wei = self.my_gas_price_in_wei)
        return new_submission_cid

    # functions for reading information from the Tournament contract
    def get_current_gas_price_in_wei(self):
        return self.w3.eth.gas_price

    def get_stake(self):
        integer_amount = self.competition.getStake(self.token.controlling_account_address)
        return token_uint_to_float(integer_amount, self.token)

    def get_my_personal_token_balance(self):
        return token_uint_to_float(self.token.balanceOf(self.token.controlling_account_address), self.token)

    def get_my_ETH_balance(self):
        return self.w3.fromWei(self.w3.eth.get_balance(self.token.controlling_account_address),'ether')

    def get_my_submission_cid(self, challenge_number):
        return hash_to_cid(self.competition.getSubmission(challenge_number, self.token.controlling_account_address).hex())

    def get_latest_challenge_number(self):
        return self.competition.getLatestChallengeNumber()

    def get_competition_pool(self):
        return token_uint_to_float(self.competition.getCompetitionPool(), self.token)

    def get_dataset_cid(self, challenge_number):
        dataset_hash = self.competition.getDatasetHash(challenge_number).hex()
        if int(dataset_hash, 16) == 0 or int(dataset_hash, 16) == 1:
            print('Dataset for phase {} not found.'.format(challenge_number))
            return None
        else:
            return hash_to_cid(dataset_hash)

    def get_result_cid(self, challenge_number):
        results_hash = self.competition.getResultsHash()(challenge_number).hex()
        if int(results_hash, 16) == 0 or int(results_hash, 16) == 1:
            print('Results for phase {} not found.'.format(challenge_number))
            return None
        else:
            return hash_to_cid(results_hash)

    def create_dataset(self):
        return create_dataset()

if __name__ == '__main__':

    # # Set to `True` if only querying the blockchain for information.
    # READ_ONLY = False
    #
    # # Enter Infura Project ID here.
    # INFURA_ID = ''
    #
    # # Your account address.
    # PUBLIC_ADDRESS1 = ''
    # ''
    #
    # PUBLIC_ADDRESS2 = ''
    # ''
    #
    # # Instantiate Organizer session. You will be prompted for your private key if `READ_ONLY` is set to False.
    # my_account1 = Participant(read_only=READ_ONLY, network_url=network.polygon_mainnet, infura_id=INFURA_ID,
    #                        account_address=PUBLIC_ADDRESS1)
    # my_account2 = Participant(read_only=READ_ONLY, network_url=network.polygon_mainnet, infura_id=INFURA_ID,
    #                          account_address=PUBLIC_ADDRESS2)
    #
    # # # POLYGON contracts
    # # # Instantiate existing contracts
    #
    # # TOKEN
    # TOKEN_CONTRACT_ADDRESS = '0x38036bbF1e95957aB04CFd47708c5ca293916FFe'
    # my_account1.token_init(TOKEN_CONTRACT_ADDRESS)
    # my_account2.token_init(TOKEN_CONTRACT_ADDRESS)
    #
    # # # COMPETITON
    # COMPETITON_NAME = 'RCI_COMP_5'
    # COMPETITON_CONTRACT_ADDRESS = '0xe4AA9385BC3377b286a83861A860b990882a21aA'
    # my_account1.competition_init(COMPETITON_CONTRACT_ADDRESS)
    # my_account2.competition_init(COMPETITON_CONTRACT_ADDRESS)
    #
    # market_gas_price_in_gwei = my_account1.conversion_to_float(my_account1.get_current_gas_price_in_wei()) * 1e9
    # print('Market gas price: {:.2f} Gwei'.format(market_gas_price_in_gwei))
    #
    # # Set slightly higher for faster transactions
    # market_gas_price_in_gwei *= 1.8
    #
    # my_account1.set_gas_price_in_gwei(market_gas_price_in_gwei)
    # my_account2.set_gas_price_in_gwei(market_gas_price_in_gwei)
    # #
    # # my_account1.token.grantPermission(my_account1.competition.address())  # only needs to be run once.
    # # my_account1.competition.setStake(token_float_to_uint(30, my_account1.token))
    # # my_account2.token.grantPermission(my_account2.competition.address())  # only needs to be run once.
    # # my_account2.competition.setStake(token_float_to_uint(60, my_account2.token))
    # # print(my_account1.get_stake())
    # # print(my_account2.get_stake())
    # # my_account1.retrieve_dataset(1)
    # # #
    # file = ''
    # #
    # my_account1.send_submission(file, 'participant1_test_submit')
    # my_account2.send_submission(file, 'participant2_test_submit')



