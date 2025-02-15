import os
import platform

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def validate_input(prompt, data_type):
    """Validate user input based on the expected data type."""
    while True:
        value = input(prompt).strip()
        
        if not value:
            raise ValueError("Input cannot be empty")

        if data_type == str:
            if len(value) < 2:
                raise ValueError("Input must be at least 2 characters long")
            return value
        
        try:
            return data_type(value)
        except ValueError:
            raise ValueError(f"Invalid input. Expected {data_type.__name__}")
