import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from fozzie.greet.greet import greet  # ✅ Correct import path

def test_greet():
    name = "Adge"
    assert isinstance(greet(name), str)  # Adjusted test to avoid hardcoded string
    assert greet(name) == f"Hello, {name}! Welcome to the Fozzie Library." 
    return None

# Run the test
