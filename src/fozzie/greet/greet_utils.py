import random
import datetime
from colorama import Fore, Style, init

# # Initialize colorama for Windows compatibility
# init(autoreset=True)

def greet(name):
    
    output = f"Hello, {name}! Welcome to the Fozzie Library."
    return(output)

# ---------------------------------------------------------
# Example usage:
# greet("Adge")




"""Greets the user with a time-appropriate message, using random greetings and terminal color."""
    # # Get the current hour
    # current_hour = datetime.datetime.now().hour
    
    # # Define greeting categories
    # greetings = {
    #     "morning": [
    #         f"Good morning {name}, how are you doing today?",
    #         f"Rise and shine, {name}!",
    #         f"Top of the morning to you, {name}!",
    #         f"Hope you have a fantastic morning, {name}!",
    #         f"Morning, {name}! Coffee or tea today?"
    #     ],
    #     "afternoon": [
    #         f"Good afternoon {name}, hope your day is going well!",
    #         f"Hey {name}, how's your afternoon treating you?",
    #         f"Hello {name}, a fine afternoon to you!",
    #         f"Hope your afternoon is productive, {name}!",
    #         f"Good day, {name}! Getting things done?"
    #     ],
    #     "evening": [
    #         f"Good evening {name}, winding down?",
    #         f"Hey {name}, how was your day?",
    #         f"Evening, {name}! Time to relax a bit?",
    #         f"Hope you're having a cozy evening, {name}!",
    #         f"Nightfall is here, {name}. What’s on your mind?"
    #     ]
    # }
    
    # # Determine the greeting category
    # if 5 <= current_hour < 12:
    #     greeting = random.choice(greetings["morning"])
    #     color = Fore.YELLOW
    # elif 12 <= current_hour < 18:
    #     greeting = random.choice(greetings["afternoon"])
    #     color = Fore.GREEN
    # else:
    #     greeting = random.choice(greetings["evening"])
    #     color = Fore.BLUE





        # Print the greeting with color
    #print(color + greeting + Style.RESET_ALL)