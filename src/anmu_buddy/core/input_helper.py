def ask_until_valid(prompt, validator, error_msg):
    while True:
        value = input(prompt).strip()

        if value.lower() in ("exit", "quit", "q"):
            print("Process aborted by user.")

        if validator(value):
            return value
        
        print(error_msg)