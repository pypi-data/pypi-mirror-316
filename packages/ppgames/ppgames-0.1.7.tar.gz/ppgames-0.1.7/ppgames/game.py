import random
import socket
import threading
import time


def banner():
    print("""
 .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. |
| |   ______     | || |   ______     | || |    ______    | || |      __      | |
| |  |_   __ \   | || |  |_   __ \   | || |  .' ___  |   | || |     /  \     | |
| |    | |__) |  | || |    | |__) |  | || | / .'   \_|   | || |    / /\ \    | |
| |    |  ___/   | || |    |  ___/   | || | | |    ____  | || |   / ____ \   | |
| |   _| |_      | || |   _| |_      | || | \ `.___]  _| | || | _/ /    \ \_ | |
| |  |_____|     | || |  |_____|     | || |  `._____.'   | || ||____|  |____|| |
| |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------' 
    """)


# List of Indian bowlers
indian_bowlers = [
    "Kapil Dev", "Anil Kumble", "Harbhajan Singh", "Zaheer Khan", "Javagal Srinath",
    "Bhuvneshwar Kumar", "Mohammad Shami", "Ishant Sharma", "Ravichandran Ashwin", 
    "Jasprit Bumrah", "Ravindra Jadeja", "Sreesanth", "Kuldeep Yadav", "Yuzvendra Chahal",
    "Shreyas Gopal"
]

# Game loop function
def game_loop(player1_name, player2_name, connection=None):
    player_scores = {player1_name: 0, player2_name: 0}
    player_lives = {player1_name: 3, player2_name: 3}
    total_balls = 6  # Balls per over

    for over in range(1, 3):  # 2 overs per player
        print(f"\n--- Over {over} ---")
        bowler = random.choice(indian_bowlers)
        print(f"{bowler} is bowling...\n")
        
        for ball in range(1, total_balls + 1):
            for player in [player1_name, player2_name]:
                if player_lives[player] <= 0:
                    print(f"{player} is out of lives!")
                    continue

                print(f"{player}'s turn, Ball {ball}:")

                if connection and player == player2_name:  # Multiplayer input
                    connection.send("Your turn to bat! Enter your score (1-6): ".encode())
                    batting = int(connection.recv(1024).decode().strip())
                else:  # Local input
                    batting = int(input("Enter your batting score (1-6): "))

                bowling = random.randint(1, 6)
                print(f"Bowling: {bowling}")

                if batting == bowling:
                    player_lives[player] -= 1
                    print(f"{player} is OUT! Remaining lives: {player_lives[player]}")
                else:
                    player_scores[player] += batting
                    print(f"{player}'s score: {player_scores[player]}")

    print("\n--- Game Over! ---")
    print(f"Final Scores: {player1_name}: {player_scores[player1_name]}, {player2_name}: {player_scores[player2_name]}")
    if player_scores[player1_name] > player_scores[player2_name]:
        print(f"{player1_name} wins!")
    elif player_scores[player2_name] > player_scores[player1_name]:
        print(f"{player2_name} wins!")
    else:
        print("It's a tie!")

# Host game
def host_game():
    host_name = input("Enter your name: ")
    host_ip = socket.gethostbyname(socket.gethostname())
    print(f"Host IP: {host_ip}")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host_ip, 65432))
    server_socket.listen(1)
    print("Waiting for a player to join...")

    connection, addr = server_socket.accept()
    print(f"Player connected from {addr}")
    player2_name = connection.recv(1024).decode().strip()
    print(f"Player 2: {player2_name}")

    game_loop(host_name, player2_name, connection)
    connection.close()

# Join game
def join_game():
    host_ip = input("Enter the host's IP address: ")
    player2_name = input("Enter your name: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host_ip, 65432))
        client_socket.send(player2_name.encode())

        while True:
            message = client_socket.recv(1024).decode()
            if "Enter your score" in message:
                score = input(message)
                client_socket.send(score.encode())
            else:
                print(message)
    except ConnectionRefusedError:
        print("Failed to connect to the host. Ensure the host is running.")
    finally:
        client_socket.close()

# Main menu
def main():
    banner()
    print("1. Host Game")
    print("2. Join Game")
    print("3. Single Player")
    choice = input("Choose an option: ")

    if choice == "1":
        host_game()
    elif choice == "2":
        join_game()
    elif choice == "3":
        player1_name = input("Enter your name: ")
        game_loop(player1_name, "AI")
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
