from src.rci_competition_utilities.utilities.MultiSig import MultiSig
from src.rci_competition_utilities.utilities.rci_utilities import *
from src.rci_competition_utilities.utilities.Token import Token
from src.rci_competition_utilities.utilities.Competition import Competition
from src.rci_competition_utilities.utilities.Registry import Registry
from src.rci_competition_utilities.utilities.Vault import Vault
from src.rci_competition_utilities.utilities.ProxyAdmin import ProxyAdmin
from src.rci_competition_utilities.utilities.TransparentUpgradeableProxy import  TransparentUpgradeableProxy
from src.rci_competition_utilities.utilities.OldCompetition import OldCompetition


CHILD_CHAIN_MANAGER_PROXY = '0xb5505a6d998549090530911180f38aC5130101c6'


class Organizer:
    def __init__(self, read_only, network_url, infura_id, account_address):

        w3 = connect(ip=network_url, port=None, infuraID=infura_id)
        if not read_only:
            PRIVATE_KEY = input(
                'Please paste your private key here and press "Enter". Your private key is a 32-byte hexadecimal string.\nPlease keep your private key secure and store it somewhere safe.\n')
            if PRIVATE_KEY[:2] == '0x':
                PRIVATE_KEY = PRIVATE_KEY[2:]
            this_account = w3.eth.account.from_key(PRIVATE_KEY)
            assert this_account.address == account_address, 'Private key does not match account {}.'.format(
                account_address)
        else:
            this_account = account_address
        self.w3 = w3
        self.this_account = this_account
        self.set_gas_price_in_gwei()
        self.verbose = True

    def conversion_to_uint(self, amount):
        return token_float_to_uint(amount, self.token)

    def conversion_to_float(self, amount):
        return token_uint_to_float(amount, self.token)

    def set_gas_price_in_gwei(self, gas_price_in_gwei = 1):
        self.my_gas_price_in_wei = int(gas_price_in_gwei) * int(1e9)

    # Deploy a new proxy_admin contract.
    def proxy_admin_deploy(self):
        proxy_admin = ProxyAdmin('contracts/ProxyAdmin.json', self.w3, None, self.this_account, self.verbose,
                                 deploy=True, deploy_args_list=[], gas_price_in_wei=self.my_gas_price_in_wei)
        self.proxy_admin = proxy_admin

    # Instantiate an existing proxy admin contract.
    def proxy_admin_init(self, proxy_admin_address):
        proxy_admin = ProxyAdmin('contracts/ProxyAdmin.json', self.w3, proxy_admin_address, self.this_account, self.verbose)
        self.proxy_admin = proxy_admin

    # Deploy a new proxy_upgradeable contract.
    def proxy_upgradeable_deploy(self, impl_addr, admin_addr, data):
        proxy_upgradeable = TransparentUpgradeableProxy('contracts/TransparentUpgradeableProxy.json', self.w3, None, self.this_account, self.verbose,
                                 deploy=True, deploy_args_list=[impl_addr, admin_addr, data], gas_price_in_wei=self.my_gas_price_in_wei)
        self.proxy_upgradeable = proxy_upgradeable

    # Instantiate an existing proxy admin contract.
    def proxy_upgradeable_init(self, proxy_upgradeable_address):
        proxy_upgradeable = TransparentUpgradeableProxy('contracts/TransparentUpgradeableProxy.json', self.w3, proxy_upgradeable_address, self.this_account, self.verbose)
        self.proxy_upgradeable = proxy_upgradeable

    # Deploy a new token contract.
    def token_deploy(self, token_name, token_symbol, initial_supply = 100000000000000000000000000):
        token = Token('contracts/Token.json', self.w3, None, self.this_account, self.verbose, deploy=True, deploy_args_list=[token_name, token_symbol, initial_supply], gas_price_in_wei=self.my_gas_price_in_wei)
        self.token = token

    # Instantiate an existing token contract.
    def token_init(self, token_contract_address):
        token = Token('contracts/Token.json', self.w3, token_contract_address, self.this_account, self.verbose)
        self.token = token

    # Deploy a new competition contract.
    def competition_deploy(self):
        competition = Competition('contracts/Competition.json', self.w3, None, self.this_account, self.verbose, True, gas_price_in_wei=self.my_gas_price_in_wei)
        self.competition = competition

    # Instantiate an existing competition contract.
    def competition_init(self, competition_contract_address):
        competition = Competition('contracts/Competition.json', self.w3, competition_contract_address, self.this_account, self.verbose)
        self.competition = competition
        
    # Deploy a new old_competition contract.
    def old_competition_deploy(self):
        old_competition = OldCompetition('contracts/OldCompetition.json', self.w3, None, self.this_account, self.verbose, True, gas_price_in_wei=self.my_gas_price_in_wei)
        self.old_competition = old_competition

    # Instantiate an existing old_competition contract.
    def old_competition_init(self, old_competition_contract_address):
        old_competition = OldCompetition('contracts/OldCompetition.json', self.w3, old_competition_contract_address, self.this_account, self.verbose)
        self.old_competition = old_competition

    # Deploy a new registry contract.
    def registry_deploy(self):
        registry = Registry('contracts/Registry.json', self.w3, None, self.this_account, self.verbose, deploy=True, deploy_args_list=[], gas_price_in_wei=self.my_gas_price_in_wei)
        self.registry = registry

    # Initiate an existing registry contract.
    def registry_init(self, registry_contract_address):
        registry = Registry('contracts/Registry.json', self.w3, registry_contract_address, self.this_account, self.verbose)
        self.registry = registry
        
    # Deploy a new multisig contract.
    def multisig_deploy(self, owners_list, required):
        multisig = MultiSig('contracts/MultiSig.json', self.w3, None, self.this_account, self.verbose, deploy=True, deploy_args_list=[owners_list, required], gas_price_in_wei=self.my_gas_price_in_wei)
        self.multisig = multisig

    # Initiate an existing multisig contract.
    def multisig_init(self, multisig_contract_address):
        multisig = MultiSig('contracts/MultiSig.json', self.w3, multisig_contract_address, self.this_account, self.verbose)
        self.multisig = multisig

    # Deploy
    def vault_deploy(self, start=0):
        vault = Vault('contracts/Vault.json', self.w3, None, self.this_account, self.verbose, deploy=True, deploy_args_list=[start, self.token.contract.address], gas_price_in_wei=self.my_gas_price_in_wei)
        self.vault = vault

    def vault_init(self, vault_contract_address):
        vault = Vault('contracts/Vault.json', self.w3, vault_contract_address, self.this_account, self.verbose)
        self.vault = vault

    def sponsor(self, amount_tokens):
        integer_amount = token_float_to_uint(amount_tokens, self.token)
        self.competition.sponsor(integer_amount, gas_price_in_wei = self.my_gas_price_in_wei)

    def create_dataset(self):
        return create_dataset()

    def upload_datasets(self, train_csv_file_path, test_csv_file_path, public_key_file_path, zip_folder_name='dataset_dir'):
        # TODO: read a training dataset csv file and checks the number of rows and columns
        # TODO: read a test dataset csv file and checks tne number of rows and columns

        # Create folder for zipping
        try: os.mkdir(zip_folder_name)
        except: pass

        # Move files into folder for zipping
        fileName = train_csv_file_path.split('/')
        if len(fileName) > 0: fileName = fileName[-1]
        copy_file(train_csv_file_path, zip_folder_name + '//' + fileName)

        fileName = test_csv_file_path.split('/')
        if len(fileName) > 0: fileName = fileName[-1]
        copy_file(test_csv_file_path, zip_folder_name + '//' + fileName)

        # fileName = public_key_file_path.split('/')
        # if len(fileName) > 0: fileName = fileName[-1]
        # copy_file(public_key_file_path, zip_folder_name + '//' + fileName)

        # Zip folder
        zip_file(zip_folder_name)

        # Put on IPFS
        dataset_cid = pin_file_to_ipfs(zip_folder_name + '.zip')
        key_cid = pin_file_to_ipfs(public_key_file_path)

        return dataset_cid, key_cid

    def zip_and_upload_dataset(self, dataset_dir_path, public_key_file_path, zip_folder_name=None):

        if zip_folder_name is None:
            zip_folder_name = dataset_dir_path.split('/')[-1]

        if dataset_dir_path[-3] != 'zip':
            zip_file(dataset_dir_path, zip_folder_name)

        # Put on IPFS
        dataset_cid = pin_file_to_ipfs(zip_folder_name + '.zip')
        key_cid = pin_file_to_ipfs(public_key_file_path)

        return dataset_cid, key_cid

    
    def open_staking_and_register_dataset(self, dataset_cid, key_cid):
        self.competition.openStaking(cid_to_hash(dataset_cid), cid_to_hash(key_cid), gas_price_in_wei = self.my_gas_price_in_wei)

    def update_dataset(self, old_dataset_cid, new_dataset_cid):
        self.competition.updateDataset(cid_to_hash(old_dataset_cid), cid_to_hash(new_dataset_cid), gas_price_in_wei = self.my_gas_price_in_wei)

    def open_submission(self):
        self.competition.openSubmission(gas_price_in_wei = self.my_gas_price_in_wei)

    def close_submission(self):
        self.competition.closeSubmission(gas_price_in_wei = self.my_gas_price_in_wei)

    def retrieve_one_submission(self, challenge_number, participant_address, retrieved_submissions_folder, private_key_path, decrypted_destination_path, problematic_submissions):
        # Retrieve and unzip
        submission_cid_hash = self.competition.getSubmission(challenge_number, participant_address)
        submission_cid = hash_to_cid(submission_cid_hash.hex())
        print(submission_cid)

        # remove existing folder
        dir_path = os.path.join(os.getcwd(), retrieved_submissions_folder)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

        retrieve_file(submission_cid, retrieved_submissions_folder + '.zip')
        unzip_dir(retrieved_submissions_folder + '.zip', retrieved_submissions_folder)

        # Get encrypted participant symmetric key
        participant_key_path = None
        for f in os.listdir(retrieved_submissions_folder):
            if f.endswith('.pem'):
                participant_key_path = retrieved_submissions_folder + '//' + f
        if participant_key_path == None:
            print("No decryption key found. Please check the downloaded predictions zip file.")

        # Decrypt Participant's Symmetric Key
        decrypted_symmetric_key_path = decrypt_participant_key(private_key_path, participant_key_path)

        # Get encrypted submission
        encrypted_submission_path = None
        originator_path = None
        for f in os.listdir(retrieved_submissions_folder):
            if f.endswith('.bin'):
                if f == 'originator.bin':
                    originator_path = retrieved_submissions_folder + '//' + f
                else:
                    encrypted_submission_path = retrieved_submissions_folder + '//' + f
        if (encrypted_submission_path is None):
            problematic_submissions.append([participant_address, None, submission_cid, submission_cid_hash, 'No submission file found.'])
            return None
        if (originator_path is None):
            problematic_submissions.append([participant_address, None, submission_cid, submission_cid_hash, 'No originator file found.'])
            return None

        # Decrypt the originator file
        originator_file_destination = retrieved_submissions_folder + '//originator.txt'
        decrypt_file(originator_path, decrypted_symmetric_key_path, originator_file_destination)

        # Verify originator.
        with open(originator_file_destination, 'r') as f:
            decrypted_originator = f.read().strip()
        if decrypted_originator.lower() != participant_address.lower():
            problematic_submissions.append([participant_address, decrypted_originator, submission_cid, submission_cid_hash, 'Originator and submitter inconsistent.'])
            return None

        # Decrypt the submission file
        decrypt_file(encrypted_submission_path, decrypted_symmetric_key_path, decrypted_destination_path)

        return participant_address

    def retrieve_submissions(self, challenge_number, private_key_path):
                             #from_block, to_block = None, chunk = 20000):

        # Warn if the challenge is still open for submissions.
        if self.competition.getPhase(challenge_number) < 3:
            print('WARNING: This challenge may still be open for submissions. Collected submissions are incomplete.')

        # Create a folder for decrypted submissions for this challenge
        folder_name = 'decrypted_submissions_for_challenge_{}'.format(challenge_number)
        try: os.mkdir(folder_name)
        except: pass

        # Create a folder for retrieved submissions for this challenge
        retrieved_folder = 'retrieved_submissions_for_challenge_{}'.format(challenge_number)
        try: os.mkdir(retrieved_folder)
        except: pass

        # Get the latest submission CID from each registered participant, retrieve and decrypt the submission
        problematic_submissions = []
        successful_participants = []

        participant_list = self.competition.getSubmitters(challenge_number)
        participant_set = set(participant_list)

        if len(participant_list) != len(participant_set):
            print('Duplicates found in list of submitters!')
        else:
            print('No duplicates found in list of submitters.')

        for data in participant_set:
            participant_address = self.w3.toChecksumAddress(data)
            retrieved_submissions_folder = '{}//retrieved_challenge_{}_participant_{}'.format(retrieved_folder,challenge_number, participant_address[0:6])
            successful_pt = self.retrieve_one_submission(challenge_number, participant_address, retrieved_submissions_folder, private_key_path, "{}/{}.csv".format(folder_name, participant_address), problematic_submissions)

            if not successful_pt is None:
                successful_participants.append(successful_pt)

        if len(problematic_submissions) > 0:
            df = pd.DataFrame(problematic_submissions, columns=['submitter','decrypted_originator', 'cid', 'cid_in_hex_format', 'problem_description'])
            df.to_csv('problematic_submissions_for_challenge{}.csv'.format(challenge_number))

        df = pd.DataFrame(successful_participants, columns=['participant'])
        df.to_csv('successful_participants_challenge{}.csv'.format(challenge_number))

        print('{} problematic submissions found.'.format(len(problematic_submissions)))
        return
    # creates random scores and uploads a set of results for a challenge
    def create_and_upload_results(self, challenge, participants):
        return create_and_upload_overall_results(challenge, participants)

    # uploads a score csv file to pinata (IPFS) and returns a IPFS cid
    def upload_score(self, score_file_path):
        score_cid = pin_file_to_ipfs(score_file_path)
        return score_cid

    # writes an IPFS score cid to a challenge. The challenge results must be updated before opening a new challenge.
    def submit_results(self, score_cid):
        self.competition.submitResults(cid_to_hash(score_cid), gas_price_in_wei = self.my_gas_price_in_wei)

    # overwrites an IPFS score cid to a challenge
    def update_results(self, old_score_cid, new_score_cid):
        self.competition.updateResults(cid_to_hash(old_score_cid), cid_to_hash(new_score_cid), gas_price_in_wei = self.my_gas_price_in_wei)

    def create_rewards_file(self, winners):
        challenge_budget = self.competition.getCurrentChallengeRewardsBudget()
        tournament_budget = self.competition.getCurrentTournamentRewardsBudget()

        if challenge_budget <= 0 or tournament_budget <= 0:
            print('Not enough budget!')
            return

        # challenge
        challenge_allocation = token_uint_to_float(0.99 * challenge_budget // len(winners), self.token)
        tournament_allocation = token_uint_to_float(0.99 * tournament_budget // len(winners), self.token)
        data = []
        challenge_disbursed = 0
        tournament_disbursed = 0
        for w in winners:
            data.append([w, challenge_allocation, tournament_allocation])
            challenge_disbursed += challenge_allocation
            tournament_disbursed += tournament_allocation

            if (challenge_budget-challenge_disbursed) <= 0:
                print('Ran out of challenge rewards!')
                return
            if (tournament_budget-tournament_disbursed) <= 0:
                print('Ran out of tournament rewards!')
                return

        df = pd.DataFrame(data, columns=['winners', 'challenge_rewards', 'tournament_rewards'])
        filename = 'rewards_{}.csv'.format(datetime.now().strftime('%Y-%b-%d_%Hh%Mm%Ss'))
        df.to_csv(filename)
        return filename

    def create_rank_file(self, participants):
        filename = 'ranks_{}.csv'.format(datetime.now().strftime('%Y-%b-%d_%Hh%Mm%Ss'))
        ranks = list(range(1, len(participants)+1))
        data = []
        for p in participants:
            r = random.choice(ranks)
            ranks.remove(r)
            data.append([p,r])
        df = pd.DataFrame(data, columns=['participants', 'ranks'])
        df.to_csv(filename)
        return filename

    def create_data_file(self, participants, label='data'):
        filename = '{}_{}.csv'.format(label, datetime.now().strftime('%Y-%b-%d_%Hh%Mm%Ss'))

        data = []
        for p in participants:
            value = 100 * random.random()
            data.append([p, value])
        df = pd.DataFrame(data, columns=['participants', label])
        df.to_csv(filename)
        return filename

    def upload_info(self, challenge_number, item_number, file_path, label='data', from_wei = False):
        df = pd.read_csv(file_path)
        participants = df['participants'].tolist()
        data = df[label].tolist()
        if from_wei:
            data = [token_float_to_uint(d, self.token) for d in data]
        assert len(participants) == len(data), 'Participants and data columns of different length.'
        self.competition.updateInformationBatch(challenge_number, participants, item_number, data, gas_price_in_wei = self.my_gas_price_in_wei)

    # uploads the rewards to the contest
    def pay_rewards(self, rewards_csv_path, winners_label='winners', challenge_rewards_in_float_label='challenge_reward', tournament_rewards_in_float_label='tournament_reward'):
        challenge_budget = self.competition.getCurrentChallengeRewardsBudget()
        tournament_budget = self.competition.getCurrentTournamentRewardsBudget()
        df = pd.read_csv(rewards_csv_path)
        winners = df[winners_label].tolist()
        challenge_rewards = df[challenge_rewards_in_float_label].tolist()
        tournament_rewards = df[tournament_rewards_in_float_label].tolist()
        integer_challenge_rewards = [int(r * 1e18) for r in challenge_rewards]
        integer_tournament_rewards = [int(r * 1e18) for r in tournament_rewards]
        assert len(winners) == len(integer_challenge_rewards), 'winners and challenge rewards columns of different length.'
        assert len(winners) == len(integer_tournament_rewards), 'winners and tournament rewards columns of different length.'
        print(sum(integer_challenge_rewards), challenge_budget)
        assert sum(integer_challenge_rewards) <= challenge_budget, 'challenge rewards amount greater than budget.'
        assert sum(integer_tournament_rewards) <= tournament_budget, 'tournament rewards amount greater than budget.'
        self.competition.payChallengeAndTournamentRewards(winners, integer_challenge_rewards, integer_tournament_rewards, gas_price_in_wei = self.my_gas_price_in_wei)

    # functions for reading information from the Competition contract
    def get_current_gas_price_in_wei(self):
        return self.w3.eth.gas_price

    def get_my_competition_token_balance(self):
        integer_amount = self.competition.getBalance(self.token.controlling_account_address)
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

    def get_stake(self, participant):
        return token_uint_to_float(self.competition.getStake(participant), self.token)

    def get_dataset_cid(self, challenge_number):
        dataset_hash = self.competition.getDatasetHash(challenge_number).hex()
        if int(dataset_hash, 16) == 0 or int(dataset_hash, 16) == 1:
            print('Dataset for challenge {} not found.'.format(challenge_number))
            return None
        else:
            return hash_to_cid(dataset_hash)

    def get_result_cid(self, challenge_number):
        results_hash = self.competition.getResultsHash(challenge_number).hex()
        if int(results_hash, 16) == 0 or int(results_hash, 16) == 1:
            print('Results for challenge {} not found.'.format(challenge_number))
            return None
        else:
            return hash_to_cid(results_hash)

    def get_information(self, challenge_number, participant, itemNumber):
        return self.competition.getInformation(challenge_number, participant, itemNumber)

    def add_competition_admin(self, new_admin_address):
        self.competition.grantRole(0, new_admin_address, gas_price_in_wei = self.my_gas_price_in_wei)

    def del_competition_admin(self, admin_address):
        self.competition.revokeRole(0, admin_address, gas_price_in_wei = self.my_gas_price_in_wei)

    def add_registry_admin(self, new_admin_address):
        self.registry.grantRole(0, new_admin_address, gas_price_in_wei = self.my_gas_price_in_wei)

    def del_registry_admin(self, admin_address):
        self.registry.revokeRole(0, admin_address, gas_price_in_wei = self.my_gas_price_in_wei)

    def add_competition_to_registry(self, competition_name, competition_address, rules_cid):
        self.registry.registerNewCompetition(competitionName=competition_name, competitionAddress=competition_address, rulesLocation=cid_to_hash(rules_cid), gas_price_in_wei = self.my_gas_price_in_wei)

    def add_token_to_registry(self):
        self.registry.changeTokenAddress(self.token.contract.address, gas_price_in_wei = self.my_gas_price_in_wei)

    def add_vault_to_registry(self):
        self.registry.changeVaultAddress(self.vault.contract.address, gas_price_in_wei = self.my_gas_price_in_wei)

    def activate_competition(self, competition_name):
        if self.registry.getCompetitionActive(competition_name):
            print('{} is already active.'.format(competition_name))
            return
        self.registry.toggleCompetitionActive(competition_name, gas_price_in_wei = self.my_gas_price_in_wei)

    def deactivate_competition(self, competition_name):
        if not self.registry.getCompetitionActive(competition_name):
            print('{} is already inactive.'.format(competition_name))
            return
        self.registry.toggleCompetitionActive(competition_name, gas_price_in_wei = self.my_gas_price_in_wei)

    def get_competition_from_registry(self, competition_name):
        return self.registry.getCompetitionAddress(competition_name)

    def create_and_upload_rules(self):
        return create_and_upload_rules(self.competition.contract.address)




