import random
import time
import socket


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





# List of Indian bowlers
indian_bowlers = [
    "Kapil Dev", "Anil Kumble", "Harbhajan Singh", "Zaheer Khan", "Javagal Srinath",
    "Bhuvneshwar Kumar", "Mohammad Shami", "Ishant Sharma", "Ravichandran Ashwin", 
    "Jasprit Bumrah", "Ravindra Jadeja", "Sreesanth", "Kuldeep Yadav", "Yuzvendra Chahal",
    "Shreyas Gopal"
]

# Game loop for single-player or multiplayer
def game_loop(player1_name, player2_name=None, is_multiplayer=False, host_ip=None):
    player1_score = 0
    player2_score = 0
    player1_lives = 3
    player2_lives = 3
    total_balls = 6  # Each over has 6 balls
    total_overs = 6  # 6 overs in total
    ball_count = 0  # Track the number of balls bowled
    current_player = 1  # Track the current player
    player2_connected = False  # Track if the second player is connected

    if is_multiplayer:
        # Multiplayer - Client (Second Player)
        if host_ip:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host_ip, 65432))  # Connect to the host
            client_socket.send(f"{player2_name}\n".encode())  # Send player 2's name

            player2_connected = True  # Player 2 is connected
            print(f"{player2_name} has connected to the game!")

    else:
        # Single-player mode
        print(f"\nWelcome to the game, {player1_name}!\n")
        time.sleep(1)
        print("Let's begin...\n")
        time.sleep(1)

    # Game loop for 3 overs per player
    for over in range(1, total_overs + 1):
        if player1_lives <= 0 and player2_lives <= 0:
            break  # Exit game if both players lose all lives
        
        print(f"\n--- Over {over} ---")

        # Select random bowler for this over
        bowler = random.choice(indian_bowlers)
        print(f"{bowler} is bowling...\n")
        time.sleep(1)

        for ball in range(1, total_balls + 1):
            if player1_lives <= 0 and player2_lives <= 0:
                break  # Exit game if both players lose all lives

            print(f"Ball {ball}:")
            batting = int(input("Batting Score (1-6): "))
            
            if batting >= 1 and batting <= 6:
                bowling = random.randint(1, 6)  # Random bowling score

                # Check if the player has lost a life
                if batting == bowling:
                    if current_player == 1:
                        player1_lives -= 1
                        print(f"{player1_name} lost a life! Remaining lives: {player1_lives}")
                    else:
                        player2_lives -= 1
                        print(f"{player2_name} lost a life! Remaining lives: {player2_lives}")
                    print(f"Your score is: {player1_score if current_player == 1 else player2_score}")
                    break
                else:
                    if current_player == 1:
                        player1_score += batting
                    else:
                        player2_score += batting

                print(f"Batting: {batting}, Bowling: {bowling}, {player1_name if current_player == 1 else player2_name}'s score: {player1_score if current_player == 1 else player2_score}")
                
            else:
                print("Invalid batting score. Please enter a number between 1 and 6.")

            # Alternate between Player 1 and Player 2 in multiplayer
            if is_multiplayer:
                if current_player == 1:
                    current_player = 2
                else:
                    current_player = 1

            # Send the game status to the second player (if multiplayer mode)
            if player2_connected and is_multiplayer:
                client_socket.send(f"{player1_score},{player2_score},{player1_lives},{player2_lives}\n".encode())

        # Print the score after each over
        print(f"{player1_name}'s score: {player1_score}, {player2_name}'s score: {player2_score}")

    # End game and print the final scores
    print(f"\nGame Over! Final Scores:")
    print(f"{player1_name}'s score: {player1_score}")
    print(f"{player2_name}'s score: {player2_score}")

    if player1_score > player2_score:
        print(f"{player1_name} wins!")
    elif player2_score > player1_score:
        print(f"{player2_name} wins!")
    else:
        print("It's a tie!")

# Server side (Host) function
def host_game():
    host_name = input("Enter Player 1 Name: ")
    host_ip = socket.gethostbyname(socket.gethostname())  # Get the local IP address of the host machine
    print(f"Your IP address (Host): {host_ip}")
    player2_name = input("Enter Player 2 Name: ")

    # Start server thread to handle player 2 connection
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host_ip, 65432))  # Bind to the local IP address and port
    server_socket.listen(1)
    print("Waiting for Player 2 to connect...")

    # Accept connection from player 2
    player2_connection, player2_address = server_socket.accept()
    print(f"Player 2 connected from {player2_address}")
    
    # Receive player 2 name
    player2_name = player2_connection.recv(1024).decode().strip()
    print(f"Player 2's name: {player2_name}")

    # Run the game in multiplayer mode
    game_loop(host_name, player2_name, is_multiplayer=True, host_ip=host_ip)

# Client side (Joiner) function
def join_game():
    host_ip = input("Enter the IP address of the host: ")
    player2_name = input("Enter Player 2 Name: ")

    # Run the game in multiplayer mode
    game_loop(None, player2_name, is_multiplayer=True, host_ip=host_ip)

# Main Menu - Select Game Mode
def run():
    print("Welcome to PPGames!")
    print("1. Single Player")
    print("2. Multiplayer")

    choice = input("Select the game mode (1 or 2): ")

    if choice == "1":
        player1_name = input("Enter Player 1 Name: ")
        game_loop(player1_name)
    elif choice == "2":
        mode = input("Select mode (1 for Host, 2 for Join): ")

        if mode == "1":
            host_game()
        elif mode == "2":
            join_game()
        else:
            print("Invalid mode selected.")


