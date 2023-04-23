<script>
  import { onMount } from 'svelte';
  import TemplateChooser from './TemplateChooser.svelte';
  import ModelChooser from './ModelChooser.svelte';
  import ChatWindow from './ChatWindow.svelte';
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
<div class="layout">
  <div class="main-content">
    <main>
        <h1>Svelte App</h1>

        <ChatWindow
        {chatHistory}
        bind:textInput
        on:submitForm="{submitForm}"
      />

    </main>
  </div>
  <div class="right-column">
    <ModelChooser
      {models}
      bind:selectedModel
      on:modelChange="{(e) => selectModel(e.detail)}"
    />
    <TemplateChooser
        {templates}
        bind:selectedTemplate
        on:templateChange="{populateTextbox}"
      />
  </div>
</div>

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

  .layout {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      align-items: flex-start;
    }

    .main-content {
       flex: 1;
       margin-right: 2rem;
       border-right: 1px solid #ccc;
  }

    .right-column {
      flex: 0 0 200px; /* You can adjust the width of the right column here */
    }


</style>

