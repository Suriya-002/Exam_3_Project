'''
Bulls and Cows Game Solver using Information Theory
This implementation uses entropy-based approach to make optimal guesses
by maximizing information gain at each step of the game.
'''
import itertools
import math
from typing import List, Tuple, Dict

def compute_feedback(secret: str, guess: str) -> Tuple[int, int]:
    """
    Compute the feedback for a guess in terms of bulls and cows.
    Uses a marking strategy to avoid double-counting digits.
    
    Args:
        secret (str): The secret code to be matched against
        guess (str): The current guess being evaluated
        
    Returns:
        Tuple[int, int]: A tuple containing (bulls, cows) where:
            - bulls: number of correct digits in correct positions
            - cows: number of correct digits in wrong positions
            
    Example:
        >>> compute_feedback("1234", "1432")
        (2, 2)  # 1,4 are bulls; 2,3 are cows
    """
    # Create copies of strings as lists to mark used digits
    secret_digits = list(secret)
    guess_digits = list(guess)
    bulls = 0
    cows = 0

    # First count bulls
    for i in range(4):
        if guess_digits[i] == secret_digits[i]:
            bulls += 1
            # Mark matched positions with special characters to avoid reuse
            secret_digits[i] = 'x'
            guess_digits[i] = 'y'

    # Then count cows (avoiding marked positions)
    for i in range(4):
        if guess_digits[i] != 'y' and guess_digits[i] in secret_digits:
            cows += 1
            # Mark the used digit in secret to avoid double counting
            secret_digits[secret_digits.index(guess_digits[i])] = 'z'

    return (bulls, cows)

def filter_codes(possible_codes: List[str], guess: str, bulls: int, cows: int) -> List[str]:
    """
    Filter the possible codes based on the feedback received.
    Eliminates codes that wouldn't give the same feedback for the guess.
    
    Args:
        possible_codes (List[str]): List of remaining possible secret codes
        guess (str): The guess that was made
        bulls (int): Number of bulls in the feedback
        cows (int): Number of cows in the feedback
        
    Returns:
        List[str]: Filtered list of codes that remain possible
    """
    filtered = []
    for code in possible_codes:
        b, c = compute_feedback(code, guess)
        if b == bulls and c == cows:
            filtered.append(code)
    return filtered

def calculate_entropy(possible_codes: List[str], guess: str) -> float:
    """
    Calculate the expected information gain (entropy) for a given guess.
    Uses Shannon entropy formula: -Σ P(x) * log₂(P(x))
    
    Args:
        possible_codes (List[str]): List of remaining possible secret codes
        guess (str): The guess to evaluate
        
    Returns:
        float: Expected information gain in bits
        
    Note:
        Higher entropy indicates better guesses that will eliminate more possibilities
        on average.
    """
    total_codes = len(possible_codes)
    if total_codes == 0:
        return 0.0

    # Count frequency of each possible feedback
    feedback_counts: Dict[Tuple[int, int], int] = {}
    for code in possible_codes:
        feedback = compute_feedback(code, guess)
        feedback_counts[feedback] = feedback_counts.get(feedback, 0) + 1

    # Calculate Shannon entropy
    entropy = 0.0
    for count in feedback_counts.values():
        probability = count / total_codes
        entropy -= probability * math.log2(probability)

    return entropy

def find_best_guess(possible_codes: List[str], all_codes: List[str]) -> Tuple[str, float]:
    """
    Find the optimal guess that maximizes expected information gain.
    Considers all possible codes as guesses, not just the remaining possibilities.
    
    Args:
        possible_codes (List[str]): List of remaining possible secret codes
        all_codes (List[str]): List of all valid codes that can be guessed
        
    Returns:
        Tuple[str, float]: The best guess and its expected information gain
        
    Note:
        Uses an optimization where it stops searching if maximum possible
        entropy is achieved (log2 of number of possibilities).
    """
    max_entropy = -1
    best_guess = possible_codes[0]

    # Evaluate each possible guess
    for guess in all_codes:
        entropy = calculate_entropy(possible_codes, guess)
        if entropy > max_entropy:
            max_entropy = entropy
            best_guess = guess

        # Early stopping if we've found optimal entropy
        if abs(max_entropy - math.log2(len(possible_codes))) < 1e-10:
            break

    return best_guess, max_entropy

def main() -> None:
    """
    Main game loop implementing the Bulls and Cows solver.
    Computer tries to guess the human player's secret code using
    information theory to make optimal guesses.
    
    Features:
    - Uses entropy calculations to make intelligent guesses
    - Tracks remaining possibilities and entropy
    - Validates user feedback
    - Detects contradictions in feedback
    """
    # Generate all possible 4-digit codes with unique digits
    all_codes = [''.join(p) for p in itertools.permutations('0123456789', 4)]
    possible_codes = all_codes.copy()

    # Display game instructions
    print("Think of a 4-digit number with unique digits.")
    print("For each guess, provide the number of bulls and cows.")
    print("Bulls: correct digit in correct position")
    print("Cows: correct digit in wrong position\n")

    attempts = 0

    # Main game loop
    while True:
        attempts += 1
        # Calculate and display current game state
        current_entropy = math.log2(len(possible_codes)) if possible_codes else 0
        print(f"\nCurrent entropy: {current_entropy:.4f} bits")
        print(f"Possible codes remaining: {len(possible_codes)}")

        # Find and make the best guess
        guess, expected_entropy = find_best_guess(possible_codes, all_codes)
        print(f"\nAttempt {attempts}: Computer guesses {guess}")
        print(f"Expected information gain: {expected_entropy:.4f} bits")

        # Get and validate user feedback
        while True:
            try:
                feedback = input("Enter feedback as 'Bulls Cows' (or 'win' if correct): ").strip().lower()
                if feedback == 'win':
                    print(f"\nComputer won in {attempts} attempts!")
                    return
                bulls, cows = map(int, feedback.split())
                if 0 <= bulls <= 4 and 0 <= cows <= 4 and bulls + cows <= 4:
                    break
                print("Invalid feedback. Bulls and cows should be between 0 and 4, and their sum ≤ 4.")
            except ValueError:
                print("Invalid input. Please enter two numbers separated by space, or 'win'.")

        # Update possible codes based on feedback
        possible_codes = filter_codes(possible_codes, guess, bulls, cows)

        # Check for contradictions or solution
        if not possible_codes:
            print("Error: No possible codes remain. Please check your feedback.")
            return

        if len(possible_codes) == 1:
            print(f"\nOnly one possibility remains: {possible_codes[0]}")
            print("This must be your number!")
            return

if __name__ == "__main__":
    main()