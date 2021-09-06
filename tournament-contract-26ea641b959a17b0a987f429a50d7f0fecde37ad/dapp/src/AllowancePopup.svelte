<script lang="ts">
  import Popup from './Popup.svelte'

  import { createEventDispatcher } from 'svelte';

  export let show = false;
  export let allowance;

	const dispatch = createEventDispatcher();

	function submit() {
		dispatch('submit', { increase, quantity });
	}

  function cancel() {
		dispatch('cancel');
	}

  let increase = true;
  let quantity;

  function toggle() {
    increase = !increase;
  }
</script>

<Popup on:cancel={cancel} on:submit={submit} show={show}>
  <div>
        <div>
          <!-- <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
            <!- - Heroicon name: outline/check - ->
            <svg class="h-6 w-6 text-green-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div> -->
          <div>
            Current allowance: {allowance}
          </div>
          <div class="mt-3 __text-center sm:mt-5">
            <label for="allowance" class="block text-sm font-medium text-gray-700">Allowance</label>
            <div class="mt-1 flex rounded-md shadow-sm">
              <button on:click={() => toggle()} class="relative inline-flex items-center space-x-2 px-4 py-2 border border-gray-300 text-sm font-medium rounded-l-md text-gray-700 bg-gray-50 hover:bg-gray-100 focus:outline-none focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500">
                <!-- Heroicon name: solid/plus-circle -->
                {#if increase}
                  <span>Increase by</span>
                {:else}
                  <span>Decrease by</span>
                {/if}
              </button>
              <div class="-ml-px relative flex items-stretch flex-grow focus-within:z-10">
                <input type="text" bind:value={quantity} name="allowance" id="allowance" class="focus:ring-indigo-500 focus:border-indigo-500 block w-full rounded-none rounded-r-md pl-3 sm:text-sm border-gray-300">
              </div>

            </div>
            <!-- <label for="stake" class="mt-4 block text-sm font-medium text-gray-700">Stake</label>
            <div class="mt-1">
              <input type="text" name="stake" id="stake" class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md">
            </div> -->
            <!-- <div class="mt-2">
              <p class="text-sm text-gray-500">
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Consequatur amet labore.
              </p>
            </div> -->
          </div>
        </div>
  </div>
  <div class="mt-5 sm:mt-6">
    <button on:click={submit} type="button" class="inline-flex justify-center w-full rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:text-sm">
      Submit
    </button>
  </div>
  <div class="mt-5 sm:mt-6">
    <button on:click={cancel} type="button" class="inline-flex justify-center w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 text-base font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:text-sm">
      Cancel
    </button>
  </div>
</Popup>
