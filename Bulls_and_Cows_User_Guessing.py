'''
Bulls and Cows Game with Information Theory.
This implementation uses entropy calculation to measure the uncertainty
in the game state as players make guesses.
'''

#required imports
import itertools
import math
import random
from typing import List, Tuple

def compute_feedback(secret: str, guess: str) -> Tuple[int, int]:
    """
    Compute the feedback for a guess in terms of bulls and cows.
    
    Args:
        secret (str): The secret code to be guessed
        guess (str): The player's guess
        
    Returns:
        Tuple[int, int]: A tuple containing (bulls, cows) where:
            - bulls: number of correct digits in correct positions
            - cows: number of correct digits in wrong positions
            
    Example:
        >>> compute_feedback("1234", "1432")
        (2, 2)  # 1 and 4 are bulls, 2 and 3 are cows
    """
    # Count exact matches (bulls)
    bulls = sum(s == g for s, g in zip(secret, guess))
    
    # Count total matching digits across all positions
    common = sum(min(secret.count(d), guess.count(d)) for d in set(guess))
    
    # Subtract bulls from common matches to get cows
    cows = common - bulls
    return (bulls, cows)

def calculate_current_entropy(bulls: int, cows: int) -> float:
    """
    Calculate the current entropy (uncertainty) in the game state.
    Uses information theory principles to quantify remaining uncertainty.
    
    Args:
        bulls (int): Number of correct digits in correct positions
        cows (int): Number of correct digits in wrong positions
        
    Returns:
        float: Current entropy in bits
        
    Note:
        - Base entropy is log2(10) = 3.32 bits per position
        - Total initial entropy for 4 positions is 13.29 bits
        - Bulls provide more certainty than cows in reducing entropy
    """
    # Maximum possible entropy for a 4-digit number
    base_entropy = 4 * math.log2(10)  

    # Convert feedback into uncertainty reduction factors
    position_certainty = bulls / 4.0  # Each bull gives complete position certainty
    digit_certainty = cows / 8.0      # Cows provide less certainty than bulls

    # Calculate remaining uncertainty as a fraction
    remaining_uncertainty = 1.0 - (position_certainty + digit_certainty)

    # Apply uncertainty to base entropy
    current_entropy = base_entropy * remaining_uncertainty

    return current_entropy

def is_valid_guess(guess: str) -> bool:
    """
    Validate if a guess meets the game rules.
    
    Args:
        guess (str): The player's guess
        
    Returns:
        bool: True if guess is valid (4 unique digits), False otherwise
        
    Example:
        >>> is_valid_guess("1234")
        True
        >>> is_valid_guess("1122")
        False  # Contains duplicate digits
    """
    return (len(guess) == 4 and
            guess.isdigit() and
            len(set(guess)) == 4)

def main() -> None:
    """
    Main game loop implementing the Bulls and Cows game with entropy tracking.
    
    Game Rules:
    1. Computer generates a secret 4-digit code with unique digits
    2. Player tries to guess the code
    3. After each guess, feedback is given as bulls and cows
    4. Game ends when player guesses correctly or exceeds 20 attempts
    
    Features:
    - Entropy calculation to track game progress
    - Input validation
    - Quit option available
    """
    # Generate all possible 4-digit codes with unique digits
    all_codes = [''.join(p) for p in itertools.permutations('0123456789', 4)]
    secret_code = random.choice(all_codes)

    # Calculate initial entropy for a 4-digit number
    initial_entropy = 4 * math.log2(10)

    # Display game instructions
    print("I've thought of a 4-digit number with unique digits.")
    print("Try to guess it! After each guess, I'll tell you:")
    print("- Bulls: correct digit in correct position")
    print("- Cows: correct digit in wrong position")
    print(f"\nInitial entropy: {initial_entropy:.4f} bits")
    print("\nEnter 'quit' to give up.\n")

    attempts = 0

    # Main game loop
    while True:
        attempts += 1

        # Input validation loop
        while True:
            guess = input(f"\nAttempt {attempts}. Enter your guess (4 unique digits): ").strip().lower()

            if guess == 'quit':
                print(f"\nGame over! The secret number was: {secret_code}")
                return

            if is_valid_guess(guess):
                break
            print("Invalid guess. Please enter exactly 4 unique digits.")

        # Process guess and provide feedback
        bulls, cows = compute_feedback(secret_code, guess)
        current_entropy = calculate_current_entropy(bulls, cows)

        # Display round results
        print(f"\nFeedback for {guess}:")
        print(f"Bulls: {bulls}")
        print(f"Cows: {cows}")
        print(f"Current entropy: {current_entropy:.4f} bits")

        # Check win condition
        if bulls == 4:
            print(f"\nCongratulations! You found the number {secret_code} in {attempts} attempts!")
            return

        # Check maximum attempts
        if attempts >= 20:
            print(f"\nToo many attempts! The secret number was: {secret_code}")
            return

if __name__ == "__main__":
    main()