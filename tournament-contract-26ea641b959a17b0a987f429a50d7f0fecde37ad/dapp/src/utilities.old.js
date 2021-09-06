import { ethers } from "ethers";
import JSZip from 'jszip'

import Encoding from './encoding'

const REGISTRY_ADDR_DEFAULT = '0x54ffe47B396d04FD567bC87788D085CF29Ac15E2';
const TOURNAMENT_NAME = 'DAPP_TNMT_0';

export const ethereum = window.ethereum; // TODO: do not export
const encoding = new Encoding();
const provider = new ethers.providers.Web3Provider(ethereum);
const gateways = ['https://gateway.ipfs.io/ipfs/', 'https://gateway.pinata.cloud/ipfs/', 'https://ipfs.io/ipfs/', 'https://cloudflare-ipfs.com/ipfs/'];


let registry;
let tournament;
let token;
let chainName;
let activeUser


async function _parseAbi(filename) {
	let response = await fetch(`/contracts/${filename}`);
	return (await response.json())['abi'];
}

function _isMetaMaskInstalled() {
	return !!ethereum && ethereum.isMetaMask;
};

async function _getActiveUser() {
	if (_isMetaMaskInstalled()){
		await ethereum.request({ method: 'eth_requestAccounts' });
	}
	activeUser = await provider.getSigner().getAddress();
}

function _hashToCid(hash) {
	if (hash && hash.byteLength !== undefined) {
		hash = encoding.byteToHexString(hash);
	}
	if (hash.slice(0, 2) === '0x') {
		hash = hash.slice(2);
	}
	hash = '1220' + hash;
	return encoding.byteToB58(encoding.hexStringToByte(hash));
}

async function _retrieve(hash) {
	let cid      = _hashToCid(hash);
	let gateway  = gateways[0];
	let request  = new Request(gateway + cid);
	let response = await fetch(request);
	let blob     = await response.blob();

	if (response.ok) {
		let ext = blob['type'].split('/')[1];
		if (ext !== 'zip') {
			ext = 'csv';
		}

		let a = document.createElement('a');
		let url = URL.createObjectURL(blob);
		a.href = url;
		let filename = cid.slice(0,9) + '.' + ext;
		a.download = filename;
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
	} else {
		console.error('File not found.');
		return;
	}
}


export function getTournamentName() {
  return TOURNAMENT_NAME;
}

export async function getChainName() {
	let chainId = await ethereum.request({ method: 'eth_chainId' });
	switch (chainId) {
		case '1':
			chainName = 'MAINNET';
			break;
		case '3':
			chainName = 'Ropsten Test';
			break;
		case '4':
			chainName = 'Rinkeby Test';
			break;
		case '42':
			chainName = 'Kovan Test';
			break;
		default:
			chainName = 'Unknown Network';
	}
}

export async function getTournamentAddress() {
	return registry.getTournamentAddress(TOURNAMENT_NAME);
}

export async function getTokenAddress() {
	return registry.getTokenAddress();
}

export async function setup() {
	let registryAbi = await _parseAbi('Registry.json');
	registry        = new ethers.Contract(REGISTRY_ADDR_DEFAULT, registryAbi, provider);

	let tournamentAddress = getTournamentAddress();
	let tournamentAbi     = _parseAbi('Tournament.json');
	let tokenAddress      = getTokenAddress()
	let tokenAbi          = _parseAbi('Token.json');

	await Promise.all([tournamentAddress, tournamentAbi, tokenAddress, tokenAbi]).then(result => {
		tournament = new ethers.Contract(result[0], result[1], provider);
		token      = new ethers.Contract(result[2], result[3], provider);
	})
}

export function refresh() {
	tournament = tournament.connect(provider.getSigner());
	token      = token.connect(provider.getSigner());
}

export async function connect() {
	await Promise.all([getChainName(), _getActiveUser()]);
	refresh();
}

export async function getStake() {
  let caller = await provider.getSigner().getAddress();
  return ethers.utils.formatEther(await tournament.getStake(caller));
}

// export async function getPhase(phaseIndex) {
//   return this.tournament.getPhaseStatus(phaseIndex);
// }

export async function getLastPhaseIndex() {
	return tournament.getLastPhaseIndex();
}


// The following are functions to read general information from the smart contract.
export async function getTournamentPool() {
	return ethers.utils.formatEther(await tournament.getTournamentPool());
}

export async function getPhaseStatus(phaseIndex) {
	let status = await tournament.getPhaseStatus(phaseIndex);
	switch (status) {
		case 0:
			return "Phase has not started.";
		case 1:
			return "Phase is in STAKING mode.";
		case 2:
			return "Phase is in SUBMISSION mode.";
		case 3:
			return "Phase is in COMPUTATION mode.";
		case 4:
			return "Phase is COMPLETE."
		default:
			return "Phase is in UNKNOWN mode."
	}
}

export async function downloadPhaseDataset(phaseIndex) {
	let datasetHash = await tournament.getPhaseDatasetHash(phaseIndex);
	if (parseInt(datasetHash, 16) === 0){
		console.error(`No dataset found for phase ${phaseIndex}.`);
		return null;
	}

	// Download from IPFS. Browser will ask for a download confirmation.
	_retrieve(datasetHash);
}













export class RciUtilities {
	constructor() {
		this.encoding = new Encoding();
		this.ethereum = window.ethereum
		this.provider = new ethers.providers.Web3Provider(this.ethereum);
		this.REGISTRY_ADDR_DEFAULT = '0x54ffe47B396d04FD567bC87788D085CF29Ac15E2';
		this.TOURNAMENT_NAME = 'DAPP_TNMT_0';
		this.gateways = ['https://gateway.ipfs.io/ipfs/', 'https://gateway.pinata.cloud/ipfs/', 'https://ipfs.io/ipfs/', 'https://cloudflare-ipfs.com/ipfs/']
	}

	async setup() {
		let tournamentAbi = await this.parseAbi('Tournament.json');
		let tokenAbi = await this.parseAbi('Token.json');
		let registryAbi = await this.parseAbi('Registry.json');

		this.registry = new ethers.Contract(this.REGISTRY_ADDR_DEFAULT, registryAbi, this.provider);

		let tournamentAddress = await this.getTournamentAddress();
		let tokenAddress = await this.getTokenAddress();

		this.tournament = new ethers.Contract(tournamentAddress, tournamentAbi, this.provider);
		this.token = new ethers.Contract(tokenAddress, tokenAbi, this.provider);
	}

	// Call this to set the current sending account.
	refresh() {
		this.tournament = this.tournament.connect(this.provider.getSigner());
		this.token = this.token.connect(this.provider.getSigner());
	}

	async connect() {
		await this.getChainName();
		await this.getActiveUser();
		this.refresh();
	}

	// The following are functions to read general information from the smart contract.
	async getTournamentPool() {
		return ethers.utils.formatEther(await this.tournament.getTournamentPool());
	}

	async getCurrentTotalStaked() {
		return ethers.utils.formatEther(await this.tournament.getCurrentTotalStaked());
	}

	async getTotalStakesLockedForPhase(phaseIndex) {
		return ethers.utils.formatEther(await this.tournament.getTotalStakesLockedForPhase(phaseIndex));
	}

	async getCurrentParticipationRewardsBudget() {
		return ethers.utils.formatEther(await this.tournament.getCurrentParticipationRewardsBudget());
	}

	async getCurrentPerformanceRewardsBudget() {
		return ethers.utils.formatEther(await this.tournament.getCurrentPerformanceRewardsBudget());
	}

	async getLastPhaseIndex() {
		return await this.tournament.getLastPhaseIndex();
	}

	async getStakeThreshold() {
		return ethers.utils.formatEther(await this.tournament.getStakeThreshold());
	}

	async getTokenName() {
		return await this.token.name();
	}

	async getTokenSymbol() {
		return await this.token.symbol();
	}

	async getTokenAddress() {
		return await this.registry.getTokenAddress();
	}

	async getTournamentAddress() {
		return await this.registry.getTournamentAddress(this.TOURNAMENT_NAME);
	}

	// The following are functions that read information from the smart contract but require at least one input.

	async getPhaseStatus(phaseIndex) {
		let status = await this.tournament.getPhaseStatus(phaseIndex);
		switch (status){
			case 0:
				return "Phase has not started.";
			case 1:
				return "Phase is in STAKING mode.";
			case 2:
				return "Phase is in SUBMISSION mode.";
			case 3:
				return "Phase is in COMPUTATION mode.";
			case 4:
				return "Phase is COMPLETE."
			default:
				return "Phase is in UNKNOWN mode."
		}
	}

	async getPhaseDatasetHash(phaseIndex) {
		let datasetHash = await this.tournament.getPhaseDatasetHash(phaseIndex);
		return (parseInt(datasetHash,16)==0) ? "No dataset posted for this phase." : this.hashToCid(datasetHash);
	}

	async getPhaseResultsHash(phaseIndex) {
		let resultsHash = await this.tournament.getPhaseResultsHash(phaseIndex);
		return (parseInt(resultsHash,16)==0) ? "No results posted for this phase." : this.hashToCid(resultsHash);
	}

	async getPhaseSubmissionCounter(phaseIndex) {
		return await this.tournament.getPhaseSubmissionCounter(phaseIndex);
	}

	// The following are functions to read information from the smart contract specific to the current active user.
	async getStake() {
		let caller = await this.provider.getSigner().getAddress();
		return ethers.utils.formatEther(await this.tournament.getStake(caller));
	}

	async getSubmission(phaseIndex) {
		let caller = await this.provider.getSigner().getAddress();
		let submissionHash = await this.tournament.getSubmission(phaseIndex, caller);
		return (parseInt(submissionHash,16)==0) ? "No submissions made for this phase." : this.hashToCid(submissionHash);
	}

	async getAllowance() {
		let caller = await this.provider.getSigner().getAddress();
		return ethers.utils.formatEther(await this.token.allowance(caller, this.tournament.address));
	}

	// The following are write functions. They will induce a Metamask pop-up for the user to confirm the transaction and set the gas amount if desired.

	async increaseAllowance(amountToIncreaseInFloat) {
		amountToIncreaseInFloat = document.getElementById('testInput').value;
		let amountToIncreaseInInteger = ethers.utils.parseEther(amountToIncreaseInFloat);
		let txObj = await this.token.increaseAllowance(this.tournament.address, amountToIncreaseInInteger);
		
		// wait for the transaction to be mined and processed.
		await this.provider.waitForTransaction(txObj['hash']);
	}

	async decreaseAllowance(amountToDecreaseInFloat) {
		let amountToDecreaseInInteger = ethers.utils.parseEther(amountToDecreaseInFloat);
		let txObj = await this.token.decreaseAllowance(this.tournament.address, amountToDecreaseInInteger);
		
		// wait for the transaction to be mined and processed.
		await this.provider.waitForTransaction(txObj['hash']);
	}


	async increaseStake(amountToIncreaseInFloat) {
		amountToIncreaseInFloat = document.getElementById('testInput').value;
		let amountToIncreaseInInteger = ethers.utils.parseEther(amountToIncreaseInFloat);
		let txObj = await this.tournament.increaseStake(amountToIncreaseInInteger);

		// wait for the transaction to be mined and processed.
		await this.provider.waitForTransaction(txObj['hash']);

	}

	async decreaseStake(amountToDecreaseInFloat) {
		let amountToDecreaseInInteger = ethers.utils.parseEther(amountToDecreaseInFloat);
		let txObj = await this.tournament.decreaseStake(amountToDecreaseInInteger);
		
		// wait for the transaction to be mined and processed.
		await this.provider.waitForTransaction(txObj['hash']);
	}

	async transferStake(recipient, amountToTransferInFloat) {
		let amountToTransferInInteger = ethers.utils.parseEther(amountToTransferInFloat);
		let txObj = await this.tournament.transferStake(recipient, amountToTransferInInteger);
		
		// wait for the transaction to be mined and processed.
		await this.provider.waitForTransaction(txObj['hash']);
	}

	// The following read the the IPFS cid from the smart contract, then retrieves data from IPFS.
	// `download` functions: downloads either .zip or .csv files from IPFS.
	// `obtain` functions: obtains data from IPFS and returns data as js arrays or js strings.

	async downloadPhaseDataset(phaseIndex) {
		let datasetHash = await this.tournament.getPhaseDatasetHash(phaseIndex);
		if (parseInt(datasetHash,16)==0){
			console.error("No dataset found for phase " + phaseIndex + ".");
			return null;
		}

		// Download from IPFS. Browser will ask for a download confirmation.
		await this.retrieve(datasetHash);
	}

	async downloadPhaseResults(phaseIndex) {
		let resultsHash = await this.tournament.getPhaseResultsHash(phaseIndex);
		if (parseInt(resultsHash,16)==0){
			console.error("No results found for phase " + phaseIndex + ".");
			return null;
		}

		// Download from IPFS. Browser will ask for a download confirmation.
		await this.retrieve(resultsHash);
	}

	async obtainMyHistoricalScores() {
		let output = await this.obtainOverallIpfs();
		let phases = output[0];
		let results = output[1];
		if (phases == null){
			console.error("No results found for "+ await this.provider.getSigner().getAddress() + ".");
			return [null, null]
		}
		return [phases, results];
	}

	async obtainOverallIpfs() {
		let phaseIndex = await this.tournament.getLastPhaseIndex();
		let resultsHash = await this.tournament.getPhaseResultsHash(phaseIndex);
		if (parseInt(resultsHash,16)==0){
			console.error("No results found for phase " + phaseIndex + ".");
			return [null, null]
		}
		let cid = this.hashToCid(resultsHash);
		let url = this.gateways[0] + cid;
		let response = await fetch(url);
		let reader = response.body.getReader();
		
		let data = await reader.read();
		let decoder = new TextDecoder();
		let rows = decoder.decode(data.value).split('\n');
		let cols;
		let activeUser = await this.provider.getSigner().getAddress();

		for (let i=0; i < rows.length; i++){
			cols = rows[i].split(',');
			if (cols[1] == activeUser){
				return await this.obtainFromIndividualIpfs(cols[2]);
			}
		}

		while (!data.done){
			data = await reader.read();
			rows = decoder.decode(data.value).split('\n');
			for (let i=0; i < rows.length; i++){
				cols = rows[i].split(',');
				if (cols[1] == activeUser){
					return await this.obtainFromIndividualIpfs(cols[2]);
				}
			}
		}

		return [null, null]
	}

	async obtainFromIndividualIpfs(cid) {
		let url = this.gateways[0] + cid;
		let response = await fetch(url);
		let reader = response.body.getReader();
		let data = await reader.read();
		let decoder = new TextDecoder();
		let rows = decoder.decode(data.value).split('\n');
		let cols;
		let phases = [];
		let scores = [];

		//skip first row of labels.
		for (let i=1; i < rows.length; i++){
			cols = rows[i].split(',');
			if (cols[1] != null){
				phases.push(cols[1]);
				scores.push(cols[2]);
			}
		}

		while (!data.done){
			data = await reader.read();
			rows = decoder.decode(data.value).split('\n');
			for (let i=0; i < rows.length; i++){
				cols = rows[i].split(',');
				if (cols[1] != null){
					phases.push(cols[1]);
					scores.push(cols[2]);
				}
			}
		}
		if (phases.length == 0){
			return [null, null]
		}
		return [phases, scores];
	}

	async obtainRules() {
		let rulesHash = await this.registry.getTournamentRulesLocation(this.TOURNAMENT_NAME);
		if (parseInt(rulesHash,16)==0){
			return "No rules published for " + this.TOURNAMENT_NAME + ".";
		}
		let rulesCid = this.hashToCid(rulesHash);
		let url = this.gateways[0] + rulesCid;
		let response = await fetch(url);
		let reader = response.body.getReader();
		let data = await reader.read();
		let decoder = new TextDecoder();
		let text = decoder.decode(data.value);

		while (!data.done){
			data = await reader.read();
			text += decoder.decode(data.value);
		}

		return text;
	}
 
	// The following functions take files from the user input, processes them and uploads them to IPFS, then sends a blockchain transaction to write the IPFS cid to the smart contract.

	async makeSubmission() {

		let predictionsFile = document.getElementById("predictionsFile").files[0];
		let pubKeyFile = document.getElementById("pubKeyFile").files[0];

		// Encrypt, zip and upload to IPFS.
		let output = await this.encryptZipUpload(predictionsFile, pubKeyFile);
		let myCid = output[1];
		console.log(myCid);

		// Submit hash to blockchain.
		let txObj =  await this.tournament.submitNewPhasePredictions(this.cidToHash(myCid));

		// wait for the transaction to be mined and processed.
		await this.provider.waitForTransaction(txObj['hash']);
	}


	async redoSubmission() {

		let predictionsFile = document.getElementById("predictionsFile").files[0];
		let pubKeyFile = document.getElementById("pubKeyFile").files[0];
		let oldCidString = document.getElementById("testInput").value;

		
		// Encrypt, zip and upload to IPFS.
		let output = await this.encryptZipUpload(predictionsFile, pubKeyFile);
		let myCid = output[1];

		// Submit hash to blockchain.
		let txObj =  await this.tournament.updatePhaseSubmission(this.cidToHash(oldCidString), this.cidToHash(myCid));
		
		// wait for the transaction to be mined and processed.
		await this.provider.waitForTransaction(txObj['hash']);
	}


	/* ***********************************
	The following are helper functions for the above blockchain and IPFS interaction functions.
	*********************************** */
	
	isMetaMaskInstalled() {
		const { ethereum } = window;
		return Boolean(ethereum && ethereum.isMetaMask);
	  };

	async getActiveUser() {
		if (this.isMetaMaskInstalled()){
			await window.ethereum.request({ method: 'eth_requestAccounts' });
		}
		this.activeUser = await this.provider.getSigner().getAddress();
	}

	async getChainName() {
		let chainId = await window.ethereum.request({ method: 'eth_chainId' });
		let chainName;
		if (chainId == 1){
			chainName = 'MAINNET';
		}else if(chainId == 3){
			chainName = 'Ropsten Test';
		}
		else if (chainId == 4){
			chainName = 'Rinkeby Test';
		}
		else if (chainId == 42){
			chainName = 'Kovan Test';
		}
		else{
			chainName = 'Unknown Network';
		}

		this.chainName = chainName;
	}

	async parseAbi(filename) {
		let response = await fetch('/contracts/' + filename);
		response = await response.json();
		let abi = response['abi'];
		return abi;
	}

	cidToHash(cid) {
		let res = this.encoding.byteToHexString(this.encoding.b58ToByte(cid));
		return "0x" + res.slice(4)

	}
	
	hashToCid(hash) {
		if (hash && hash.byteLength !== undefined) {
			hash = this.encoding.byteToHexString(hash);
		}
		if (hash.slice(0,2) == '0x') hash = hash.slice(2);
		hash = '1220' + String(hash)
		return this.encoding.byteToB58(this.encoding.hexStringToByte(hash));
	}

	async encryptZipUpload(predictionsFile, pubKeyFile) {
		const formData = new FormData();

		let predictionsData = await predictionsFile.arrayBuffer();
		let predictionsName = predictionsFile.name;

		let symmetricKey = await this.generateSymmetricKey();
		let iv = this.getIV(16);
		let encryptedPredictions = await this.encryptPredictions(predictionsData, symmetricKey, iv);

		encryptedPredictions = new Uint8Array(encryptedPredictions);
		let predictionsPayload = this.appendBuffer(iv, encryptedPredictions);

		let originator = await this.provider.getSigner().getAddress();
		let originatorData = (new TextEncoder).encode(originator);
		let encryptedOriginator = await this.encryptPredictions(originatorData, symmetricKey, iv);
		let originatorPayload = this.appendBuffer(iv, encryptedOriginator);


		let pubKeyData = await this.importRsaPublicKey(await pubKeyFile.text());
		let wrapKeyResult = await this.wrapSymmetricKey(symmetricKey, pubKeyData);

		let zip = new JSZip();
		zip.file(predictionsName.split(".")[0]+".bin", predictionsPayload);
		zip.file("originator.bin", originatorPayload);
		zip.file("encrypted_symmetric_key.pem", wrapKeyResult);
		
		let content = await zip.generateAsync({
			type: 'blob',
			compression: "DEFLATE",
			compressionOptions: {
				level: 3
			}});
		formData.append('blob', content);
		
		let response = await this.submitIpfs(formData);
		let myCid = response['Hash']
		let responseAlert = "IPFS: File of size " + response['Size'] + " bytes uploaded to IPFS with CID " + myCid + '.<br> Downloadable <a href="https://ipfs.io/ipfs/' + myCid + '">link</a>.';
		responseAlert = '<p class="info-text alert alert-primary">' + responseAlert + '</p>';
		return [responseAlert, myCid];
	}

	async submitIpfs(fileToSubmit) {
		const url = 'https://ipfs.infura.io:5001/api/v0/add';
		let response = await fetch(url, { method: 'POST', body: fileToSubmit});
		return await response.json();
	}

	async retrieve(hash) {
		let cid = this.hashToCid(hash);
		let gateway = this.gateways[0];

		let request = new Request(gateway + cid);
		let response = await fetch(request);
		let blob = await response.blob();
		if (response.ok){
			let ext = blob['type'].split("/")[1];
			if (ext!='zip'){
				ext = 'csv';
			}
			let a = document.createElement("a");
			let url = URL.createObjectURL(blob);
			a.href = url;
			let filename = cid.slice(0,9) + '.' + ext;
			a.download = filename;
			document.body.appendChild(a);
			a.click();
		}else{
			console.error('File not found.');
			return;
		}
	}
	
	/* ***********************************
	The following are functions and classes that help to perform encryption.
	*********************************** */

	async generateSymmetricKey() {
		let key = await window.crypto.subtle.generateKey(
			{
			  name: "AES-GCM",
			  length: 256
			},
			true,
			["encrypt", "decrypt"]
		  );
		return key;
	}

	getIV(size) {
		return window.crypto.getRandomValues(new Uint8Array(size));
	}

	async encryptPredictions(data, key, iv) {
		// let iv = window.crypto.getRandomValues(new Uint8Array(12));
		return await window.crypto.subtle.encrypt(
			{
			  name: "AES-GCM",
			  iv: iv,
			  tagLength: 128,

			},
			key,
			data
		  );
	}

	async wrapSymmetricKey(symmetricKey, publicKey) {
		let wrapKeyResult = await window.crypto.subtle.wrapKey(
			"raw",
			symmetricKey,
			publicKey,
			publicKey.algorithm.name
		);

		return new Uint8Array(wrapKeyResult)
	}

	str2ab(str) {
		const buf = new ArrayBuffer(str.length);
		const bufView = new Uint8Array(buf);
		for (let i = 0, strLen = str.length; i < strLen; i++) {
		  bufView[i] = str.charCodeAt(i);
		}
		return buf;
	  }

	async importRsaPublicKey(pem) {
		// fetch the part of the PEM string between header and footer
		const pemHeader = "-----BEGIN PUBLIC KEY-----";
		const pemFooter = "-----END PUBLIC KEY-----";
		const pemContents = pem.substring(pemHeader.length, pem.length - pemFooter.length);
		// base64 decode the string to get the binary data
		const binaryDerString = window.atob(pemContents);
		// convert from a binary string to an ArrayBuffer
		const binaryDer = this.str2ab(binaryDerString);
	  
		return await window.crypto.subtle.importKey(
			"spki",
			binaryDer,
			{
			  name: "RSA-OAEP",
			  hash: "SHA-1"
			},
			true,
			["wrapKey","encrypt"]
		  );
		}

	appendBuffer(buffer1, buffer2 ) {
		var tmp = new Uint8Array( buffer1.byteLength + buffer2.byteLength );
		tmp.set( new Uint8Array( buffer1 ), 0 );
		tmp.set( new Uint8Array( buffer2 ), buffer1.byteLength );
		return tmp.buffer;
	}

	async exportCryptoKey(key) {
		const exported = await window.crypto.subtle.exportKey(
		  "raw",
		  key
		);
		const exportedKeyBuffer = new Uint8Array(exported);
		return exportedKeyBuffer;
		// let enc = new TextEncoder();
		// return enc.encode(exported);
	  }

	async encryptSymmetricKey(symmetricKey, publicKey) {
		return await window.crypto.subtle.encrypt({ name: "RSA-OAEP" }, publicKey, symmetricKey);
	}
}
