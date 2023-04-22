<script>
  import { onMount } from 'svelte';

  let textInput = '';
  let selectedTemplate = '';
  let selectedModel = '';

  const templates = [
    { id: 1, name: 'Template 1', content: 'Sample content for Template 1' },
    { id: 2, name: 'Template 2', content: 'Sample content for Template 2' },
  ];

  const models = ['databricks/dolly-v2-3b', 'EleutherAI/pythia-2.8b'];

  let chatHistory = [];

  const populateTextbox = () => {
    const template = templates.find((t) => t.name === selectedTemplate);
    textInput = template ? template.content : '';
  };

  let modelStatus = '';

  const selectModel = async () => {
    modelStatus = 'loading';
    try {
      const response = await fetch('/model', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model: selectedModel }),
      });

      if (response.ok) {
        modelStatus = 'success';
      } else {
        modelStatus = 'error';
      }
    } catch (error) {
      modelStatus = 'error';
    }
  };

  const submitForm = async (hist) => {
    chatHistory.push({ type: 'input', content: textInput });
    chatHistory = chatHistory;
    const response = await fetch(`/predict?prompt=${encodeURIComponent(textInput)}`, {
      method: 'GET',
    });
    const data = await response.text();

    chatHistory.push({ type: 'output', content: data });
    chatHistory = chatHistory;
    console.log(chatHistory)
  };
</script>

<main>
  <h1>Svelte App</h1>
  <div>
    <label for="textbox">Text Input:</label>
    <textarea bind:value="{textInput}" id="textbox" rows="4" cols="50"></textarea>
  </div>
  <div>
    <label for="templates">Choose a template:</label>
    <select bind:value="{selectedTemplate}" id="templates" on:change="{populateTextbox}">
      <option value="">Select a template</option>
      {#each templates as template}
        <option value="{template.name}">{template.name}</option>
      {/each}
    </select>
  </div>
<div>
    <label for="models">Select a model:</label>
    <select bind:value="{selectedModel}" id="models" on:change="{selectModel}">
      <option value="">Select a model</option>
      {#each models as model}
        <option value="{model}">{model}</option>
      {/each}
    </select>
  </div>
  {#if modelStatus === 'loading'}
    <div class="loading">Loading...</div>
  {:else if modelStatus === 'success'}
    <div class="success">Model loaded successfully.</div>
  {:else if modelStatus === 'error'}
    <div class="error">Failed to load model.</div>
  {/if}
  <div>
    <button on:click="{submitForm(chatHistory)}">Submit</button>
  </div>
  <div class="chat-history">
    <h2>Chat History</h2>
    <ul>
      {#each chatHistory as entry (entry.content)}
        <li class="{entry.type}">
          <span class="label">{entry.type === 'input' ? 'You:' : 'Model:'}</span>
            {@html entry.content.replace(/\n/g, '<br>')}
        </li>
      {/each}
    </ul>
  </div>
</main>

<style>
  main {
    text-align: center;
    padding: 1em;
    max-width: 240px;
    margin: 0 auto;
  }

  textarea {
    width: 100%;
  }

  .chat-history {
    margin-top: 1em;
  }

  .chat-history ul {
    list-style-type: none;
    padding: 0;
  }

  .chat-history li {
    margin-bottom: 0.5em;
    text-align: left;
  }

  .chat-history .input {
    font-weight: bold;
  }

 
  .loading, .success, .error {
    margin-top: 1em;
    padding: 0.5em;
    border-radius: 4px;
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
