<script lang="ts">
  import Popup from './Popup.svelte'

  import { createEventDispatcher } from 'svelte';

  import { transactions } from './stores.js'

  export let show = false;

	const dispatch = createEventDispatcher();

	function submit() {
		dispatch('submit');
	}

	function cancel() {
		dispatch('cancel');
	}
</script>

<Popup on:cancel={cancel} on:submit={submit} show={show}>
  <div>
    <!-- <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
      <!- - Heroicon name: outline/check - ->
      <svg class="h-6 w-6 text-green-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
      </svg>
    </div> -->
    <div>
      Transactions
    </div>
    <div class="mt-3 __text-center sm:mt-5">
      {#each Object.entries($transactions) as [k, v]}
        <li>
          <a target="_blank" href="https://ropsten.etherscan.io/tx/{k}">
            {v.description};
          </a>
        </li>
      {/each}
    </div>
  </div>
</Popup>
