import { writable, derived } from 'svelte/store';
import * as utils from './utilities.js';

export const loaded = writable(false);

export const tournamentName    = writable(utils.getTournamentName());
export const tournamentAddress = writable(null);
export const tournamentPool    = writable(null);
export const submissionCounter = writable(null);
export const totalStake        = writable(null);
export const permission        = writable(null);
export const stake             = writable(null);
export const challenge         = writable(null);
export const phase             = writable(null);
export const submissionHash    = writable(null);
export const competitionKey    = writable(null);
// export const phaseStatus: utils.PhaseStatus = null;

// Scores and rewards
export const challengeScoresList  = writable(null)
export const tournamentScoresList = writable(null)
export const stakingRewardsList   = writable(null)
export const challengeRewardsList = writable(null)
export const tournamentRewards    = writable(null)
export const overallRewardsList   = writable(null)

const storedTransactions = localStorage.getItem("transactions") || "{}";

export const transactions = writable(JSON.parse(storedTransactions));
transactions.subscribe(value => {
  localStorage.setItem("transactions", JSON.stringify(value));
});

export const newNotifications = derived(
	transactions,
	$transactions => Object.values($transactions).some(t => t['new'])
);



export async function setup() {
	const challengeNumber = await utils.getLatestChallengeNumber();
	challenge.set(challengeNumber);

	return Promise.all([
		utils.getCompetitionAddress(),
		utils.getCompetitionPool(),
		utils.getSubmissionCounter(challengeNumber),
		utils.getPhase(challengeNumber),
		utils.getPermission(),
		utils.getCurrentTotalStaked(),
		utils.getStake(),
		utils.getSubmissionHash(challengeNumber),

		utils.downloadCompetitionKey(challengeNumber)
	]).then(async results => {
		tournamentAddress.set(results[0]);
		tournamentPool.set(results[1]);
		submissionCounter.set(results[2]);
		phase.set(results[3]);
		permission.set(results[4]);
		totalStake.set(results[5])
		stake.set(results[6]);
		submissionHash.set(results[7]); // TODO: only set if in submission status?

		competitionKey.set(results[8]);

		loaded.set(true);
	});
}

export async function getScoresAndRewards(challengeNumber: number) {
	return Promise.all([
		// utils.getChallengeScores(challengeNumber),
		utils.getChallengeScoresList(1, challengeNumber),
		// utils.getTournamentScores(challengeNumber),
		utils.getTournamentScoresList(1, challengeNumber),
		// utils.getStakingRewards(challengeNumber),
		utils.getStakingRewardsList(1, challengeNumber),
		// utils.getChallengeRewards(challengeNumber),
		utils.getChallengeRewardsList(1, challengeNumber),
		utils.getTournamentRewards(challengeNumber),
		// TODO: check why getOverallRewards is different from last value in getOverallRewardsList
		// utils.getOverallRewards(1, challengeNumber),
		utils.getOverallRewardsList(1, challengeNumber)
	]).then(indicators => {
		challengeScoresList.set(indicators[0]);
		tournamentScoresList.set(indicators[1]);
		stakingRewardsList.set(indicators[2]);
		challengeRewardsList.set(indicators[3]);
		tournamentRewards.set(indicators[4]);
		overallRewardsList.set(indicators[5]);
	});
}
