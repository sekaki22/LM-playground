
<script>
  import { onMount } from 'svelte';
  let evaluations = [];
  let activeEvaluation = null;
  let progress = 0;
  let results = null;

  const fetchEvaluations = async () => {
    const response = await fetch('/eval/list');
    evaluations = await response.json();
  };

  const runEvaluation = async (evaluation) => {
    activeEvaluation = evaluation;
    progress = 0;
    results = null;

    // Simulate progress updates
    const progressInterval = setInterval(() => {
      progress += 10;
      if (progress >= 100) {
        clearInterval(progressInterval);
      }
    }, 1000);

    // Call the /eval/run endpoint with evalname
    const response = await fetch(`/eval/run?evalname=${encodeURIComponent(evaluation)}`);
    results = await response.json();

    // Update progress to 100% when the test is done
    progress = 100;
  };

  onMount(() => {
    fetchEvaluations();
  });
</script>

<div>
  <h2>Evaluate</h2>
  <ul class="evaluations">
    {#each evaluations as evaluation}
      <li on:click={() => runEvaluation(evaluation)}>{evaluation}</li>
    {/each}
  </ul>

  {#if activeEvaluation}
    <div class="evaluation-details">
      <h3>Evaluation: {activeEvaluation}</h3>
      <div class="progress">
        Progress: {progress}%
      </div>
      {#if results}
        <pre class="results">{JSON.stringify(results, null, 2)}</pre>
      {/if}
    </div>
  {/if}
</div>

<style>
  .evaluations {
    list-style-type: none;
    padding: 0;
  }

  .evaluations li {
    padding: 8px 16px;
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    border-radius: 4px;
    cursor: pointer;
    margin-bottom: 8px;
  }

  .evaluations li:hover {
    background-color: #e0e0e0;
  }

  .evaluation-details {
    margin-top: 1rem;
  }

  .progress {
    margin-bottom: 1rem;
  }

  .results {
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 1rem;
    white-space: pre-wrap;
  }
</style>

