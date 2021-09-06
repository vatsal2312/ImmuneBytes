// define known addresses.

const rci = new RciUtilities();
const { ethereum } = window;

const initialize = async () => {

    await rci.setup();
    rci.refresh();

    // Listeners
    ethereum.on('chainChanged', rci.getChainName);
    ethereum.on('accountsChanged', rci.refresh);
    ethereum.on('connect', rci.connect);

    // For testing

    testButton.onclick = rci.makeSubmission;

    let tournamentName = rci.TOURNAMENT_NAME;
    console.log(await rci.getTournamentAddress())
    console.log(await rci.getTokenName());
    console.log(await rci.getTokenSymbol());
    console.log(await rci.getTournamentPool());
    console.log(await rci.obtainRules());
    console.log(await rci.getStake());
    console.log(await rci.getStakeThreshold())

    let phaseIndex = await rci.getLastPhaseIndex()
    console.log(phaseIndex);

    console.log(await rci.obtainMyHistoricalScores());

    await rci.downloadPhaseDataset(phaseIndex);
};


window.addEventListener('DOMContentLoaded', initialize);


