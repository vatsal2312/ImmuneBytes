<script lang="ts">
  import Step from './Step.svelte'
  // import { ChallengePhase } from '../utilities';

  export let phase: number;
  export let stakeLocked: boolean

  function stakingStepStatus(challengePhase: number, stakeLocked: boolean) {
    if (challengePhase === 1 && !stakeLocked) {
      return 'current'
    } else {
      return 'complete'
    }
  }

  function submissionStepStatus(challengePhase: number, stakeLocked: boolean) {
    if (challengePhase === 1) {
      return stakeLocked ? 'current' : 'upcoming';
    } else {
      return 'complete'
    }
  }

  function evaluationStepStatus(challengePhase: number) {
    if (challengePhase === 4) return 'complete';
    else if (challengePhase > 1) return 'current';
    else return 'upcoming';
  }

  // function getStepStage(challengePhase: number, phaseLocked: boolean, phase: number) {
  //   if (challengePhase === 1 && phase === 1) return 'current';
  //   if (challengePhase === 1 )
  //   if (challenge)

  //   if (challengePhase === phase) return 'current'
  //   else if (challengePhase < phase) return 'upcoming'
  //   else return 'complete'
  // }
</script>

<ol class="divide-y divide-gray-300 md:flex md:divide-y-0">
  <Step label="Staking" number="1" stage={stakingStepStatus(phase, stakeLocked)} last={false}></Step>
  <Step label="Submission" number="2" stage={submissionStepStatus(phase, stakeLocked)} last={false}></Step>
  <Step label="Evaluation" number="3" last={true} stage={evaluationStepStatus(phase)}></Step>
</ol>
