from termcolor import colored

def printOutput(message, type):
    if type == "failure":
        print(
            colored(
                f"[*] {message}!", "red", attrs=['bold']
            )
        )
    elif type == "loading":
        print(
            colored(
                f"[*] {message}...", "yellow", attrs=['bold']
            )
        )
    elif type == "success":
        print(
            colored(
                f"[*] {message}!", "green", attrs=['bold']
            )
        )

