import random
import time


def banner():
    
    print("""
░▒▓███████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓██████████████▓▒░░▒▓████████▓▒░░▒▓███████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
░▒▓███████▓▒░░▒▓███████▓▒░░▒▓█▓▒▒▓███▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░  ░▒▓██████▓▒░  
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░       ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░  
                                                                                                    """)

def run():
    banner()
    score = 0
    player_name = input("Enter Your Name: ")

    # List of Indian bowlers
    indian_bowlers = [
        "Kapil Dev", "Anil Kumble", "Harbhajan Singh", "Zaheer Khan", "Javagal Srinath",
        "Bhuvneshwar Kumar", "Mohammad Shami", "Ishant Sharma", "Ravichandran Ashwin", 
        "Jasprit Bumrah", "Ravindra Jadeja", "Sreesanth", "Kuldeep Yadav", "Yuzvendra Chahal",
        "Shreyas Gopal"
    ]
    
    # Set lives to 3
    lives = 3
    total_balls = 6  # 1 over has 6 balls (for simplicity in this case)
    total_overs = 6  # 6 overs in total
    ball_count = 0  # To track number of balls bowled

    # Display a welcome message and instructions
    print(f"\nWelcome to the game, {player_name}!\n")
    time.sleep(1)
    print("In this game, you will be batting against 6 random bowlers, with 6 balls each over.")
    print(f"You have {lives} lives. If you match the bowler's score on any ball, you lose one life.")
    print("The game ends either when you lose all lives or finish 6 overs.")
    print("Let's begin...\n")
    time.sleep(1)

    # Game loop
    while lives > 0 and ball_count < total_overs * total_balls:
        print(f"\nOver {ball_count // total_balls + 1} - Ball {ball_count % total_balls + 1}")

        # Select 6 random bowlers for the over
        bowlers_for_over = random.sample(indian_bowlers, 6)
        
        # Loop through the 6 bowlers (6 balls in an over)
        for bowler in bowlers_for_over:
            if lives <= 0 or ball_count >= total_overs * total_balls:
                break  # End the game if the player has no lives left or the over limit is reached

            print(f"{bowler} is bowling...")
            time.sleep(1)

            # Input for batting score
            while True:
                try:
                    batting = int(input(f"Enter your Batting Score (1-6) for Ball {ball_count % total_balls + 1}: "))
                    if 1 <= batting <= 6:
                        break
                    else:
                        print("Invalid input! Please enter a number between 1 and 6.")
                except ValueError:
                    print("Please enter a valid integer between 1 and 6.")

            bowling = random.randint(1, 6)  # Random bowling score

            # Check if the batting score matches the bowling score
            if batting == bowling:
                lives -= 1
                print(f"Oops! You were bowled out by {bowler}.")
                print(f"Remaining Lives: {lives}")
                if lives <= 0:
                    print(f"\nGame Over! {player_name}, you lost all your lives.")
                    break
            else:
                score += batting
                print(f"Batting: {batting}, Bowling: {bowling}, Your score: {score}")
                
            ball_count += 1

        # After completing an over, check if the game should continue
        if ball_count >= total_overs * total_balls:
            break
    
    # Final score after all overs or lives are lost
    if lives > 0:
        print(f"\nGame Over! {player_name}, you've completed all {total_overs} overs.")
    print(f"Your final score is: {score}")

    return score
