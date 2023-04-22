<script>
  export let templates = [];
  export let selectedTemplate = '';
  export let onTemplateChange = () => {};

  const populateTextbox = () => {
    onTemplateChange(selectedTemplate);
  };
</script>

<div>
  <label for="templates">Choose a template:</label>
  <select bind:value="{selectedTemplate}" id="templates" on:change="{populateTextbox}">
    <option value="">Select a template</option>
    {#each templates as template}
      <option value="{template.name}">{template.name}</option>
    {/each}
  </select>
</div>


<style>
  select {
    width: 100%;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 0.5em;
  }
</style>
