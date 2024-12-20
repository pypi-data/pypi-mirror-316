# ppgames/game.py
import random

def run():
    score = 0

    while True:
        # Input for batting score
        batting = int(input("Batting Score(1-6): "))
        
        if batting >= 1 and batting <= 6:
            bowling = random.randint(1, 6)  # Random bowling score

            if batting == bowling:
                print(f"Your score is: {score}")
                break
            else:
                score += batting

            print(f"Batting: {batting}, Bowling: {bowling}, Your score: {score}")
        else:
            print("Invalid batting score. Please enter a number between 1 and 6.")

    return score
