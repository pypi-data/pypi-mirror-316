import random
import time


def banner():
    
    print("""

 .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |   ______     | || |   ______     | || |    ______    | || |      __      | || | ____    ____ | || |  _________   | || |    _______   | |
| |  |_   __ \   | || |  |_   __ \   | || |  .' ___  |   | || |     /  \     | || ||_   \  /   _|| || | |_   ___  |  | || |   /  ___  |  | |
| |    | |__) |  | || |    | |__) |  | || | / .'   \_|   | || |    / /\ \    | || |  |   \/   |  | || |   | |_  \_|  | || |  |  (__ \_|  | |
| |    |  ___/   | || |    |  ___/   | || | | |    ____  | || |   / ____ \   | || |  | |\  /| |  | || |   |  _|  _   | || |   '.___`-.   | |
| |   _| |_      | || |   _| |_      | || | \ `.___]  _| | || | _/ /    \ \_ | || | _| |_\/_| |_ | || |  _| |___/ |  | || |  |`\____) |  | |
| |  |_____|     | || |  |_____|     | || |  `._____.'   | || ||____|  |____|| || ||_____||_____|| || | |_________|  | || |  |_______.'  | |
| |              | || |              | || |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 

          
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
    total_balls = 6  # 1 over has 6 balls
    total_overs = 6  # 6 overs in total
    ball_count = 0  # To track the number of balls bowled

    # Display a welcome message and instructions
    print(f"\nWelcome to the game, {player_name}!\n")
    time.sleep(1)
    print("In this game, you will be batting against 6 random bowlers, with each bowler bowling one over (6 balls).")
    print(f"You have {lives} lives. If you match the bowler's score on any ball, you lose one life.")
    print("The game ends either when you lose all lives or finish 6 overs.")
    print("Let's begin...\n")
    time.sleep(1)

    # Game loop for 6 overs
    for over in range(1, total_overs + 1):
        if lives <= 0:
            break  # Exit game if no lives are left

        print(f"\n--- Over {over} ---")
        
        # Randomly select one bowler for the over
        bowler = random.choice(indian_bowlers)
        print(f"{bowler} is bowling...\n")
        time.sleep(1)
        
        # Loop through 6 balls in the over
        for ball in range(1, total_balls + 1):
            if lives <= 0:
                break  # Exit the game if no lives are left

            print(f"Ball {ball}:")
            
            # Input for batting score
            while True:
                try:
                    batting = int(input(f"Enter your Batting Score (1-6) for Ball {ball}: "))
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

        if lives <= 0:
            break  # End the game if player loses all lives

    # Final score after all overs or lives are lost
    if lives > 0:
        print(f"\nGame Over! {player_name}, you've completed all {total_overs} overs.")
    print(f"Your final score is: {score}")

    return score
