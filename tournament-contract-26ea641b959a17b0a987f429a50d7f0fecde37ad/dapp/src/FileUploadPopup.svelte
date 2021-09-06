<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  import Popup from './Popup.svelte'

  export let show = false;

  let dropTarget: HTMLElement;
  let predictionFiles;
  let over = false;

  $: {
    if (dropTarget) {
      dropTarget.ondragover = dropTarget.ondragenter = evt => {
        evt.preventDefault(); 
        over = true;
      }
      dropTarget.ondragleave = () => over = false;

      dropTarget.ondrop = function(evt) {
        over = false;
        predictionFiles = evt.dataTransfer.files;

        evt.preventDefault();
      }
    }
  }

  const dispatch = createEventDispatcher();

	function submit() {
		dispatch('submit', { predictionFile: predictionFiles[0] });
	}

	function cancel() {
		dispatch('cancel');
	}
</script>

<Popup on:cancel={cancel} on:submit={submit} show={show}>
  <div>
    <h3 class="text-lg leading-6 font-medium text-gray-900">
      Please upload the prediction file (.csv)
    </h3>
  </div>


  <div>
    <div bind:this={dropTarget}
         class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 rounded-md"
         class:border-gray-300={!predictionFiles}
         class:border-dashed={!predictionFiles}
         class:bg-indigo-200={predictionFiles}
         class:border-indigo-400={over}
         class:border-gray-400={predictionFiles}>
      <div class="space-y-1 text-center">
        <svg xmlns="http://www.w3.org/2000/svg"
             class="mx-auto h-8 w-8" 
             class:text-gray-400={!predictionFiles}
             class:text-gray-600={predictionFiles}
             fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <div class="mx-auto text-sm"
             class:text-gray-600={!predictionFiles}
             class:text-gray-800={predictionFiles}>
          <span>
            {#if predictionFiles && predictionFiles[0]}
              <span class="font-bold">{predictionFiles[0].name}</span>
            {:else}
              Prediction file
            {/if}
          </span>
        </div>
        <div class="flex text-sm text-gray-600">
          <label for="prediction-file-upload" class="relative cursor-pointer rounded-md font-medium text-indigo-600 hover:text-indigo-500">
            <span>
              Choose a file
            </span>
            <input bind:files={predictionFiles} id="prediction-file-upload" name="file-upload" type="file" accept=".csv" class="sr-only">
          </label>
          <p class="pl-1">or drag and drop</p>
        </div>
        <!-- <p class="text-xs text-gray-500">
          PNG, JPG, GIF up to 10MB
        </p> -->
      </div>
    </div>
  </div>
  <div class="mt-5 sm:mt-6">
    <button on:click={submit} type="button" disabled={!predictionFiles} class="inline-flex justify-center w-full rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 disabled:bg-indigo-300 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:text-sm">
      Upload
    </button>
  </div>
  <div class="mt-5 sm:mt-6">
    <button on:click={cancel} type="button" class="inline-flex justify-center w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 text-base font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:text-sm">
      Cancel
    </button>
  </div>
</Popup>
