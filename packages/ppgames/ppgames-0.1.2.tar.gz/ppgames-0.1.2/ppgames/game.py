import random
import time

def run():
    score = 0
    player_name = input("Enter Your Name: ")

    # List of Indian bowlers
    indian_bowlers = [
        "Kapil Dev", "Anil Kumble", "Harbhajan Singh", "Zaheer Khan", "Javagal Srinath",
        "Bhuvneshwar Kumar", "Mohammad Shami", "Ishant Sharma", "Ravichandran Ashwin", 
        "Jasprit Bumrah", "Ravindra Jadeja", "Sreesanth", "Kuldeep Yadav", "Yuzvendra Chahal",
        "Shreyas Gopal"
    ]

    # Display a welcome message and instructions
    print(f"\nWelcome to the game, {player_name}!\n")
    time.sleep(1)
    print("In this game, you will be batting against a random bowler from the list of Indian legends.")
    print("Try to match your batting score with the bowler's to win!")
    print("Let's begin...\n")
    time.sleep(1)

    # Game loop
    while True:
        # Choose a random bowler
        bowler = random.choice(indian_bowlers)

        # Simulate the bowling
        print(f"{bowler} is bowling...\n")
        time.sleep(2)

        # Input for batting score
        while True:
            try:
                batting = int(input("Enter your Batting Score (1-6): "))
                if 1 <= batting <= 6:
                    break
                else:
                    print("Invalid input! Please enter a number between 1 and 6.")
            except ValueError:
                print("Please enter a valid integer between 1 and 6.")

        bowling = random.randint(1, 6)  # Random bowling score

        # Check if the batting score matches the bowling score
        if batting == bowling:
            print(f"Oops! {player_name}, you were bowled out by {bowler}.")
            print(f"Your final score is: {score}")
            break
        else:
            score += batting
            print(f"Batting: {batting}, Bowling: {bowling}, Your score: {score}")

        # Ask if the player wants to continue playing
        play_again = input("\nDo you want to continue playing? (y/n): ").strip().lower()
        if play_again != 'y':
            print(f"Game Over! {player_name}, your final score is: {score}")
            break

    return score
