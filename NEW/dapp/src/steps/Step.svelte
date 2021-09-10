<script lang="ts">
  export let stage: 'complete' | 'current' | 'upcoming';
  export let last: boolean
  export let label: string
  export let number: string

  // function getSegmentColor(): string {
  //   return stage === 'complete' ? 'bg-indigo-600' : 'bg-gray-300'
  // }
</script>

<!-- {#if stage === 'complete'}
  <li class="relative" class:pb-10="{!last}">
    {#if !last}
      <div class="-ml-px absolute mt-0.5 top-4 left-4 w-0.5 h-full {getSegmentColor()}" aria-hidden="true"></div>
    {/if}
    <!- - Complete Step - ->
    <a href="#" class="relative flex items-center group">
      <span class="h-9 flex items-center">
        <span class="relative z-10 w-8 h-8 flex items-center justify-center bg-indigo-600 rounded-full group-hover:bg-indigo-800">
          <! -- Heroicon name: solid/check - ->
          <svg class="w-5 h-5 text-white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
        </span>
      </span>
      <span class="ml-4 min-w-0 flex flex-col">
        <span class="text-xs font-semibold tracking-wide uppercase">{label}</span>
      </span>
    </a>
  </li>
{:else if stage === 'current'}
  <li class="relative" class:pb-10="{!last}">
    {#if !last}
      <div class="-ml-px absolute mt-0.5 top-4 left-4 w-0.5 h-full {getSegmentColor()}" aria-hidden="true"></div>
    {/if}
    <!- - Current Step - ->
    <a href="#" class="relative flex items-center group" aria-current="step">
      <span class="h-9 flex items-center" aria-hidden="true">
        <span class="relative z-10 w-8 h-8 flex items-center justify-center bg-white border-2 border-indigo-600 rounded-full">
          <span class="h-2.5 w-2.5 bg-indigo-600 rounded-full"></span>
        </span>
      </span>
      <span class="ml-4 min-w-0 flex flex-col">
        <span class="text-xs font-semibold tracking-wide uppercase text-indigo-600">{label}</span>
      </span>
    </a>
  </li>
{:else}
  <li class="relative" class:pb-10="{!last}">
    <!- - Upcoming Step - ->
    {#if !last}
      <div class="-ml-px absolute mt-0.5 top-4 left-4 w-0.5 h-full {getSegmentColor()}" aria-hidden="true"></div>
    {/if}
    <a href="#" class="relative flex items-center group">
      <span class="h-9 flex items-center" aria-hidden="true">
        <span class="relative z-10 w-8 h-8 flex items-center justify-center bg-white border-2 border-gray-300 rounded-full group-hover:border-gray-400">
          <span class="h-2.5 w-2.5 bg-transparent rounded-full group-hover:bg-gray-300"></span>
        </span>
      </span>
      <span class="ml-4 min-w-0 flex flex-col">
        <span class="text-xs font-semibold tracking-wide uppercase text-gray-500">{label}</span>
      </span>
    </a>
  </li>
{/if} -->

{#if stage === 'complete'}
  <li class="relative md:flex-1 md:flex">
    <!-- Completed Step -->
    <a href="#" class="group flex items-center w-full">
      <span class="px-6 py-4 flex items-center text-sm font-medium">
        <span class="flex-shrink-0 w-10 h-10 flex items-center justify-center bg-indigo-600 rounded-full group-hover:bg-indigo-800">
          <!-- Heroicon name: solid/check -->
          <svg class="w-6 h-6 text-white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
        </span>
        <span class="ml-4 text-sm font-medium text-gray-900">{label}</span>
      </span>
    </a>

    <!-- Arrow separator for lg screens and up -->
    {#if !last}
      <div class="hidden md:block absolute top-0 right-0 h-full w-5" aria-hidden="true">
        <svg class="h-full w-full text-gray-300" viewBox="0 0 22 80" fill="none" preserveAspectRatio="none">
          <path d="M0 -2L20 40L0 82" vector-effect="non-scaling-stroke" stroke="currentcolor" stroke-linejoin="round" />
        </svg>
      </div>
    {/if}
  </li>


  <!-- <li class="relative" class:pb-10="{!last}">
    {#if !last}
      <div class="-ml-px absolute mt-0.5 top-4 left-4 w-0.5 h-full {getSegmentColor()}" aria-hidden="true"></div>
    {/if}
    <!- - Complete Step - ->
    <a href="#" class="relative flex items-center group">
      <span class="h-9 flex items-center">
        <span class="relative z-10 w-8 h-8 flex items-center justify-center bg-indigo-600 rounded-full group-hover:bg-indigo-800">
          <!- - Heroicon name: solid/check - ->
          <svg class="w-5 h-5 text-white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
        </span>
      </span>
      <span class="ml-4 min-w-0 flex flex-col">
        <span class="text-xs font-semibold tracking-wide uppercase">{label}</span>
      </span>
    </a>
  </li> -->
{:else if stage === 'current'}
  <li class="relative md:flex-1 md:flex">
    <!-- Current Step -->
    <a href="#" class="px-6 py-4 flex items-center text-sm font-medium" aria-current="step">
      <span class="flex-shrink-0 w-10 h-10 flex items-center justify-center border-2 border-indigo-600 rounded-full">
        <span class="text-indigo-600">{number}</span>
      </span>
      <span class="ml-4 text-sm font-medium text-indigo-600">{label}</span>
    </a>

    <!-- Arrow separator for lg screens and up -->
    {#if !last}
      <div class="hidden md:block absolute top-0 right-0 h-full w-5" aria-hidden="true">
        <svg class="h-full w-full text-gray-300" viewBox="0 0 22 80" fill="none" preserveAspectRatio="none">
          <path d="M0 -2L20 40L0 82" vector-effect="non-scaling-stroke" stroke="currentcolor" stroke-linejoin="round" />
        </svg>
      </div>
    {/if}
  </li>

  <!-- <li class="relative" class:pb-10="{!last}">
    {#if !last}
      <div class="-ml-px absolute mt-0.5 top-4 left-4 w-0.5 h-full {getSegmentColor()}" aria-hidden="true"></div>
    {/if}
    <!- - Current Step - ->
    <a href="#" class="relative flex items-center group" aria-current="step">
      <span class="h-9 flex items-center" aria-hidden="true">
        <span class="relative z-10 w-8 h-8 flex items-center justify-center bg-white border-2 border-indigo-600 rounded-full">
          <span class="h-2.5 w-2.5 bg-indigo-600 rounded-full"></span>
        </span>
      </span>
      <span class="ml-4 min-w-0 flex flex-col">
        <span class="text-xs font-semibold tracking-wide uppercase text-indigo-600">{label}</span>
      </span>
    </a>
  </li> -->
{:else}
  <li class="relative md:flex-1 md:flex">
    <!-- Upcoming Step -->
    <a href="#" class="group flex items-center">
      <span class="px-6 py-4 flex items-center text-sm font-medium">
        <span class="flex-shrink-0 w-10 h-10 flex items-center justify-center border-2 border-gray-300 rounded-full group-hover:border-gray-400">
          <span class="text-gray-500 group-hover:text-gray-900">{number}</span>
        </span>
        <span class="ml-4 text-sm font-medium text-gray-500 group-hover:text-gray-900">{label}</span>
      </span>
    </a>
    {#if !last}
      <div class="hidden md:block absolute top-0 right-0 h-full w-5" aria-hidden="true">
        <svg class="h-full w-full text-gray-300" viewBox="0 0 22 80" fill="none" preserveAspectRatio="none">
          <path d="M0 -2L20 40L0 82" vector-effect="non-scaling-stroke" stroke="currentcolor" stroke-linejoin="round" />
        </svg>
      </div>
    {/if}
  </li>
  <!-- <li class="relative" class:pb-10="{!last}">
    <!- - Upcoming Step - ->
    {#if !last}
      <div class="-ml-px absolute mt-0.5 top-4 left-4 w-0.5 h-full {getSegmentColor()}" aria-hidden="true"></div>
    {/if}
    <a href="#" class="relative flex items-center group">
      <span class="h-9 flex items-center" aria-hidden="true">
        <span class="relative z-10 w-8 h-8 flex items-center justify-center bg-white border-2 border-gray-300 rounded-full group-hover:border-gray-400">
          <span class="h-2.5 w-2.5 bg-transparent rounded-full group-hover:bg-gray-300"></span>
        </span>
      </span>
      <span class="ml-4 min-w-0 flex flex-col">
        <span class="text-xs font-semibold tracking-wide uppercase text-gray-500">{label}</span>
      </span>
    </a>
  </li> -->
{/if}


  <!-- <li class="relative md:flex-1 md:flex">
    <!- - Completed Step - ->
    <a href="#" class="group flex items-center w-full">
      <span class="px-6 py-4 flex items-center text-sm font-medium">
        <span class="flex-shrink-0 w-10 h-10 flex items-center justify-center bg-indigo-600 rounded-full group-hover:bg-indigo-800">
          <!- - Heroicon name: solid/check - ->
          <svg class="w-6 h-6 text-white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
        </span>
        <span class="ml-4 text-sm font-medium text-gray-900">Job details</span>
      </span>
    </a>

    <!- - Arrow separator for lg screens and up - ->
    <div class="hidden md:block absolute top-0 right-0 h-full w-5" aria-hidden="true">
      <svg class="h-full w-full text-gray-300" viewBox="0 0 22 80" fill="none" preserveAspectRatio="none">
        <path d="M0 -2L20 40L0 82" vector-effect="non-scaling-stroke" stroke="currentcolor" stroke-linejoin="round" />
      </svg>
    </div>
  </li>

  <li class="relative md:flex-1 md:flex">
    <!- - Current Step - ->
    <a href="#" class="px-6 py-4 flex items-center text-sm font-medium" aria-current="step">
      <span class="flex-shrink-0 w-10 h-10 flex items-center justify-center border-2 border-indigo-600 rounded-full">
        <span class="text-indigo-600">02</span>
      </span>
      <span class="ml-4 text-sm font-medium text-indigo-600">Application form</span>
    </a>

    <!- - Arrow separator for lg screens and up - ->
    <div class="hidden md:block absolute top-0 right-0 h-full w-5" aria-hidden="true">
      <svg class="h-full w-full text-gray-300" viewBox="0 0 22 80" fill="none" preserveAspectRatio="none">
        <path d="M0 -2L20 40L0 82" vector-effect="non-scaling-stroke" stroke="currentcolor" stroke-linejoin="round" />
      </svg>
    </div>
  </li>

  <li class="relative md:flex-1 md:flex">
    <!- - Upcoming Step - ->
    <a href="#" class="group flex items-center">
      <span class="px-6 py-4 flex items-center text-sm font-medium">
        <span class="flex-shrink-0 w-10 h-10 flex items-center justify-center border-2 border-gray-300 rounded-full group-hover:border-gray-400">
          <span class="text-gray-500 group-hover:text-gray-900">03</span>
        </span>
        <span class="ml-4 text-sm font-medium text-gray-500 group-hover:text-gray-900">Preview</span>
      </span>
    </a>
  </li>
</ol> -->
