<script>
  import { createEventDispatcher } from 'svelte';

  export let models = [];
  export let selectedModel = '';
  export let modelStatus = '';

  const dispatch = createEventDispatcher();

  const changeModel = () => {
    dispatch('modelChange', selectedModel);
  };
</script>

<div>
  <label for="models">Select a model:</label>
  <select bind:value="{selectedModel}" id="models" on:change="{changeModel}">
    <option value="">Select a model</option>
    {#each models as model}
      <option value="{model}">{model}</option>
    {/each}
  </select>
</div>
<div>
    {#if modelStatus === 'loading'}
        <div class="box loading">Loading...</div>
    {:else if modelStatus === 'success'}
        <div class="box success">Model loaded successfully.</div>
    {:else if modelStatus === 'error'}
        <div class="box error">Failed to load model.</div>
    {/if}
</div>


<style>
  .box {
    padding: 0.5em;
    margin-bottom: 0.5em;
  }

  select {
    width: 100%;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 0.5em;
  }
  .loading {
    background-color: #f0ad4e;
  }

  .success {
    background-color: #5cb85c;
  }

  .error {
    background-color: #d9534f;
  }
</style>
