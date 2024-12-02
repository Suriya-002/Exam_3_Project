# Bulls and Cows Game with Information Theory

This repository contains two implementations of the classic Bulls and Cows game, both utilizing information theory principles. The first implementation has the computer generate a secret code while tracking uncertainty as the user guesses, while the second implementation demonstrates an optimal computer solver using entropy-based decision making.

## Game Rules
Bulls and Cows is a code-breaking game where:
- The secret code is a 4-digit number with unique digits (0-9)
- After each guess, feedback is given as:
  - Bulls: Correct digits in correct positions
  - Cows: Correct digits in wrong positions
- The goal is to guess the secret code in as few attempts as possible

## Implementations

### 1. User Guessing Implementation (`Bulls_and_Cows_User_Guessing.py`)
In this version:
- Computer generates a random 4-digit secret code
- Player makes guesses and receives feedback
- Program tracks remaining uncertainty using entropy calculations
- Game ends when the correct code is guessed or after 20 attempts
- Features a 'quit' option

#### Key Features:
- Entropy tracking after each guess
- Input validation for guesses
- Real-time feedback with bulls and cows
- Running entropy calculation display

### 2. Computer Solver Implementation (`Bulls_and_Cows_Computer_Guessing.py`)
In this version:
- User thinks of a secret code
- Computer makes optimal guesses using information theory
- User provides feedback as bulls and cows
- Computer narrows down possibilities until finding the solution

#### Key Features:
- Entropy-based guess optimization
- Efficient filtering of impossible codes
- Expected information gain calculations
- Progress tracking with remaining possibilities

## Information Theory Concepts

Both implementations use information theory principles:

### User Game Entropy
- Initial entropy: 13.29 bits (log2(10) * 4 positions)
- Entropy reduction based on bulls and cows
- Bulls provide complete position certainty
- Cows provide partial digit certainty

### Computer Solver Entropy
- Uses Shannon's entropy formula for guess evaluation
- Calculates expected information gain
- Makes decisions to maximize information gain
- Typically solves the puzzle in 5-6 guesses

