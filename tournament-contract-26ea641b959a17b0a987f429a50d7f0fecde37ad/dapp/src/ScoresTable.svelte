<script type="ts">
  export let challengeScoresList:  string[];
  export let tournamentScoresList: string[];
  export let stakingRewardsList:   string[];
  export let challengeRewardsList: string[];
  export let overallRewardsList:   string[];
</script>

<div class="flex flex-col">
  <div class="-my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
    <div class="py-2 align-middle inline-block min-w-full sm:px-6 lg:px-8">
      <div class="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                #
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Challenge score
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Competition score
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Staking reward
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Challenge reward
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Overall reward
              </th>

              <!-- <th scope="col" class="relative px-6 py-3">
                <span class="sr-only">Edit</span>
              </th> -->
            </tr>
          </thead>
          <tbody>
            <!-- Odd row -->
            {#each challengeScoresList.reverse() as challengeScore, i}
              <tr class="bg-white" class:bg-gray-50={i % 2}>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {challengeScoresList.length - i}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {parseFloat(challengeScore).toFixed(6)}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {parseFloat(tournamentScoresList[challengeScoresList.length - i - 1]).toFixed(6)}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {parseFloat(stakingRewardsList[challengeScoresList.length - i - 1]).toFixed(6)}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {parseFloat(challengeRewardsList[challengeScoresList.length - i - 1]).toFixed(6)}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {parseFloat(overallRewardsList[challengeScoresList.length - i - 1]).toFixed(6)}
                </td>
                <!-- <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <a href="#" class="text-indigo-600 hover:text-indigo-900">Edit</a>
                </td> -->
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
