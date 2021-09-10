<script lang="ts">
  export let show = false;
  
  let _add = false;
  let _show = false

  $: {
    if (show) {
      _add = true;
      setTimeout(() => _show = true, 10);
    } else {
      setTimeout(() => _add = false, 200);
      _show = false;
    }
  }
</script>
{#if _add}
  <div class="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!--
        Background overlay, show/hide based on modal state.

        Entering: "ease-out duration-300"
          From: "opacity-0"
          To: "opacity-100"
        Leaving: "ease-in duration-200"
          From: "opacity-100"
          To: "opacity-0"
      -->
      <div
        class:ease-out={_show}
        class:opacity-100={_show}
        class:duration-300={_show}
        class:ease-in={!_show}
        class:opacity-0={!_show}
        class:duration-200={!_show}
        class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>

      <!-- This element is to trick the browser into centering the modal contents. -->
      <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

      <!--
        Modal panel, _show/hide based on modal state.

        Entering: "ease-out duration-300"
          From: "opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          To: "opacity-100 translate-y-0 sm:scale-100"
        Leaving: "ease-in duration-200"
          From: "opacity-100 translate-y-0 sm:scale-100"
          To: "opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
      -->
      <div class:ease-out={_show}
           class:duration-300={_show}
           class:translate-y-0={_show}
           class:sm:scake-100={_show}
           class:opacity-100={_show}
           class:ease-in={!_show}
           class:duration-200={!_show}
           class:opacity-0={!_show}
           class:translate-y-4={!_show}
           class:sm:translate-y-0={!_show}
           class:sm:scale-95={!_show}
           class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-sm sm:w-full sm:p-6">
        <slot></slot>
      </div>
    </div>
  </div>
{/if}