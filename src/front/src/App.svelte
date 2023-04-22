<script>
  import { onMount } from 'svelte';
  import TemplateChooser from './TemplateChooser.svelte';
  import ModelChooser from './ModelChooser.svelte';

  let textInput = '';
  let selectedTemplate = '';
  let selectedModel = '';

  const templates = [
    { id: 1, name: 'Template 1', content: 'Sample content for Template 1' },
    { id: 2, name: 'Template 2', content: 'Sample content for Template 2' },
  ];

  const models = ['databricks/dolly-v2-3b', 'EleutherAI/pythia-2.8b'];

  let chatHistory = [];


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
      console.log(textInput)
    chatHistory = [...chatHistory, { type: 'input', content: textInput }];
    const response = await fetch(`/predict?prompt=${encodeURIComponent(textInput)}`, {
      method: 'GET',
    });
    const data = await response.text();

    chatHistory = [...chatHistory, { type: 'output', content: data }];
    console.log(chatHistory)
  };

  const populateTextbox = () => {
    const template = templates.find((t) => t.name === selectedTemplate);
    textInput = template ? template.content : '';
  };
</script>

<main>
    <h1>Svelte App</h1>

  <div class="chat-window">
    <div class="chat-history">
      <h2>Chat History</h2>
      <ul>
        {#each chatHistory as entry (entry.content)}
          <li class="{entry.type}">
            <span class="label">{entry.type === 'input' ? 'You:' : 'Model:'}</span>
          <div class="message-box">
            {@html entry.content.replace(/\n/g, '<br>')}
            </div>
          </li>
        {/each}
      </ul>
    </div>
    <div class="input-area">
      <label for="textbox">Text Input:</label>
      <textarea bind:value="{textInput}" id="textbox" rows="4" cols="50"></textarea>
      <div>
        <button on:click="{submitForm}">Submit</button>
      </div>
    </div>
  </div>

    <TemplateChooser
    {templates}
    bind:selectedTemplate
    on:templateChange="{populateTextbox}"
  />
    <ModelChooser
    {models}
    bind:selectedModel
    bind:modelStatus
    on:modelChange="{selectModel}"
  />
  <div>
    <button on:click="{submitForm}">Submit</button>
  </div>



</main>

<style>
  main {
    text-align: center;
    padding: 1em;
    max-width: 500px;
    margin: 0 auto;
    font-family: 'Roboto', sans-serif;
  }

  h1 {
    color: #59656f;
  }

  textarea {
    width: 100%;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 0.5em;
  }


  label {
    display: block;
    margin-bottom: 0.5em;
  }

  button {
    background-color: #8fb7c5;
    color: white;
    padding: 0.5em 1em;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
  }

  .chat-history {
    margin-top: 1em;
  }

  .chat-history ul {
    list-style-type: none;
    padding: 0;
  }

  .chat-history li {
    margin-bottom: 1em;
    text-align: left;
  }

  .chat-history .label {
    font-weight: bold;
  }

  .message-box {
    display: inline-block;
    max-width: 75%;
    border-radius: 12px;
    padding: 12px;
    font-size: 14px;
  }

  .chat-history .input .message-box {
    background-color: #b5e7a0;
    margin-left: 1em;
  }

  .chat-history .output .message-box {
    background-color: #a5d2ff;
    margin-left: 1em;
  }

  .loading, .success, .error {
    margin-top: 1em;
    padding: 0.5em;
    border-radius: 4px;
  }
.chat-window {
    display: flex;
    flex-direction: column;
    height: 80vh;
    max-width: 500px;
    margin: 0 auto;
  }

  .chat-history {
    flex-grow: 1;
    overflow-y: auto;
    margin-bottom: 1em;
  }

  .input-area {
    flex-shrink: 1;
  }

</style>

