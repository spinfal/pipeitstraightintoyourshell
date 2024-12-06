import random

def get_funny_message():
    messages = [
        "common sense isn't so common now is it",
        "what if i wiped your system",
        "sudo rm -rf / --no-preserve-root",
        "sending your files to a hacker...",
        "unzipping zip bomb...",
        "rm -rf ~/*",
        ":(){ :|: & };:",
        "mkfs.ext4 /dev/sda1",
        "yes > /dev/null"
    ]
    return random.choice(messages)
