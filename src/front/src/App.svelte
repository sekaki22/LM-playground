<script>
    import { onMount } from 'svelte';
    import TemplateChooser from './TemplateChooser.svelte';
    import ModelChooser from './ModelChooser.svelte';
    import ChatWindow from './ChatWindow.svelte';
    import Evaluate from './Evaluate.svelte';

    let textInput = '';
    let selectedTemplate = '';
    let selectedModel = '';
    let currentPage = 2;

    const templates = [
        { id: 1, name: 'Template 1', content: 'Sample content for Template 1' },
        { id: 2, name: 'Template 2', content: 'Sample content for Template 2' },
    ];

    let models = [];

    let chatHistory = [];


    let modelStatus = '';

    const listModels = async () => {
        try {
            const response = await fetch('/model/list', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            });

            if (response.ok) {
                const data = await response.json();
                return data.models;
            } else {
            return []
            }
        } catch (error) {
            return []
        }
    };


    const selectModel = async () => {
        modelStatus = 'loading';
        try {
            const response = await fetch('/model/set', {
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
        chatHistory = [...chatHistory, { type: 'input', content: textInput }];
        const response = await fetch(`/predict?prompt=${encodeURIComponent(textInput)}`, {
            method: 'GET',
        });
        const data = await response.text();

        chatHistory = [...chatHistory, { type: 'output', content: data }];
    };

    const populateTextbox = () => {
        const template = templates.find((t) => t.name === selectedTemplate);
        textInput = template ? template.content : '';
    };
    onMount(async () => {
        models = await listModels();
        });
</script>
<main>
    <div class="layout">
        <div class="main-content">
            <div class="pagination">
                <button on:click={() => (currentPage = 1)}>ChatWindow</button>
                <button on:click={() => (currentPage = 2)}>Evaluate</button>
            </div>

            <!-- Display either ChatWindow or Evaluate based on currentPage -->
            {#if currentPage === 1}
                <ChatWindow
                    {chatHistory}
                    bind:textInput
                    on:submitForm="{submitForm}"
                />
            {:else if currentPage === 2}
                <Evaluate />
            {/if}
        </div>
        <div class="right-column">
            <ModelChooser
                {models}
                bind:selectedModel
                bind:modelStatus
                on:modelChange="{(e) => selectModel(e.detail)}"
            />
            <TemplateChooser
                {templates}
                bind:selectedTemplate
                on:templateChange="{populateTextbox}"
            />
        </div>
    </div>

</main>
<style>
    main {
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
        text-align: center;
        padding: 1em;
        max-width: 500px;
        margin: 0 auto;
    }

    .right-column {
        flex: 0 0 200px; /* You can adjust the width of the right column here */
    }

    .container {
        display: flex;
    }

    .main-content {
        flex: 1;
        margin-right: 2rem;
        border-right: 1px solid #ccc;
    }

    .right-column {
        width: 200px;
    }

    .pagination {
        display: flex;
        justify-content: space-between;
        margin-bottom: 1rem;
    }

    .pagination button {
        background-color: #8fb7c5;
        color: white;
        padding: 0.5em 1em;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 16px;
    }

</style>


