<script lang="ts">
  // import { onMount } from 'svelte';

  import Popup from './Popup.svelte'
  import { ethers } from "ethers";

  import { createEventDispatcher } from 'svelte';

  export let show = false;
  export let permission: boolean
  export let stake: number;

  let newStake = null;
  let increase: boolean;
  let difference;
  let differenceAbsStr: string;
  let prevPermission: boolean;

	const dispatch = createEventDispatcher();

  $:{
    // alert(permission);
    prevPermission = prevPermission || permission;
  }

  function grantPermission() {
    dispatch('grantPermission');
  }

	function submit() {
		dispatch('submit', { difference });
	}

	function cancel() {
		dispatch('cancel');
	}

  $: {
    let oldStakeFloat = !!stake && ethers.utils.parseEther('' + stake);
    let newStakeFloat = !!newStake && ethers.utils.parseEther('' + newStake);

    if (oldStakeFloat && newStakeFloat) {
      increase = newStakeFloat.gt(oldStakeFloat);
      difference = newStakeFloat.sub(oldStakeFloat);
      
      let differenceAbs = increase ? newStakeFloat.sub(oldStakeFloat) : oldStakeFloat.sub(newStakeFloat);
      differenceAbsStr = ethers.utils.formatEther(differenceAbs);
    }
  }
</script>

<Popup on:cancel={cancel} on:submit={submit} show={show}>
  {#if false}
    <div>
      <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
        <!-- Heroicon name: outline/check -->
        <svg class="h-6 w-6 text-green-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
      </div>
      <div class="mt-3 text-center sm:mt-5">
        <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
          Payment successful
        </h3>
        <div class="mt-2">
          <p class="text-sm text-gray-500">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Consequatur amet labore.
          </p>
        </div>
      </div>
    </div>
    <div class="mt-5 sm:mt-6">
      <button on:click={grantPermission} type="button" class="inline-flex justify-center w-full rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:text-sm">
        Grant permission
      </button>
    </div>
  {:else}
    <div>
      <div>
        Current Stake: {stake}
      </div>
      <div class="mt-3 __text-center sm:mt-5">
        <div class="mt-1 flex rounded-md shadow-sm">
          <span class="relative inline-flex items-center space-x-2 px-4 py-2 border border-gray-300 text-sm font-medium rounded-l-md text-gray-700 bg-gray-50">Set to</span>
          <div class="-ml-px relative flex items-stretch flex-grow focus-within:z-10">
            <input type="text" autocomplete="off" bind:value={newStake} name="stake" id="stake" class="focus:ring-indigo-500 focus:border-indigo-500 block w-full rounded-none rounded-r-md pl-3 sm:text-sm border-gray-300" placeholder="Insert yout new stake">
          </div>
        </div>
        <p class="mt-2 text-sm text-gray-500" id="email-description">
          Stake will be {newStake - stake >= 0 ? 'increased' : 'decreased'} by {differenceAbsStr}
        </p>
      </div>
    </div>
    {#if !prevPermission}
      <div class="mt-5 sm:mt-6">
        <button on:click={grantPermission} type="button" class:hover:bg-indigo-700={!permission} class="inline-flex justify-center w-full rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 disabled:bg-indigo-300 text-base font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:text-sm">
          {#if !permission}
            Grant staking permission
          {:else}
            Permission granted
          {/if}
        </button>
      </div>
    {/if}
    <div class="mt-5 sm:mt-6">
      <button on:click={submit} type="button" disabled={newStake === null || newStake === '' || !permission} class="inline-flex justify-center w-full rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 disabled:bg-indigo-300 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:text-sm">
        Submit
      </button>
    </div>
    <div class="mt-5 sm:mt-6">
      <button on:click={cancel} type="button" class="inline-flex justify-center w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 text-base font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:text-sm">
        Cancel
      </button>
    </div>
  {/if}
</Popup>
