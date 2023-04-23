<script>
    import { createEventDispatcher } from 'svelte';

    export let chatHistory = [];
    export let textInput = '';
    const dispatch = createEventDispatcher();

    const submitForm= () => {
        dispatch('submitForm', textInput);
    };
</script>

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


<style>
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
</style>
