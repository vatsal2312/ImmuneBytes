<script lang="ts">
  import { onMount } from 'svelte';

  import { ethers } from "ethers";

  import * as utils from './utilities';
  import {
    setup,
    getScoresAndRewards,

    loaded,
    tournamentName,
    // tournamentAddress,
    tournamentPool,
    submissionCounter,
    totalStake,
    permission,
    stake,
    challenge,
    phase,
    submissionHash,
    transactions,
    newNotifications,
    competitionKey,

    challengeScoresList,
    tournamentScoresList,
    stakingRewardsList,
    challengeRewardsList,
    tournamentRewards,
    overallRewardsList,
  } from './stores.js';

  
  // import Notifications from './Notifications.svelte'
  import Steps from './steps/Steps.svelte'
  // import AllowancePopup from './AllowancePopup.svelte'
  import StakingPopup from './StakingPopup.svelte'
  import FileUploadPopup from './FileUploadPopup.svelte'
  import TransactionsPopup from './TransactionsPopup.svelte'
  import ScoresTable from './ScoresTable.svelte';
  import { init } from 'svelte/internal';
  
  // const baseEtherAddr = "https://ropsten.etherscan.io/address/";
	
  let installWarning = false;

  let stakingPopup        = false;
  let updatingStake       = false;
  let predictionPopup     = false;
  let uploadingPrediction = false
  let showTransactions    = false;

  const prevPhase = $phase

  const refreshGui = async function() {
    if (loaded) {
      let gui = false;
      while (!gui) {
        try {
          // TODO: cleanup
          // await utils.setup(); // TODO: call refreshGui here
          await setup().then(async () => {
            // utils.grantPermission();
            if (!$challengeScoresList || (prevPhase !== $phase && $phase === 3)) {
              await getScoresAndRewards($challenge);
            }
          }
        )
          gui = true;
        } catch (error) {
          console.log('Error with gui setup - retrying');
        }
        await (() => new Promise(resolve => setTimeout(resolve, 1000)))();
      }
    }

    // return setup().then(async () => {
    //     // alert();
    //     // utils.grantPermission();
    //     // Get scores and rewards if not done yet
    //     if (!$challengeScoresList) {
    //       getScoresAndRewards($challenge);
    //     }
    //     // Or if new ones just made available
    //     if (prevPhase !== $phase && $phase === 3) {
    //       getScoresAndRewards($challenge);
    //       // TODO catch
    //     }
    //   }
    // );
    // console.log(await utils.downloadOwnSubmission(2));
  }

  setInterval(refreshGui, 6e4);
  utils.RciEvents.addListener('EthAccountChanged', async () => {
    // TODO make them parallel
    await refreshGui();
  });

  onMount(async () => {
    try {
      utils.init();
    } catch (err) {
      console.log(err);
      installWarning = true;
      return;
    }
    

    let setup = false;
    while (!setup) {
      try {
        await utils.setup(); // TODO: call refreshGui here
        setup = true;
      } catch (error) {
        console.log(error)
        // console.log('Error with setup - retrying');
        installWarning = true;
        return; // TODO
      }
    }
		// TODO - check if not connected - why there's rci.ethereum.on('connect', rci.connect); below?

    // try {
    //   await utils.setup();
    // } catch (error) {
    //   installWarning = true;
    //   return;
    // }

    let connected = false;
    while (!connected) {
      try {
        await utils.connect();
        connected = true;
      } catch (error) {
        console.log('Error with connect - retrying');
      }
      await (() => new Promise(resolve => setTimeout(resolve, 1000)))();
    }
	});

  async function addToken() {
    console.log(await Promise.all([utils.addToken(), utils.switchNetwork()]));
  }

  function showStakingPopup(show: boolean) {
    stakingPopup = show;
  }

  async function grantPermission() {
    utils.grantPermission().then(result => {
      console.log(result)
      $permission = true;
    });
  }

  async function updateStake(event) {
    showStakingPopup(false);

    const difference = event.detail.difference;
    if (difference.isZero()) return;

    let promise: Promise<any>; // TODO: Promise.transactionReceipt or a wrapper
    if (difference.gt(0)) {
      promise = utils.increaseStake(difference);
    } else {
      promise = utils.decreaseStake(difference.mul(ethers.constants.NegativeOne))
    }
    updatingStake = true;

    return promise.then(async ([tx, receiptPromise]) => {
      // TODO move this to stores.js
      transactions.update(t => {
        t[tx.hash] = {};
        t[tx.hash].description = `${difference.gt(0) ? 'Increase' : 'Decrease'} stake by ${ethers.utils.formatEther(difference)}`;
        return t;
      });
      const receipt = await(receiptPromise);
      // console.log(receipt);
      transactions.update(t => {
        t[tx.hash].new = true;
        t[tx.hash].from = receipt.from;
        t[tx.hash].to = receipt.to;
        t[tx.hash].timestamp = Date.now();
        return t;
      });

      refreshGui(); // TODO - only refresh stake
    }).catch(err => {
      alert(err.message);
      console.log(err); // TODO show error
    }).finally(() => {
      updatingStake = false
    })
  }

  function showUploadPopup(show: boolean) {
    predictionPopup = show;
  }

  function _uploadSubmission(updateFn, {detail: {predictionFile}}) {
    showUploadPopup(false);
    uploadingPrediction = true;
    const promise = updateFn(predictionFile, $competitionKey)
    
    return promise.then(async([tx, receiptPromise]) => {
      // TODO: notify user
      const receipt = await(receiptPromise);
      // TODO store in log
      refreshGui(); // TODO - only refresh stake
      receiptPromise.then(() => alert('Upload completed'))
    }).catch(error => {
      // TODO: notify user
      console.log(error)
      alert(error.data.message || error.data.details);
    }).finally(() => uploadingPrediction = false);
  }

  const uploadSubmission = evt => _uploadSubmission(utils.makeSubmission, evt);

  const reUploadSubmission = evt => _uploadSubmission(utils.redoSubmission, evt);

  function downloadOwnSubmission() {
    utils.downloadOwnSubmission($challenge);
  }

  function showTransactionsPopup() {
    showTransactions = true;
    const newTransactions = {};
    for (const [key, value] of Object.entries($transactions)) {
      newTransactions[key] = value;
      newTransactions[key].new = false;
    }
    transactions.set(newTransactions);
  }
</script>

<!--
  This example requires Tailwind CSS v2.0+ 
  
  This example requires some changes to your config:
  
  ```
  // tailwind.config.js
  const colors = require('tailwindcss/colors')
  
  module.exports = {
    // ...
    theme: {
      extend: {
        colors: {
          sky: colors.sky,
          teal: colors.teal,
          cyan: colors.cyan,
          rose: colors.rose,
        }
      }
    },
    plugins: [
      // ...
      require('@tailwindcss/forms'),
      require('@tailwindcss/line-clamp'),
    ]
  }
  ```
-->

{#if installWarning}
  <div class="bg-indigo-700">
    <div class="max-w-2xl mx-auto text-center py-16 px-4 sm:py-20 sm:px-6 lg:px-8">
      <h2 class="text-3xl font-extrabold text-white sm:text-4xl">
        <span class="block">Welcome to the RCI competition platform.</span>
        <span class="block">Start competing today.</span>
      </h2>
      <p class="mt-4 text-lg leading-6 text-indigo-200">You need to install Metamask to be able to participate.</p>
      <a href="https://metamask.io/download.html" target="_blank" class="mt-8 w-full inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-indigo-50 sm:w-auto">
        Install metamask
      </a>
      <p class="mt-4 text-lg leading-6 text-indigo-200">After installing MetaMask, please
        <a target="_blank" href="https://polygonscan.com/" class="underline">switch to the Polygon network</a> and reload this page.</p>
    </div>
  </div>
{/if}

<!-- <div class:hidden={$loaded}>
  Please wait...
</div> -->

<div class:hidden={!$loaded} class="min-h-screen bg-gray-100">
  <!-- <AllowancePopup allowance={$allowance} on:submit={updateAllowance} on:cancel={() => showAllowancePopup(false)} show={allowanceEditing}></AllowancePopup> -->
  <StakingPopup permission={$permission}
                stake={$stake}
                on:grantPermission={grantPermission}
                on:submit={updateStake}
                on:cancel={() => showStakingPopup(false)}
                show={stakingPopup}></StakingPopup>
  <FileUploadPopup on:submit={!$submissionHash ? uploadSubmission : reUploadSubmission} on:cancel={() => showUploadPopup(false)} show={predictionPopup}></FileUploadPopup>
  <TransactionsPopup show={showTransactions}></TransactionsPopup>

  <header class="pb-24">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:max-w-5xl__ lg:px-8__">
      <div class="h-20 relative flex flex-wrap items-center justify-between">
        <!-- Logo -->
        <div class="left-0 py-5 flex-shrink-0 static">
					<span class="sr-only">Rocket Capital Investment</span>
					<!-- https://tailwindui.com/img/logos/workflow-mark-cyan-200.svg -->
					<svg xmlns="http://www.w3.org/2000/svg" width="41.278" height="30.958" viewBox="0 0 41.278 30.958"><rect width="14.594" height="14.594" transform="translate(0 20.639) rotate(-45)" fill="#45adf7"/><rect width="14.594" height="14.594" transform="translate(10.319 10.319) rotate(-45)" fill="#0328d2"/><rect width="14.594" height="14.594" transform="translate(20.64 20.639) rotate(-45)" fill="#6428ee"/></svg>
        </div>





        <!-- Right section on desktop -->
        <!-- <div class="hidden lg:ml-4 lg:flex lg:items-center lg:py-5 lg:pr-0.5"> -->
        <div class="ml-4 flex items-center py-5 pr-0.5">
          <div class="px-6 py-5 text-sm font-medium text-center">
            <span class="text-gray-600">Tot. submissions:</span>
            <span class="text-gray-900">{$submissionCounter}</span>
          </div>
          <div class="px-6 py-5 text-sm font-medium text-center">
            <span class="text-gray-600">Tot. stake:</span>
            <span class="text-gray-900">{parseFloat($totalStake).toFixed(6)}</span>
          </div>
          <div class="px-6 py-5 text-sm font-medium text-center">
            <span class="text-gray-600">Pool:</span>
            <span class="text-gray-900">{parseFloat($tournamentPool).toFixed(6)}</span>
          </div>

          <button on:click={showTransactionsPopup} type="button" class="relative">
            <!-- Heroicon name: outline/bell -->
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 transform hover:rotate-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
            {#if $newNotifications}
              <span class="absolute -right-0 -top-0 rounded-full bg-red-600 w-2 h-2 top right p-0 m-0 text-white font-mono text-sm  leading-tight text-center"></span>
            {/if}
          </button>
        </div>
      </div>
    </div>
  </header>
  <main class="-mt-24 pb-8">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:max-w-5xl__ lg:px-8__">
      <h1 class="sr-only">Profile</h1>

      <!-- Main 3 column grid -->
      <div class="grid grid-cols-1 gap-4 items-start lg:grid-cols-3_ lg:gap-8">
        <!-- Left column -->
        <div class="grid grid-cols-1 gap-4 lg:col-span-2_">
          <!-- Welcome panel -->
          <section aria-labelledby="profile-overview-title">
            <div class="rounded-lg bg-white overflow-hidden shadow">
              <h2 class="sr-only" id="profile-overview-title">Competition Overview</h2>
              <div class="bg-white p-6">
                <div class="sm:flex sm:items-center sm:justify-between">
                  <div class="sm:flex sm:space-x-5">
                    <div class="mt-4 text-center sm:mt-0 sm:pt-1 sm:text-left">
                      <p class="text-xl font-bold text-gray-900 sm:text-2xl">{$tournamentName} Competition</p>
                      <p class="font-bold text-purple-600">Challenge {$challenge}</p>
                      <button on:click={addToken} type="button" class="inline-flex items-center px-2 py-1 mt-2 border shadow-sm text-base font-medium rounded-md text-black bg-gray-50 hover:bg-gray-100 focus:outline-none "> <!-- focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 -->
                        Add CMP1 token &amp; switch network
                      </button>
                    </div>
                  </div>
                  <button on:click={() => utils.downloadPhaseDataset($challenge)} type="button" class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-full shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                    Download dataset
                  </button>
                  <!-- <div class="mt-5 flex justify-center sm:mt-0">
                    <a href="{baseEtherAddr + $tournamentAddress}" class="flex justify-center items-center px-3 py-2 border border-gray-300 shadow-sm text-xs font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                      {$tournamentAddress}
                    </a>
                  </div> -->
                </div>
              </div>
              <div class="border-t bg-gray-50 grid grid-cols-1 divide-y divide-gray-200 sm:divide-y-0 sm:divide-x">
                <Steps phase={$phase} stakeLocked={!!$submissionHash}></Steps>
              </div>
              <!-- <div class="border-t border-gray-200 bg-gray-50 grid grid-cols-1 divide-y divide-gray-200 sm:grid-cols-3 sm:divide-y-0 sm:divide-x">
                <div class="px-6 py-5 text-sm font-medium text-center">
                  <span class="text-gray-600">Stake:</span>
                  <span class="text-gray-900">{parseFloat(stake).toFixed(6)}</span>
                </div>

                <div class="px-6 py-5 text-sm font-medium text-center">
                  <span class="text-gray-600">Pool:</span>
                  <span class="text-gray-900">{parseFloat(tournamentPool).toFixed(6)}</span>
                </div>

                <div class="px-6 py-5 text-sm font-medium text-center">
                  <span class="text-gray-600">Phase:</span>
                  <span class="text-gray-900">{phase}</span>
                </div>
              </div> -->
            </div>
          </section>




          <section aria-labelledby="phase-title">
            <h2 class="sr-only" id="phase-title">Phase details</h2>
            <div class="rounded-lg relative bg-indigo-700 p-6">
            <div class="px-6 py-6 bg-indigo-700 rounded-lg md:py-10 md:px-10 lg:py-12 lg:px-12 xl:flex xl:items-center">
              <div class="sm:w-full xl:mt-0 xl:ml-8">
                <div class="sm:flex sm:items-center sm:justify-between">
                  <div class="w-full text-2xl text-center font-extrabold tracking-tight text-white sm:text-3xl sm:text-left" placeholder="Enter your email">
                    My stake: <span class="font-mono tracking-normal font-bold">{parseFloat($stake).toFixed(6)}</span>
                  </div>
                  {#if !$submissionHash}
                    <button
                      on:click={() => !updatingStake && showStakingPopup(true)}
                      class:cursor-default={updatingStake}
                      class:hover:bg-indigo-700={!updatingStake}
                      class="inline-flex items-center px-6 py-3 border border-transparent shadow-sm text-base font-medium rounded-md text-white bg-indigo-600 focus:outline-none">
                      {#if updatingStake}
                        <svg class="animate-spin -ml-1 mr-3 h-5 w-5" version="1.1" xmlns="http://www.w3.org/2000/svg" x="0px" y="0px"
                          viewBox="0 0 50 50" style="enable-background:new 0 0 50 50;" xml:space="preserve" stroke="text-white" fill="text-white" aria-hidden="true">
                          <path fill="currentColor" d="M43.935,25.145c0-10.318-8.364-18.683-18.683-18.683c-10.318,0-18.683,8.365-18.683,18.683h4.068c0-8.071,6.543-14.615,14.615-14.615c8.072,0,14.615,6.543,14.615,14.615H43.935z" />
                        </svg>
                      {:else}
                        <svg xmlns="http://www.w3.org/2000/svg" class="-ml-1 mr-3 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
                        </svg>
                      {/if}
                      Update
                    </button>
                  {/if}
                </div>
                <!-- <p class="mt-3 text-sm text-indigo-200">
                  We care about the protection of your data. Read our
                  <a href="#" class="text-white font-medium underline">
                    Privacy Policy.
                  </a>
                </p> -->
              </div>

              <div class="sm:w-full xl:mt-0 xl:ml-8 mt-8">
                <div class="sm:flex sm:items-center sm:justify-between">
                  {#if $phase < 2}
                    <div class="flex-none w-full sm:w-auto text-2xl text-center font-extrabold tracking-tight text-white sm:text-3xl sm:text-left" placeholder="Enter your email">
                      {#if $submissionHash}
                        My prediction
                      {/if}
                    </div>
                    <div class="sm:flex">
                      {#if $submissionHash}
                        <button on:click={downloadOwnSubmission} type="button" class="inline-flex items-center px-6 py-3 border border-transparent shadow-sm text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none"> <!-- focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 -->
                          <!-- Heroicon name: solid/mail -->
                          <svg class="-ml-1 mr-3 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path fill-rule="evenodd" d="M2 9.5A3.5 3.5 0 005.5 13H9v2.586l-1.293-1.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 15.586V13h2.5a4.5 4.5 0 10-.616-8.958 4.002 4.002 0 10-7.753 1.977A3.5 3.5 0 002 9.5zm9 3.5H9V8a1 1 0 012 0v5z" clip-rule="evenodd" />
                          </svg>
                          Download
                        </button>
                      {/if}
                      <button class:sm:ml-5={$submissionHash}
                              on:click={() => showUploadPopup(true)}
                              class="inline-flex items-center px-6 py-3 border border-transparent shadow-sm text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none">
                        {#if $submissionHash}
                          {#if uploadingPrediction}
                              <svg class="-ml-1 mr-3 animate-spin h-5 w-5" version="1.1" xmlns="http://www.w3.org/2000/svg" x="0px" y="0px"
                                viewBox="0 0 50 50" style="enable-background:new 0 0 50 50;" xml:space="preserve" stroke="text-white" fill="text-white" aria-hidden="true">
                                <path fill="currentColor" d="M43.935,25.145c0-10.318-8.364-18.683-18.683-18.683c-10.318,0-18.683,8.365-18.683,18.683h4.068c0-8.071,6.543-14.615,14.615-14.615c8.072,0,14.615,6.543,14.615,14.615H43.935z" />
                              </svg>
                            {:else}
                            <svg xmlns="http://www.w3.org/2000/svg" class="-ml-1 mr-3 h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                              <path d="M5.5 13a3.5 3.5 0 01-.369-6.98 4 4 0 117.753-1.977A4.5 4.5 0 1113.5 13H11V9.413l1.293 1.293a1 1 0 001.414-1.414l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13H5.5z" />
                              <path d="M9 13h2v5a1 1 0 11-2 0v-5z" />
                            </svg>
                          {/if}
                          Update
                        {:else}
                          {#if uploadingPrediction}
                            <svg class="-ml-1 mr-3 animate-spin h-5 w-5" version="1.1" xmlns="http://www.w3.org/2000/svg" x="0px" y="0px"
                              viewBox="0 0 50 50" style="enable-background:new 0 0 50 50;" xml:space="preserve" stroke="text-white" fill="text-white" aria-hidden="true">
                              <path fill="currentColor" d="M43.935,25.145c0-10.318-8.364-18.683-18.683-18.683c-10.318,0-18.683,8.365-18.683,18.683h4.068c0-8.071,6.543-14.615,14.615-14.615c8.072,0,14.615,6.543,14.615,14.615H43.935z" />
                            </svg>
                          {:else}
                            <svg xmlns="http://www.w3.org/2000/svg" class="-ml-1 mr-3 h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                              <path d="M5.5 13a3.5 3.5 0 01-.369-6.98 4 4 0 117.753-1.977A4.5 4.5 0 1113.5 13H11V9.413l1.293 1.293a1 1 0 001.414-1.414l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13H5.5z" />
                              <path d="M9 13h2v5a1 1 0 11-2 0v-5z" />
                            </svg>
                          {/if}
                          Submit your prediction &amp; lock stake
                        {/if}
                      </button>
                    </div>
                  {:else}
                    <button on:click={downloadOwnSubmission} type="button" class="inline-flex items-center px-6 py-3 border border-transparent shadow-sm text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none "> <!-- focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 -->
                      <!-- Heroicon name: solid/mail -->
                      <svg class="-ml-1 mr-3 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                        <path fill-rule="evenodd" d="M2 9.5A3.5 3.5 0 005.5 13H9v2.586l-1.293-1.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 15.586V13h2.5a4.5 4.5 0 10-.616-8.958 4.002 4.002 0 10-7.753 1.977A3.5 3.5 0 002 9.5zm9 3.5H9V8a1 1 0 012 0v5z" clip-rule="evenodd" />
                      </svg>
                      My prediction
                    </button>
                  {/if}
                </div>
                <!-- <p class="mt-3 text-sm text-indigo-200">
                  We care about the protection of your data. Read our
                  <a href="#" class="text-white font-medium underline">
                    Privacy Policy.
                  </a>
                </p> -->
              </div>
            </div>
          </section>

          <!-- {$phase}
          {#await utils.getSubmissionDeadline($challenge)}
            <p>...waiting</p>
          {:then deadline}
            <p>The deadline is {deadline}</p>
          {:catch error}
            <p style="color: red">{error}</p>
          {/await} -->


          <!-- {$challengeScoresList}
          <br>
          {$tournamentScoresList}
          <br>
          {$stakingRewardsList}
          <br>
          {$challengeRewardsList}
          <br>
          {$tournamentRewards}
          <br>
          {$overallRewardsList} -->

          {#if $challengeScoresList}
            <ScoresTable challengeScoresList={$challengeScoresList}
                         tournamentScoresList={$tournamentScoresList}
                         stakingRewardsList={$stakingRewardsList}
                         challengeRewardsList={$challengeRewardsList}
                         overallRewardsList={$overallRewardsList} />
          {/if}
          <!-- Actions panel -->
          <!-- <section aria-labelledby="quick-links-title">
            <div class="rounded-lg bg-gray-200 overflow-hidden shadow divide-y divide-gray-200 sm:divide-y-0 sm:grid sm:grid-cols-2 sm:gap-px">
              <h2 class="sr-only" id="quick-links-title">Quick links</h2>

              <div class="rounded-tl-lg rounded-tr-lg sm:rounded-tr-none relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-cyan-500">
                <div>
                  <span class="rounded-lg inline-flex p-3 bg-teal-50 text-teal-700 ring-4 ring-white">
                    <!- - Heroicon name: outline/clock - ->
                    <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </span>
                </div>
              </div>

              <div class="sm:rounded-tr-lg relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-cyan-500">
                <div>
                  <span class="rounded-lg inline-flex p-3 bg-purple-50 text-purple-700 ring-4 ring-white">
                    <!- - Heroicon name: outline/badge-check - ->
                    <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                    </svg>
                  </span>
                </div>
                <div class="mt-8">
                  <h3 class="text-lg font-medium">
                    <a href="#" class="focus:outline-none">
                      <!- - Extend touch target to entire panel - ->
                      <span class="absolute inset-0" aria-hidden="true"></span>
                      Benefits
                    </a>
                  </h3>
                  <p class="mt-2 text-sm text-gray-500">
                    Doloribus dolores nostrum quia qui natus officia quod et dolorem. Sit repellendus qui ut at blanditiis et quo et molestiae.
                  </p>
                </div>
                <span class="pointer-events-none absolute top-6 right-6 text-gray-300 group-hover:text-gray-400" aria-hidden="true">
                  <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M20 4h1a1 1 0 00-1-1v1zm-1 12a1 1 0 102 0h-2zM8 3a1 1 0 000 2V3zM3.293 19.293a1 1 0 101.414 1.414l-1.414-1.414zM19 4v12h2V4h-2zm1-1H8v2h12V3zm-.707.293l-16 16 1.414 1.414 16-16-1.414-1.414z" />
                  </svg>
                </span>
              </div>

              <div class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-cyan-500">
                <div>
                  <span class="rounded-lg inline-flex p-3 bg-sky-50 text-sky-700 ring-4 ring-white">
                    <!- - Heroicon name: outline/users - ->
                    <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                  </span>
                </div>
                <div class="mt-8">
                  <h3 class="text-lg font-medium">
                    <a href="#" class="focus:outline-none">
                      <!- - Extend touch target to entire panel - ->
                      <span class="absolute inset-0" aria-hidden="true"></span>
                      Schedule a one-on-one
                    </a>
                  </h3>
                  <p class="mt-2 text-sm text-gray-500">
                    Doloribus dolores nostrum quia qui natus officia quod et dolorem. Sit repellendus qui ut at blanditiis et quo et molestiae.
                  </p>
                </div>
                <span class="pointer-events-none absolute top-6 right-6 text-gray-300 group-hover:text-gray-400" aria-hidden="true">
                  <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M20 4h1a1 1 0 00-1-1v1zm-1 12a1 1 0 102 0h-2zM8 3a1 1 0 000 2V3zM3.293 19.293a1 1 0 101.414 1.414l-1.414-1.414zM19 4v12h2V4h-2zm1-1H8v2h12V3zm-.707.293l-16 16 1.414 1.414 16-16-1.414-1.414z" />
                  </svg>
                </span>
              </div>

              <div class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-cyan-500">
                <div>
                  <span class="rounded-lg inline-flex p-3 bg-yellow-50 text-yellow-700 ring-4 ring-white">
                    <!- - Heroicon name: outline/cash - ->
                    <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                  </span>
                </div>
                <div class="mt-8">
                  <h3 class="text-lg font-medium">
                    <a href="#" class="focus:outline-none">
                      <!- - Extend touch target to entire panel - ->
                      <span class="absolute inset-0" aria-hidden="true"></span>
                      Payroll
                    </a>
                  </h3>
                  <p class="mt-2 text-sm text-gray-500">
                    Doloribus dolores nostrum quia qui natus officia quod et dolorem. Sit repellendus qui ut at blanditiis et quo et molestiae.
                  </p>
                </div>
                <span class="pointer-events-none absolute top-6 right-6 text-gray-300 group-hover:text-gray-400" aria-hidden="true">
                  <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M20 4h1a1 1 0 00-1-1v1zm-1 12a1 1 0 102 0h-2zM8 3a1 1 0 000 2V3zM3.293 19.293a1 1 0 101.414 1.414l-1.414-1.414zM19 4v12h2V4h-2zm1-1H8v2h12V3zm-.707.293l-16 16 1.414 1.414 16-16-1.414-1.414z" />
                  </svg>
                </span>
              </div>

              <div class="sm:rounded-bl-lg relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-cyan-500">
                <div>
                  <span class="rounded-lg inline-flex p-3 bg-rose-50 text-rose-700 ring-4 ring-white">
                    <!- - Heroicon name: outline/receipt-refund - ->
                    <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 15v-1a4 4 0 00-4-4H8m0 0l3 3m-3-3l3-3m9 14V5a2 2 0 00-2-2H6a2 2 0 00-2 2v16l4-2 4 2 4-2 4 2z" />
                    </svg>
                  </span>
                </div>
                <div class="mt-8">
                  <h3 class="text-lg font-medium">
                    <a href="#" class="focus:outline-none">
                      <!- - Extend touch target to entire panel - ->
                      <span class="absolute inset-0" aria-hidden="true"></span>
                      Submit an expense
                    </a>
                  </h3>
                  <p class="mt-2 text-sm text-gray-500">
                    Doloribus dolores nostrum quia qui natus officia quod et dolorem. Sit repellendus qui ut at blanditiis et quo et molestiae.
                  </p>
                </div>
                <span class="pointer-events-none absolute top-6 right-6 text-gray-300 group-hover:text-gray-400" aria-hidden="true">
                  <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M20 4h1a1 1 0 00-1-1v1zm-1 12a1 1 0 102 0h-2zM8 3a1 1 0 000 2V3zM3.293 19.293a1 1 0 101.414 1.414l-1.414-1.414zM19 4v12h2V4h-2zm1-1H8v2h12V3zm-.707.293l-16 16 1.414 1.414 16-16-1.414-1.414z" />
                  </svg>
                </span>
              </div>

              <div class="rounded-bl-lg rounded-br-lg sm:rounded-bl-none relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-cyan-500">
                <div>
                  <span class="rounded-lg inline-flex p-3 bg-indigo-50 text-indigo-700 ring-4 ring-white">
                    <!- - Heroicon name: outline/academic-cap - ->
                    <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                      <path d="M12 14l9-5-9-5-9 5 9 5z" />
                      <path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222" />
                    </svg>
                  </span>
                </div>
                <div class="mt-8">
                  <h3 class="text-lg font-medium">
                    <a href="#" class="focus:outline-none">
                      <!- - Extend touch target to entire panel - ->
                      <span class="absolute inset-0" aria-hidden="true"></span>
                      Training
                    </a>
                  </h3>
                  <p class="mt-2 text-sm text-gray-500">
                    Doloribus dolores nostrum quia qui natus officia quod et dolorem. Sit repellendus qui ut at blanditiis et quo et molestiae.
                  </p>
                </div>
                <span class="pointer-events-none absolute top-6 right-6 text-gray-300 group-hover:text-gray-400" aria-hidden="true">
                  <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M20 4h1a1 1 0 00-1-1v1zm-1 12a1 1 0 102 0h-2zM8 3a1 1 0 000 2V3zM3.293 19.293a1 1 0 101.414 1.414l-1.414-1.414zM19 4v12h2V4h-2zm1-1H8v2h12V3zm-.707.293l-16 16 1.414 1.414 16-16-1.414-1.414z" />
                  </svg>
                </span>
              </div>
            </div>
          </section> -->

          <!-- <section>
            <div class="grid grid-cols-2 gap-4">

            </div>
          </section> -->
        </div>

        <div class="grid grid-cols-2 gap-4">
          <!-- Announcements -->
          <section aria-labelledby="announcements-title">
          </section>

          <!-- Recent Hires -->
          <section aria-labelledby="recent-hires-title">
          </section>
        </div>
      </div>
    </div>
  </main>
  <footer>
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 lg:max-w-7xl">
      <div class="border-t border-gray-200 py-8 text-sm text-gray-500 text-center sm:text-left"><span class="block sm:inline">
        &copy; 2021 RCI</span> <span class="block sm:inline">All rights reserved.</span>
      </div>
    </div>
  </footer>
</div>

<!-- Global notification live region, render this permanently at the end of the document -->
<div aria-live="assertive" class="fixed inset-0 flex items-end px-4 py-6 pointer-events-none sm:p-6 sm:items-start">
  <div class="w-full flex flex-col items-center space-y-4 sm:items-end">
    <!-- <Notifications show={true}></Notifications> -->
  </div>
</div>
