import { ethers } from "ethers";
import JSZip from 'jszip'

import Encoding from './encoding'


declare global {
	interface Window { ethereum: any; }
}

// export enum ChallengePhase {
// 	NotStarted,
// 	Staking,
// 	Submission,
// 	Computation,
// 	Complete,   
// 	Unknown,    
// }


const REGISTRY_ADDR_DEFAULT = '0x2a91f354F25f9F4C8AFe078c94A997bCd50DE7Ba';
const TOURNAMENT_NAME = 'ALPHA_1';
const GATEWAYS = ['https://gateway.ipfs.io/ipfs/', 'https://gateway.pinata.cloud/ipfs/', 'https://ipfs.io/ipfs/', 'https://cloudflare-ipfs.com/ipfs/', 'https://alpha1.mypinata.cloud/ipfs/'];

export const ethereum = window.ethereum; // TODO: do not export

// const encoding = new Encoding();
// const provider = new ethers.providers.Web3Provider(ethereum);
const encoding = new Encoding();
let provider: ethers.providers.Web3Provider;

let registry;
let competition;
let token;
let chainName;
let activeUser


async function _parseAbi(filename: string): Promise<string> {
	const response = await fetch(`/contracts/${filename}`);
	return (await response.json())['abi'];
}

function _isMetaMaskInstalled(): boolean {
	return !!ethereum && ethereum.isMetaMask;
};

async function _getActiveUser(): Promise<string> {
	if (_isMetaMaskInstalled()){
		await ethereum.request({ method: 'eth_requestAccounts' });
	}
	activeUser = await provider.getSigner().getAddress();
	return activeUser;
}

async function _cidToHash(cid) {
	const res = encoding.byteToHexString(encoding.b58ToByte(cid));
	return `0x${res.slice(4)}`;
}

function _hashToCid(hash) {
	if (hash && hash.byteLength !== undefined) {
		hash = encoding.byteToHexString(hash);
	}
	if (hash.slice(0, 2) === '0x') {
		hash = hash.slice(2);
	}
	hash = `1220${hash}`;
	return encoding.byteToB58(encoding.hexStringToByte(hash));
}

function _download(hash, extension: string) {
	const cid = _hashToCid(hash);
	const gateway = GATEWAYS[4];
	// let request = new Request(gateway + cid);
	// let response = await fetch(request);
	const a = document.createElement('a');
	a.href = gateway + cid;
	const filename = `${cid.slice(0, 9)}.${extension}`; // TODO: extension
	a.download = filename;
	document.body.appendChild(a);
	a.click();
	document.body.removeChild(a);
}

async function _retrieve(hash) {
	const cid = _hashToCid(hash);
	const gateway = GATEWAYS[4];
	const request = new Request(gateway + cid);
	const response = await fetch(request);
	const blob = await response.blob();

	if (response.ok) {
		return blob.text();
	} else {
		console.error('File not found.');
		return;
	}
}

async function __retrieve(hash) {
	const cid      = _hashToCid(hash);
	const gateway  = GATEWAYS[4];
	const request  = new Request(gateway + cid);
	const response = await fetch(request);
	const blob     = await response.blob();

	if (response.ok) {
		let ext = blob['type'].split('/')[1];
		if (ext !== 'zip') {
			ext = 'csv';
		}

		const a = document.createElement('a');
		const url = URL.createObjectURL(blob);
		a.href = url;
		const filename = cid.slice(0,9) + '.' + ext;
		a.download = filename;
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
	} else {
		console.error('File not found.');
		return;
	}
}

async function _getTokenAddress() {
	return registry.getTokenAddress();
}

function _appendBuffer(buffer1, buffer2) {
	const tmp = new Uint8Array(buffer1.byteLength + buffer2.byteLength);
	tmp.set(new Uint8Array(buffer1), 0);
	tmp.set(new Uint8Array(buffer2), buffer1.byteLength);

	return tmp.buffer;
}


// TODO: move to crypto.ts file
async function _generateSymmetricKey() {
	const key = window.crypto.subtle.generateKey({
		name: "AES-GCM",
		length: 256
	},
	true,
	["encrypt", "decrypt"]);
	return key;
}

function _getIV(size) {
	return window.crypto.getRandomValues(new Uint8Array(size));
}

async function _encryptPredictions(data, key, iv) {
	// let iv = window.crypto.getRandomValues(new Uint8Array(12));
	return window.crypto.subtle.encrypt({
		name: "AES-GCM",
		iv: iv,
		tagLength: 128
	},
	key,
	data);
}

function _str2ab(str) {
	const buf = new ArrayBuffer(str.length);
	const bufView = new Uint8Array(buf);
	for (let i = 0, strLen = str.length; i < strLen; i++) {
		bufView[i] = str.charCodeAt(i);
	}

	return buf;
}

async function _importRsaPublicKey(pem) {
	// fetch the part of the PEM string between header and footer
	const pemHeader = "-----BEGIN PUBLIC KEY-----";
	const pemFooter = "-----END PUBLIC KEY-----";
	const pemContents = pem.substring(pemHeader.length, pem.length - pemFooter.length);
	// base64 decode the string to get the binary data
	const binaryDerString = window.atob(pemContents);
	// convert from a binary string to an ArrayBuffer
	const binaryDer = _str2ab(binaryDerString);

	return window.crypto.subtle.importKey(
		"spki",
		binaryDer,
		{
			name: "RSA-OAEP",
			hash: "SHA-1"
		},
		true,
		["wrapKey","encrypt"]);
}

async function _wrapSymmetricKey(symmetricKey, publicKey) {
	const wrapKeyResult = await window.crypto.subtle.wrapKey(
		"raw",
		symmetricKey,
		publicKey,
		publicKey.algorithm.name
	);

	return new Uint8Array(wrapKeyResult)
}

async function _submitIpfs(file) {
	const url = 'https://api.pinata.cloud/pinning/pinFileToIPFS';
	// const jwt = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiIxNWFiMGVmYi0wZDE3LTQ3M2ItODExZS0yZWUwZTljZmY0NGIiLCJlbWFpbCI6Imx1YmludGFuQG91dGxvb2suY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siaWQiOiJOWUMxIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZX0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6ImY2OWRlOGMxMTYyN2IwMDk2NDdiIiwic2NvcGVkS2V5U2VjcmV0IjoiOTE0ZTU2OGM4NTJiYmU1ODk5ODgwNTZmN2RmZTdjMjNiMWViYTNhZTE3ZjQ5ODhmMjlkNGYxMjVhNWUyMGUwNSIsImlhdCI6MTYyNzc0NDI3MX0.2wHGwUF_L2ZbWMn0k1PjXWt2FHZAPjussOLhNYOw92k';

	const response = await fetch(
		url,
		{
			method: 'POST',
			body: file,
			headers: {
				// 'Authorization': `Bearer ${jwt}`
				pinata_api_key: 'f69de8c11627b009647b',
				pinata_secret_api_key: '914e568c852bbe589988056f7dfe7c23b1eba3ae17f4988f29d4f125a5e20e05'
			},
		}
	);

	return response.json();
}

// async function _submitIpfs(file) {
// 	const url = 'https://ipfs.infura.io:5001/api/v0/pin/';
// 	const projectId = '1w7MApWPvrYOF49fWdayMorXjEm';
// 	const projectSecret = '6dbffa7a1fca34e6876306b9f5476836';

// 	const response = await fetch(
// 		url,
// 		{
// 			method: 'POST',
// 			body: file,
// 			headers: {
// 				'Authorization': 'Basic ' + btoa(projectId + ":" + projectSecret)
// 			}
// 		}
// 	);

// 	return response.json();
// }

export async function _encryptZipUpload(predictionsFile, pubKey) {
	const formData = new FormData();

	const predictionsData = await predictionsFile.arrayBuffer();
	const predictionsName = predictionsFile.name;

	const symmetricKey = await _generateSymmetricKey();
	const iv = _getIV(16);
	let encryptedPredictions = await _encryptPredictions(predictionsData, symmetricKey, iv);

	encryptedPredictions     = new Uint8Array(encryptedPredictions);
	const predictionsPayload = _appendBuffer(iv, encryptedPredictions);

	// const originator          = await provider.getSigner().getAddress();
  const originator          = activeUser;
	const originatorData      = (new TextEncoder).encode(originator);
	const encryptedOriginator = await _encryptPredictions(originatorData, symmetricKey, iv);
	const originatorPayload   = _appendBuffer(iv, encryptedOriginator);

	const pubKeyData    = await _importRsaPublicKey(pubKey);
	const wrapKeyResult = await _wrapSymmetricKey(symmetricKey, pubKeyData);

	const zip = new JSZip();
	zip.file(predictionsName.split(".")[0] + ".bin", predictionsPayload);
	zip.file("originator.bin", originatorPayload);
	zip.file("encrypted_symmetric_key.pem", wrapKeyResult);

	const content = await zip.generateAsync({
		type: 'blob',
		compression:        'DEFLATE',
		compressionOptions: { level: 3 },
	});
	formData.append('file', content);

	const response = await _submitIpfs(formData);
	const myCid = response['IpfsHash']
	let responseAlert = `IPFS: File of size ${response['Size']} bytes uploaded to IPFS with CID ${myCid}.<br>Downloadable <a href="https://ipfs.io/ipfs/${myCid}">link</a>.`;
	responseAlert = `<p class="info-text alert alert-primary">${responseAlert}</p>`;

	return [responseAlert, myCid];
}







export function getTournamentName() {
  return TOURNAMENT_NAME;
}

export async function getChainName() {
	const chainId = await ethereum.request({ method: 'eth_chainId' });
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

export async function getCompetitionAddress(): Promise<string> {
	return registry.getCompetitionAddress(TOURNAMENT_NAME);
}

export function init() {
	provider = new ethers.providers.Web3Provider(ethereum);
}

export async function setup(): Promise<void> {
	const registryAbi = await _parseAbi('Registry.json');
	registry          = new ethers.Contract(REGISTRY_ADDR_DEFAULT, registryAbi, provider);

	const tournamentAddress = getCompetitionAddress();
	const tournamentAbi     = _parseAbi('Competition.json');
	const tokenAddress      = _getTokenAddress()
	const tokenAbi          = _parseAbi('Token.json');

	await Promise.all([tournamentAddress, tournamentAbi, tokenAddress, tokenAbi]).then(result => {
		competition = new ethers.Contract(result[0], result[1], provider);
		token       = new ethers.Contract(result[2], result[3], provider);
	})

	ethereum.on('chainChanged', getChainName);
	ethereum.on('accountsChanged', refresh);
	ethereum.on('connect', connect);
}

export function refresh() {
	competition = competition.connect(provider.getSigner());
	token       = token.connect(provider.getSigner());
	RciEvents.emit('EthAccountChanged')
}

export async function connect() {
	await Promise.all([getChainName(), _getActiveUser()]);
	refresh();
}

export async function addToken() {
  ethereum.request({
    method: 'wallet_watchAsset',
    params: {
      type:    'ERC20',
      options: {
        address:  '0x38036bbF1e95957aB04CFd47708c5ca293916FFe',
        symbol:   'CMP1',
        decimals: 18,
        image:    'https://rocketcapital.ai/assets/logo__icon.svg',
      }
    }
  });
}

export async function isConnected() {
	let chainId = await ethereum.request({ method: 'eth_chainId' });
	return chainId == 137
}

export async function switchNetwork() {
  let chainId = await ethereum.request({ method: 'eth_chainId' });
  if (chainId == 137) {
    return "Message to show already connected."
  }
  try {
    await ethereum.request({
      method: 'wallet_switchEthereumChain',
      params: [{ chainId: '0x89' }],
    });
  } catch (error) {
    // This error code indicates that the chain has not been added to MetaMask.
    if (error.code === 4902) {
      try {
        await ethereum.request({
          method: 'wallet_addEthereumChain',
          params: [{
            chainName: 'Polygon',
						rpcUrls: ['https://rpc-mainnet.matic.quiknode.pro'],
            chainId: '0x89',
            nativeCurrency: {
              name: 'MATIC',
              symbol: 'MATIC',
              decimals: 18
            },
            blockExplorerUrls: ['https://polygonscan.com'],
            iconUrls: ['https://polygonscan.com/images/logo-white.svg']
          }],
        });
      } catch (addError) {
				console.log(addError);
      }
    }
  }
}

// Deadlines

export async function getSubmissionDeadline(challengeNumber: number) {
  return competition.getDeadlines(challengeNumber, 0);
}
export async function getResultDeadline(challengeNumber: number) {
  return competition.getDeadlines(challengeNumber, 1);
}

export async function getNextChallengeDeadline(challengeNumber: number) {
  return competition.getDeadlines(challengeNumber, 2);
}

export async function downloadCompetitionKey(phaseIndex: number) {
	const keyHash = await competition.getKeyHash(phaseIndex);
	if (parseInt(keyHash, 16) === 0) {
		console.error(`No dataset found for phase ${phaseIndex}.`);
	}

	// Download from IPFS. Browser will ask for a download confirmation.
	return _retrieve(keyHash);
}

export async function getLatestChallengeNumber() {
	return competition.getLatestChallengeNumber();
}

// The following are functions to read general information from the smart contract.
export async function getCompetitionPool(): Promise<string> {
	return ethers.utils.formatEther(await competition.getCompetitionPool());
}

export async function getSubmissionCounter(phaseIndex: number) {
	return competition.getSubmissionCounter(phaseIndex);
}

export async function getPhase(phaseIndex: number) {
	return competition.getPhase(phaseIndex);
}

// export async function getPhase(phaseIndex): Promise<ChallengePhase> {
// 	const status = await tournament.getPhase(phaseIndex);
// 	switch (status) {
// 		case 0:
// 			return ChallengePhase.NotStarted;
// 		case 1:
// 			return ChallengePhase.Staking;
// 		case 2:
// 			return ChallengePhase.Submission;
// 		case 3:
// 			return ChallengePhase.Computation;
// 		case 4:
// 			return ChallengePhase.Complete;
// 		default:
// 			return ChallengePhase.Unknown;
// 	}
// }

export async function downloadPhaseDataset(phaseIndex: number) {
	const datasetHash = await competition.getDatasetHash(phaseIndex);
	if (parseInt(datasetHash, 16) === 0) {
		console.error(`No dataset found for phase ${phaseIndex}.`);
	}

	// Download from IPFS. Browser will ask for a download confirmation.
	_download(datasetHash, 'zip');
}

export async function getAllowance() {
	// const caller = await provider.getSigner().getAddress();
  const caller = activeUser;
	return ethers.utils.formatEther(await token.allowance(caller, competition.address));
}

export async function increaseAllowance(amount: string) {
	const amountToIncreaseInInteger = ethers.utils.parseEther(amount);
	const txObj = await token.increaseAllowance(competition.address, amountToIncreaseInInteger);

	return provider.waitForTransaction(txObj['hash']);
}

export async function decreaseAllowance(amount: string) {
	const amountToDecreaseInInteger = ethers.utils.parseEther(amount);
	const txObj = await token.decreaseAllowance(competition.address, amountToDecreaseInInteger);

	// wait for the transaction to be mined and processed.
	return provider.waitForTransaction(txObj['hash']);
}

export async function getCurrentTotalStaked() {
	return ethers.utils.formatEther(await competition.getCurrentTotalStaked());
}

export async function grantPermission() {
	const txObj = await token.grantPermission(competition.address);
	return provider.waitForTransaction(txObj['hash']);
}

export async function revokePermission() {
	const txObj = await token.revokePermission(competition.address);
	return provider.waitForTransaction(txObj['hash']);
}

export async function getPermission() {
	return token.getPermission(competition.address);
}

export async function getStake() {
	// const caller = await provider.getSigner().getAddress();
  const caller = activeUser;
	return ethers.utils.formatEther(await competition.getStake(caller));
}

export async function getStakeThreshold() {
	return ethers.utils.formatEther(await competition.getStakeThreshold());
}


export async function increaseStake(amount: ethers.BigNumber) {
	const tx = await competition.increaseStake(amount);
	const promise = provider.waitForTransaction(tx['hash']);
	// await promise;
	return [tx, promise];
}

export async function decreaseStake(amount: ethers.BigNumber) {
	const tx = await competition.decreaseStake(amount);
	// console.log(tx);
	const promise = provider.waitForTransaction(tx['hash']);
	// console.log('------------------------------------------')
	// await t;
	// console.log(await provider.getTransactionReceipt(txObj.hash));
	return [tx, promise];
}

export async function getSubmissionHash(challengeNumber: number) {
  // const caller = await provider.getSigner().getAddress();
  const caller = activeUser;
	const hash = await competition.getSubmission(challengeNumber, caller);
	return parseInt(hash, 16) ? hash : null;
}

export async function makeSubmission(predictionsFile, pubKey) {
	// Encrypt, zip and upload to IPFS.
	const output = await _encryptZipUpload(predictionsFile, pubKey);
	const myCid = output[1];

	// Submit hash to blockchain.
	const txObj = await competition.submitNewPredictions(_cidToHash(myCid));
	const promise = provider.waitForTransaction(txObj['hash']);

  return [txObj, promise];
}

export async function redoSubmission(predictionsFile, pubKey) {
	const challengeNumber = await getLatestChallengeNumber();
	const submissionHash = await getSubmissionHash(challengeNumber);

	// Encrypt, zip and upload to IPFS.
	const output = await _encryptZipUpload(predictionsFile, pubKey);
	const myCid = output[1];

	// Submit hash to blockchain.
	const txObj = await competition.updateSubmission(submissionHash, _cidToHash(myCid));
  const promise = provider.waitForTransaction(txObj['hash']);

  return [txObj, promise];
}

export async function downloadOwnSubmission(challengeNumber: number) {
	const submissionHash = await getSubmissionHash(challengeNumber);
	if (parseInt(submissionHash, 16) === 0) {
		return null;
	}

	// Download from IPFS. Browser will ask for a download confirmation.
	return _download(submissionHash, 'zip');
}

export async function getResultsHash(phaseIndex: number) {
	const resultsHash = await competition.getResultsHash(phaseIndex);
	return (parseInt(resultsHash, 16) === 0)
		? "No results posted for this phase."
		: _hashToCid(resultsHash);
}

export async function downloadPhaseResults(phaseIndex: number) {
	const resultsHash = await competition.getResultsHash(phaseIndex);
	if (parseInt(resultsHash,16)==0){
		console.error("No results found for phase " + phaseIndex + ".");
		return null;
	}

	// Download from IPFS. Browser will ask for a download confirmation.
	await _retrieve(resultsHash);
}

export async function obtainMyHistoricalScores() {
	const [phases, results] = await _obtainOverallIpfs();
	if (phases === null) {
		// console.error("No results found for " + await provider.getSigner().getAddress() + ".");
    console.error("No results found for " + activeUser + ".");
		return [null, null];
	}

	return [phases, results];
}

export async function _obtainOverallIpfs() {
	const phaseIndex = await getLatestChallengeNumber();
	const resultsHash = await competition.getResultsHash(phaseIndex);

	if (parseInt(resultsHash, 16) === 0) {
		console.error("No results found for phase " + phaseIndex + ".");
		return [null, null]
	}

	const cid = _hashToCid(resultsHash);
	const url = GATEWAYS[4] + cid;
	const response = await fetch(url);
	const reader = response.body.getReader();

	let data = await reader.read();
	const decoder = new TextDecoder();
	let rows = decoder.decode(data.value).split('\n');
	// const activeUser = await provider.getSigner().getAddress();

	for (let i = 0; i < rows.length; i++) {
		const cols = rows[i].split(',');
		if (cols[1] === activeUser) {
			return await _obtainFromIndividualIpfs(cols[2]);
		}
	}

	while (!data.done) {
		data = await reader.read();
		rows = decoder.decode(data.value).split('\n');
		for (let i = 0; i < rows.length; i++) {
			let cols = rows[i].split(',');
			if (cols[1] === activeUser) {
				return await _obtainFromIndividualIpfs(cols[2]);
			}
		}
	}

	return [null, null]
}

export async function _obtainFromIndividualIpfs(cid: string) {
	const url = GATEWAYS[4] + cid;
	const response = await fetch(url);
	const reader = response.body.getReader();
	let data = await reader.read();
	const decoder = new TextDecoder();
	let rows = decoder.decode(data.value).split('\n');
	let cols;
	const phases = [];
	const scores = [];

	// skip first row of labels.
	for (let i = 1; i < rows.length; i++) {
		cols = rows[i].split(',');
		if (cols[1] !== null) {
			phases.push(cols[1]);
			scores.push(cols[2]);
		}
	}

	while (!data.done) {
		data = await reader.read();
		rows = decoder.decode(data.value).split('\n');
		for (let i = 0; i < rows.length; i++) {
			cols = rows[i].split(',');
			if (cols[1] !== null) {
				phases.push(cols[1]);
				scores.push(cols[2]);
			}
		}
	}
	if (!phases.length) {
		return [null, null]
	}
	return [phases, scores];
}



export class RciEvents {
	static listeners: { [key: string]: (() => void)[] } = {};

	static addListener(evt: string, listener: (() => void)) {
		if (!RciEvents.listeners[evt]) {
			console.log('adding event for '+ evt)
			RciEvents.listeners[evt] = [];
		}
		// TODO: check if the event is already there
		RciEvents.listeners[evt].push(listener)
	}

	// TODO add removeListener

	static emit(evt) {
		const listeners = RciEvents.listeners
		if (listeners && listeners[evt]) {
			listeners[evt].forEach(listener => listener());
		}
	}
}


// REWARDS AND SCORES

// function formatEther(fn: (n: number, p: string) => Promise<string>) {
// 	return (async (challengeNumber: number, participant: string = activeUser) => {
// 		const result = await fn(challengeNumber, participant);
// 		return ethers.utils.formatEther(result);
// 	});
// }
// 
// function formatEtherArray(fn: (s: number, e: number, p: string) => Promise<[string]>) {
// 	return (async (challengeNumberStart: number, challengeNumberEnd: number, participant: string = activeUser) => {
// 		const result = await fn(challengeNumberStart, challengeNumberEnd, participant);
// 		return result.map(ethers.utils.formatEther);
// 	});
// }
// export const getChallengeScores = formatEther(competition.getChallengeScores)
// export const getChallengeScoresList = formatEtherArray(competition.getChallengeScoresList)

export async function getChallengeScores(challengeNumber: number, participant = activeUser) {
	const result = await competition.getChallengeScores(challengeNumber, participant);
	return ethers.utils.formatEther(result);
}
export async function getChallengeScoresList(challengeNumberStart: number, challengeNumberEnd: number, participant = activeUser) {
	const result = await competition.getChallengeScoresList(challengeNumberStart, challengeNumberEnd, participant = activeUser);
	return result.map(ethers.utils.formatEther);
}
export async function getTournamentScores(challengeNumber: number, participant = activeUser) {
	const result = await competition.getTournamentScores(challengeNumber, participant);
	return ethers.utils.formatEther(result);
}
export async function getTournamentScoresList(challengeNumberStart: number, challengeNumberEnd: number, participant = activeUser) {
	const result = await competition.getTournamentScoresList(challengeNumberStart, challengeNumberEnd, participant);
	return result.map(ethers.utils.formatEther);
}
export async function getStakingRewards(challengeNumber: number, participant = activeUser) {
	const result = await competition.getStakingRewards(challengeNumber, participant);
	return ethers.utils.formatEther(result);
}
export async function getStakingRewardsList(challengeNumberStart: number, challengeNumberEnd: number, participant = activeUser) {
	const result = await competition.getStakingRewardsList(challengeNumberStart, challengeNumberEnd, participant);
	return result.map(ethers.utils.formatEther);
}
export async function getChallengeRewards(challengeNumber: number, participant = activeUser) {
	const result = await competition.getChallengeRewards(challengeNumber, participant);
	return ethers.utils.formatEther(result);
}
export async function getChallengeRewardsList(challengeNumberStart: number, challengeNumberEnd: number, participant = activeUser) {
	const result = await competition.getChallengeRewardsList(challengeNumberStart, challengeNumberEnd, participant);
	return result.map(ethers.utils.formatEther);
}
export async function getTournamentRewards(challengeNumber: number, participant = activeUser) {
	const result = await competition.getTournamentRewards(challengeNumber, participant);
	return ethers.utils.formatEther(result);
}
export async function getOverallRewards(challengeNumberStart: number, challengeNumberEnd: number, participant = activeUser) {
	const result = await competition.getOverallRewards(challengeNumberEnd, participant);
	return ethers.utils.formatEther(result);
	// return result.map(ethers.utils.formatEther);
}
// export async function getOverallRewardsList(challengeNumber: number, participant = activeUser) {
// 	const result = await competition.getOverallRewardsList(challengeNumber, participant);
// 	return ethers.utils.formatEther(result);
// }
export async function getOverallRewardsList(challengeNumberStart: number, challengeNumberEnd: number, participant = activeUser) {
	const result = await competition.getOverallRewardsList(challengeNumberStart, challengeNumberEnd, participant);
	return result.map(ethers.utils.formatEther);
}


// export class RciUtilities {
// 	static encoding: Encoding;
// 	static ethereum;
// 	static provider;
// 	static registry;
// 	static tournament;
// 	static token;

// 	constructor() {
// 		RciUtilities.encoding = new Encoding();
// 		RciUtilities.ethereum = window.ethereum
// 		RciUtilities.provider = new ethers.providers.Web3Provider(this.ethereum);
// 	}

// 	static async setup() {
// 		let tournamentAbi = await this.parseAbi('Tournament.json');
// 		let tokenAbi = await this.parseAbi('Token.json');
// 		let registryAbi = await this.parseAbi('Registry.json');

// 		this.registry = new ethers.Contract(REGISTRY_ADDR_DEFAULT, registryAbi, this.provider);

// 		let tournamentAddress = await this.getTournamentAddress();
// 		let tokenAddress = await this.getTokenAddress();

// 		this.tournament = new ethers.Contract(tournamentAddress, tournamentAbi, this.provider);
// 		this.token = new ethers.Contract(tokenAddress, tokenAbi, this.provider);
// 	}

// 	// Call this to set the current sending account.
// 	refresh() {
// 		this.tournament = this.tournament.connect(this.provider.getSigner());
// 		this.token = this.token.connect(this.provider.getSigner());
// 	}

// 	async connect() {
// 		await this.getChainName();
// 		await this.getActiveUser();
// 		this.refresh();
// 	}

// 	// The following are functions to read general information from the smart contract.
// 	async getTournamentPool() {
// 		return ethers.utils.formatEther(await this.tournament.getTournamentPool());
// 	}

// 	async getCurrentTotalStaked() {
// 		return ethers.utils.formatEther(await this.tournament.getCurrentTotalStaked());
// 	}

// 	async getTotalStakesLockedForPhase(phaseIndex) {
// 		return ethers.utils.formatEther(await this.tournament.getTotalStakesLockedForPhase(phaseIndex));
// 	}

// 	async getCurrentParticipationRewardsBudget() {
// 		return ethers.utils.formatEther(await this.tournament.getCurrentParticipationRewardsBudget());
// 	}

// 	async getCurrentPerformanceRewardsBudget() {
// 		return ethers.utils.formatEther(await this.tournament.getCurrentPerformanceRewardsBudget());
// 	}

// 	async getLastPhaseIndex() {
// 		return await this.tournament.getLastPhaseIndex();
// 	}

// 	async getStakeThreshold() {
// 		return ethers.utils.formatEther(await this.tournament.getStakeThreshold());
// 	}

// 	async getTokenName() {
// 		return await this.token.name();
// 	}

// 	async getTokenSymbol() {
// 		return await this.token.symbol();
// 	}

// 	async getTokenAddress() {
// 		return await this.registry.getTokenAddress();
// 	}

// 	async getTournamentAddress() {
// 		return await this.registry.getTournamentAddress(TOURNAMENT_NAME);
// 	}

// 	// The following are functions that read information from the smart contract but require at least one input.

// 	async getPhaseStatus(phaseIndex) {
// 		let status = await this.tournament.getPhaseStatus(phaseIndex);
// 		switch (status){
// 			case 0:
// 				return "Phase has not started.";
// 			case 1:
// 				return "Phase is in STAKING mode.";
// 			case 2:
// 				return "Phase is in SUBMISSION mode.";
// 			case 3:
// 				return "Phase is in COMPUTATION mode.";
// 			case 4:
// 				return "Phase is COMPLETE."
// 			default:
// 				return "Phase is in UNKNOWN mode."
// 		}
// 	}

// 	async getPhaseDatasetHash(phaseIndex) {
// 		let datasetHash = await this.tournament.getPhaseDatasetHash(phaseIndex);
// 		return (parseInt(datasetHash,16)==0) ? "No dataset posted for this phase." : this.hashToCid(datasetHash);
// 	}

// 	async getPhaseResultsHash(phaseIndex) {
// 		let resultsHash = await this.tournament.getPhaseResultsHash(phaseIndex);
// 		return (parseInt(resultsHash,16)==0) ? "No results posted for this phase." : this.hashToCid(resultsHash);
// 	}

// 	async getPhaseSubmissionCounter(phaseIndex) {
// 		return await this.tournament.getPhaseSubmissionCounter(phaseIndex);
// 	}

// 	// The following are functions to read information from the smart contract specific to the current active user.
// 	async getStake() {
// 		let caller = await this.provider.getSigner().getAddress();
// 		return ethers.utils.formatEther(await this.tournament.getStake(caller));
// 	}

// 	async getSubmission(phaseIndex) {
// 		let caller = await this.provider.getSigner().getAddress();
// 		let submissionHash = await this.tournament.getSubmission(phaseIndex, caller);
// 		return (parseInt(submissionHash,16)==0) ? "No submissions made for this phase." : this.hashToCid(submissionHash);
// 	}

// 	async getAllowance() {
// 		let caller = await this.provider.getSigner().getAddress();
// 		return ethers.utils.formatEther(await this.token.allowance(caller, this.tournament.address));
// 	}

// 	// The following are write functions. They will induce a Metamask pop-up for the user to confirm the transaction and set the gas amount if desired.

// 	async increaseAllowance(amountToIncreaseInFloat) {
// 		// amountToIncreaseInFloat = document.getElementById('testInput').value;
// 		let amountToIncreaseInInteger = ethers.utils.parseEther(amountToIncreaseInFloat);
// 		let txObj = await this.token.increaseAllowance(this.tournament.address, amountToIncreaseInInteger);
		
// 		// wait for the transaction to be mined and processed.
// 		await this.provider.waitForTransaction(txObj['hash']);
// 	}

// 	async decreaseAllowance(amountToDecreaseInFloat) {
// 		let amountToDecreaseInInteger = ethers.utils.parseEther(amountToDecreaseInFloat);
// 		let txObj = await this.token.decreaseAllowance(this.tournament.address, amountToDecreaseInInteger);
		
// 		// wait for the transaction to be mined and processed.
// 		await this.provider.waitForTransaction(txObj['hash']);
// 	}


// 	async increaseStake(amountToIncreaseInFloat) {
// 		// amountToIncreaseInFloat = document.getElementById('testInput').value;
// 		let amountToIncreaseInInteger = ethers.utils.parseEther(amountToIncreaseInFloat);
// 		let txObj = await this.tournament.increaseStake(amountToIncreaseInInteger);

// 		// wait for the transaction to be mined and processed.
// 		await this.provider.waitForTransaction(txObj['hash']);
// 	}

// 	async decreaseStake(amountToDecreaseInFloat) {
// 		let amountToDecreaseInInteger = ethers.utils.parseEther(amountToDecreaseInFloat);
// 		let txObj = await this.tournament.decreaseStake(amountToDecreaseInInteger);
		
// 		// wait for the transaction to be mined and processed.
// 		await this.provider.waitForTransaction(txObj['hash']);
// 	}

// 	async transferStake(recipient, amountToTransferInFloat) {
// 		let amountToTransferInInteger = ethers.utils.parseEther(amountToTransferInFloat);
// 		let txObj = await this.tournament.transferStake(recipient, amountToTransferInInteger);
		
// 		// wait for the transaction to be mined and processed.
// 		await this.provider.waitForTransaction(txObj['hash']);
// 	}

// 	// The following read the the IPFS cid from the smart contract, then retrieves data from IPFS.
// 	// `download` functions: downloads either .zip or .csv files from IPFS.
// 	// `obtain` functions: obtains data from IPFS and returns data as js arrays or js strings.

// 	async downloadPhaseDataset(phaseIndex) {
// 		let datasetHash = await this.tournament.getPhaseDatasetHash(phaseIndex);
// 		if (parseInt(datasetHash,16)==0){
// 			console.error("No dataset found for phase " + phaseIndex + ".");
// 			return null;
// 		}

// 		// Download from IPFS. Browser will ask for a download confirmation.
// 		await this.retrieve(datasetHash);
// 	}

// 	async downloadPhaseResults(phaseIndex) {
// 		let resultsHash = await this.tournament.getPhaseResultsHash(phaseIndex);
// 		if (parseInt(resultsHash,16)==0){
// 			console.error("No results found for phase " + phaseIndex + ".");
// 			return null;
// 		}

// 		// Download from IPFS. Browser will ask for a download confirmation.
// 		await this.retrieve(resultsHash);
// 	}

// 	async obtainMyHistoricalScores() {
// 		let output = await this.obtainOverallIpfs();
// 		let phases = output[0];
// 		let results = output[1];
// 		if (phases == null){
// 			console.error("No results found for "+ await this.provider.getSigner().getAddress() + ".");
// 			return [null, null]
// 		}
// 		return [phases, results];
// 	}

// 	async obtainOverallIpfs() {
// 		let phaseIndex = await this.tournament.getLastPhaseIndex();
// 		let resultsHash = await this.tournament.getPhaseResultsHash(phaseIndex);
// 		if (parseInt(resultsHash,16)==0){
// 			console.error("No results found for phase " + phaseIndex + ".");
// 			return [null, null]
// 		}
// 		let cid = this.hashToCid(resultsHash);
// 		let url = GATEWAYS[0] + cid;
// 		let response = await fetch(url);
// 		let reader = response.body.getReader();
		
// 		let data = await reader.read();
// 		let decoder = new TextDecoder();
// 		let rows = decoder.decode(data.value).split('\n');
// 		let cols;
// 		let activeUser = await this.provider.getSigner().getAddress();

// 		for (let i=0; i < rows.length; i++){
// 			cols = rows[i].split(',');
// 			if (cols[1] == activeUser){
// 				return await this.obtainFromIndividualIpfs(cols[2]);
// 			}
// 		}

// 		while (!data.done){
// 			data = await reader.read();
// 			rows = decoder.decode(data.value).split('\n');
// 			for (let i=0; i < rows.length; i++){
// 				cols = rows[i].split(',');
// 				if (cols[1] == activeUser){
// 					return await this.obtainFromIndividualIpfs(cols[2]);
// 				}
// 			}
// 		}

// 		return [null, null]
// 	}

// 	async obtainFromIndividualIpfs(cid) {
// 		let url = GATEWAYS[0] + cid;
// 		let response = await fetch(url);
// 		let reader = response.body.getReader();
// 		let data = await reader.read();
// 		let decoder = new TextDecoder();
// 		let rows = decoder.decode(data.value).split('\n');
// 		let cols;
// 		let phases = [];
// 		let scores = [];

// 		//skip first row of labels.
// 		for (let i=1; i < rows.length; i++){
// 			cols = rows[i].split(',');
// 			if (cols[1] != null){
// 				phases.push(cols[1]);
// 				scores.push(cols[2]);
// 			}
// 		}

// 		while (!data.done){
// 			data = await reader.read();
// 			rows = decoder.decode(data.value).split('\n');
// 			for (let i=0; i < rows.length; i++){
// 				cols = rows[i].split(',');
// 				if (cols[1] != null){
// 					phases.push(cols[1]);
// 					scores.push(cols[2]);
// 				}
// 			}
// 		}
// 		if (phases.length == 0){
// 			return [null, null]
// 		}
// 		return [phases, scores];
// 	}

// 	async obtainRules() {
// 		let rulesHash = await this.registry.getTournamentRulesLocation(this.TOURNAMENT_NAME);
// 		if (parseInt(rulesHash,16)==0){
// 			return "No rules published for " + TOURNAMENT_NAME + ".";
// 		}
// 		let rulesCid = this.hashToCid(rulesHash);
// 		let url = GATEWAYS + rulesCid;
// 		let response = await fetch(url);
// 		let reader = response.body.getReader();
// 		let data = await reader.read();
// 		let decoder = new TextDecoder();
// 		let text = decoder.decode(data.value);

// 		while (!data.done){
// 			data = await reader.read();
// 			text += decoder.decode(data.value);
// 		}

// 		return text;
// 	}
 
// 	// The following functions take files from the user input, processes them and uploads them to IPFS, then sends a blockchain transaction to write the IPFS cid to the smart contract.

// 	// async makeSubmission() {

// 	// 	let predictionsFile = document.getElementById("predictionsFile").files[0];
// 	// 	let pubKeyFile = document.getElementById("pubKeyFile").files[0];

// 	// 	// Encrypt, zip and upload to IPFS.
// 	// 	let output = await this.encryptZipUpload(predictionsFile, pubKeyFile);
// 	// 	let myCid = output[1];
// 	// 	console.log(myCid);

// 	// 	// Submit hash to blockchain.
// 	// 	let txObj =  await this.tournament.submitNewPhasePredictions(this.cidToHash(myCid));

// 	// 	// wait for the transaction to be mined and processed.
// 	// 	await this.provider.waitForTransaction(txObj['hash']);
// 	// }


// 	// async redoSubmission() {

// 	// 	let predictionsFile = document.getElementById("predictionsFile").files[0];
// 	// 	let pubKeyFile = document.getElementById("pubKeyFile").files[0];
// 	// 	let oldCidString = document.getElementById("testInput").value;

		
// 	// 	// Encrypt, zip and upload to IPFS.
// 	// 	let output = await this.encryptZipUpload(predictionsFile, pubKeyFile);
// 	// 	let myCid = output[1];

// 	// 	// Submit hash to blockchain.
// 	// 	let txObj =  await this.tournament.updatePhaseSubmission(this.cidToHash(oldCidString), this.cidToHash(myCid));
		
// 	// 	// wait for the transaction to be mined and processed.
// 	// 	await this.provider.waitForTransaction(txObj['hash']);
// 	// }


// 	/* ***********************************
// 	The following are helper functions for the above blockchain and IPFS interaction functions.
// 	*********************************** */
	
// 	isMetaMaskInstalled() {
// 		const { ethereum } = window;
// 		return Boolean(ethereum && ethereum.isMetaMask);
// 	  };

// 	async getActiveUser() {
// 		if (this.isMetaMaskInstalled()){
// 			await window.ethereum.request({ method: 'eth_requestAccounts' });
// 		}
// 		this.activeUser = await this.provider.getSigner().getAddress();
// 	}

// 	async getChainName() {
// 		let chainId = await window.ethereum.request({ method: 'eth_chainId' });
// 		let chainName;
// 		if (chainId == 1){
// 			chainName = 'MAINNET';
// 		}else if(chainId == 3){
// 			chainName = 'Ropsten Test';
// 		}
// 		else if (chainId == 4){
// 			chainName = 'Rinkeby Test';
// 		}
// 		else if (chainId == 42){
// 			chainName = 'Kovan Test';
// 		}
// 		else{
// 			chainName = 'Unknown Network';
// 		}

// 		this.chainName = chainName;
// 	}

// 	async parseAbi(filename) {
// 		let response = await fetch('/contracts/' + filename);
// 		response = await response.json();
// 		let abi = response['abi'];
// 		return abi;
// 	}

// 	cidToHash(cid) {
// 		let res = this.encoding.byteToHexString(this.encoding.b58ToByte(cid));
// 		return "0x" + res.slice(4)

// 	}
	
// 	hashToCid(hash) {
// 		if (hash && hash.byteLength !== undefined) {
// 			hash = this.encoding.byteToHexString(hash);
// 		}
// 		if (hash.slice(0,2) == '0x') hash = hash.slice(2);
// 		hash = '1220' + String(hash)
// 		return this.encoding.byteToB58(this.encoding.hexStringToByte(hash));
// 	}

// 	async encryptZipUpload(predictionsFile, pubKeyFile) {
// 		const formData = new FormData();

// 		let predictionsData = await predictionsFile.arrayBuffer();
// 		let predictionsName = predictionsFile.name;

// 		let symmetricKey = await this.generateSymmetricKey();
// 		let iv = this.getIV(16);
// 		let encryptedPredictions = await this.encryptPredictions(predictionsData, symmetricKey, iv);

// 		encryptedPredictions = new Uint8Array(encryptedPredictions);
// 		let predictionsPayload = this.appendBuffer(iv, encryptedPredictions);

// 		let originator = await this.provider.getSigner().getAddress();
// 		let originatorData = (new TextEncoder).encode(originator);
// 		let encryptedOriginator = await this.encryptPredictions(originatorData, symmetricKey, iv);
// 		let originatorPayload = this.appendBuffer(iv, encryptedOriginator);


// 		let pubKeyData = await this.importRsaPublicKey(await pubKeyFile.text());
// 		let wrapKeyResult = await this.wrapSymmetricKey(symmetricKey, pubKeyData);

// 		let zip = new JSZip();
// 		zip.file(predictionsName.split(".")[0]+".bin", predictionsPayload);
// 		zip.file("originator.bin", originatorPayload);
// 		zip.file("encrypted_symmetric_key.pem", wrapKeyResult);
		
// 		let content = await zip.generateAsync({
// 			type: 'blob',
// 			compression: "DEFLATE",
// 			compressionOptions: {
// 				level: 3
// 			}});
// 		formData.append('blob', content);
		
// 		let response = await this.submitIpfs(formData);
// 		let myCid = response['Hash']
// 		let responseAlert = "IPFS: File of size " + response['Size'] + " bytes uploaded to IPFS with CID " + myCid + '.<br> Downloadable <a href="https://ipfs.io/ipfs/' + myCid + '">link</a>.';
// 		responseAlert = '<p class="info-text alert alert-primary">' + responseAlert + '</p>';
// 		return [responseAlert, myCid];
// 	}

// 	async submitIpfs(fileToSubmit) {
// 		const url = 'https://ipfs.infura.io:5001/api/v0/add';
// 		let response = await fetch(url, { method: 'POST', body: fileToSubmit});
// 		return await response.json();
// 	}

// 	async retrieve(hash) {
// 		let cid = this.hashToCid(hash);
// 		let gateway = GATEWAYS[0];

// 		let request = new Request(gateway + cid);
// 		let response = await fetch(request);
// 		let blob = await response.blob();
// 		if (response.ok){
// 			let ext = blob['type'].split("/")[1];
// 			if (ext!='zip'){
// 				ext = 'csv';
// 			}
// 			let a = document.createElement("a");
// 			let url = URL.createObjectURL(blob);
// 			a.href = url;
// 			let filename = cid.slice(0,9) + '.' + ext;
// 			a.download = filename;
// 			document.body.appendChild(a);
// 			a.click();
// 		}else{
// 			console.error('File not found.');
// 			return;
// 		}
// 	}
	
// 	/* ***********************************
// 	The following are functions and classes that help to perform encryption.
// 	*********************************** */

// 	async generateSymmetricKey() {
// 		let key = await window.crypto.subtle.generateKey(
// 			{
// 			  name: "AES-GCM",
// 			  length: 256
// 			},
// 			true,
// 			["encrypt", "decrypt"]
// 		  );
// 		return key;
// 	}

// 	getIV(size) {
// 		return window.crypto.getRandomValues(new Uint8Array(size));
// 	}

// 	async encryptPredictions(data, key, iv) {
// 		// let iv = window.crypto.getRandomValues(new Uint8Array(12));
// 		return await window.crypto.subtle.encrypt(
// 			{
// 			  name: "AES-GCM",
// 			  iv: iv,
// 			  tagLength: 128,

// 			},
// 			key,
// 			data
// 		  );
// 	}

// 	async wrapSymmetricKey(symmetricKey, publicKey) {
// 		let wrapKeyResult = await window.crypto.subtle.wrapKey(
// 			"raw",
// 			symmetricKey,
// 			publicKey,
// 			publicKey.algorithm.name
// 		);

// 		return new Uint8Array(wrapKeyResult)
// 	}

// 	str2ab(str) {
// 		const buf = new ArrayBuffer(str.length);
// 		const bufView = new Uint8Array(buf);
// 		for (let i = 0, strLen = str.length; i < strLen; i++) {
// 		  bufView[i] = str.charCodeAt(i);
// 		}
// 		return buf;
// 	  }

// 	async importRsaPublicKey(pem) {
// 		// fetch the part of the PEM string between header and footer
// 		const pemHeader = "-----BEGIN PUBLIC KEY-----";
// 		const pemFooter = "-----END PUBLIC KEY-----";
// 		const pemContents = pem.substring(pemHeader.length, pem.length - pemFooter.length);
// 		// base64 decode the string to get the binary data
// 		const binaryDerString = window.atob(pemContents);
// 		// convert from a binary string to an ArrayBuffer
// 		const binaryDer = this.str2ab(binaryDerString);
	  
// 		return await window.crypto.subtle.importKey(
// 			"spki",
// 			binaryDer,
// 			{
// 			  name: "RSA-OAEP",
// 			  hash: "SHA-1"
// 			},
// 			true,
// 			["wrapKey","encrypt"]
// 		  );
// 		}

// 	appendBuffer(buffer1, buffer2 ) {
// 		var tmp = new Uint8Array( buffer1.byteLength + buffer2.byteLength );
// 		tmp.set( new Uint8Array( buffer1 ), 0 );
// 		tmp.set( new Uint8Array( buffer2 ), buffer1.byteLength );
// 		return tmp.buffer;
// 	}

// 	async exportCryptoKey(key) {
// 		const exported = await window.crypto.subtle.exportKey(
// 		  "raw",
// 		  key
// 		);
// 		const exportedKeyBuffer = new Uint8Array(exported);
// 		return exportedKeyBuffer;
// 		// let enc = new TextEncoder();
// 		// return enc.encode(exported);
// 	  }

// 	async encryptSymmetricKey(symmetricKey, publicKey) {
// 		return await window.crypto.subtle.encrypt({ name: "RSA-OAEP" }, publicKey, symmetricKey);
// 	}
// }
