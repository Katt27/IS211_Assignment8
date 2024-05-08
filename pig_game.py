import random
import time
import argparse

class Player:
    """Base class for all types of players."""
    def __init__(self, name):
        self.name = name
        self.score = 0

    def roll_or_hold(self, current_turn_score):
        raise NotImplementedError("Subclasses should implement this!")

    def add_score(self, points):
        self.score += points

class HumanPlayer(Player):
    """Human player that makes decisions based on user input."""
    def roll_or_hold(self, current_turn_score):
        decision = input(f"{self.name}, your current turn score is {current_turn_score}. Roll or hold? (r/h): ")
        return 'hold' if decision.lower().startswith('h') else 'roll'

class ComputerPlayer(Player):
    """Computer player with a basic AI to determine when to roll or hold."""
    def roll_or_hold(self, current_turn_score):
        if self.score + current_turn_score >= 100 or current_turn_score >= 25 or (100 - self.score) <= 25:
            return "hold"
        else:
            return "roll"

class PlayerFactory:
    """Factory to create players based on type."""
    @staticmethod
    def create_player(player_type, name):
        if player_type == "human":
            return HumanPlayer(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError("Invalid player type")

class Game:
    """Main game logic handling the gameplay."""
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_player = 0

    def play_turn(self):
        player = self.players[self.current_player]
        turn_score = 0
        while True:
            decision = player.roll_or_hold(turn_score)
            if decision == "hold":
                player.add_score(turn_score)
                break
            else:
                roll = self.roll_dice()
                if roll == 1:
                    turn_score = 0
                    break
                else:
                    turn_score += roll
        self.current_player = 1 - self.current_player

    @staticmethod
    def roll_dice():
        return random.randint(1, 6)

class TimedGameProxy(Game):
    """Proxy class to add timing functionality to the game."""
    def __init__(self, player1, player2):
        super().__init__(player1, player2)
        self.start_time = time.time()

    def play_turn(self):
        if time.time() - self.start_time > 60:  # One minute time limit
            raise TimeoutError("Time limit reached")
        super().play_turn()

def main():
    parser = argparse.ArgumentParser(description="Play the game of Pig.")
    parser.add_argument('--player1', type=str, choices=['human', 'computer'], required=True)
    parser.add_argument('--player2', type=str, choices=['human', 'computer'], required=True)
    parser.add_argument('--timed', action='store_true')
    args = parser.parse_args()

    player1 = PlayerFactory.create_player(args.player1, "Player 1")
    player2 = PlayerFactory.create_player(args.player2, "Player 2")

    game = TimedGameProxy(player1, player2) if args.timed else Game(player1, player2)

    try:
        while player1.score < 100 and player2.score < 100:
            game.play_turn()
            print(f"Scores: {player1.name} {player1.score}, {player2.name} {player2.score}")
            if player1.score >= 100 or player2.score >= 100:
                winner = player1 if player1.score > player2.score else player2
                print(f"{winner.name} wins!")
                break
    except TimeoutError as e:
        print(e)
        winner = player1 if player1.score > player2.score else player2
        print(f"Game ended by timeout. Winner: {winner.name}")

if __name__ == "__main__":
    main()
