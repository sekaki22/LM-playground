import os
import readline
import torch
from transformers import pipeline

def main():
    
    logdir = "/tmp/dolly-3b-cli"
    os.makedirs(logdir, exist_ok=True)

    

    history_file = f"{logdir}/cli_history.txt"
    log_file     = f"{logdir}/conversation_history.txt"

    generate_text = pipeline(model="databricks/dolly-v2-3b", torch_dtype=torch.bfloat16, trust_remote_code=True, device_map="auto")
    # generate_text = pipeline(model="EleutherAI/pythia-2.8b", torch_dtype=torch.bfloat16, trust_remote_code=True, device_map="auto")
    
    # Load history from file
    try:
        readline.read_history_file(history_file)
    except FileNotFoundError:
        pass

    while True:
        try:
            # Read input from the user with a prompt
            user_input = input("> ")

            if user_input == 'h':
                with open(log_file, 'r') as f:
                    print(f.read())
                    continue

            if user_input == 'dh':
                with open(log_file, 'r') as f:
                    f.close()
                    continue

            # # Add the input to the readline history
            if user_input:
                with open(log_file, 'a') as f:
                    f.write(f'user\t\t> {user_input} \n\n')
                readline.add_history(user_input)



            # Process the input
            if user_input.lower() == "exit":
                break
            else:
                res = generate_text(user_input)
                response_text = res[0]["generated_text"]
                with open(log_file, 'a') as f:
                    f.write(f'AI\t\t> {response_text}\n\n')


                print(response_text)

        except KeyboardInterrupt:
            # Exit gracefully on Ctrl+C
            print("\nExiting...")
            with open(log_file, 'a') as f:
                f.write(f'\n+++++++++++++++++SESSION END+++++++++++++++++++++\n')
            break

    # Save history to file
    readline.write_history_file(history_file)

if __name__ == "__main__":
    main()

