def main():
    import argparse
    parser=argparse.ArgumentParser(description="Red-Blue Nim Game")
    parser.add_argument("num-red", type=int, default=10, help="Number of red marbles")
    parser.add_argument("num-blue", type=int, default=10, help="Number of blue marbles")
    parser.add_argument("version", choices=["standard","misere"], default="standard", help="Game Version")
    parser.add_argument("first_player", choices=["computer","human"], default="human", help="First Player")
    parser.add_argument("depth", type=int, default=5, help="Search depth for AI")

    arguments= parser.parse_args()
    game= NimGame(arguments.num_red, arguments.num_blue, arguments.version, arguments.first_player, arguments.depth)
    game.actual_game()

if __name__ == "__main__":
    main()


class NimGame:
    def __init__(self, num_red, num_blue, version, first_player, depth):
        self.num_red = num_red
        self.num_blue = num_blue
        self.version = version
        self.first_player = first_player
        self.depth = depth
        self.board = {"red" : num_red, "blue" : num_blue}
        self.score = 0

    def printing_board(self):
        print("Current board: Red = {}, Blue = {}".format(self.board["red"],self.board["blue"]))

    def is_terminal(self):
        return self.board["red"] == 0 or self.board["blue"] == 0

    def input_validation(self, message):
        while True:
            try:
                marbles=int(input(message))
                if marbles in [1,2]:
                    return marbles
                else:
                    raise ValueError("Invalid input,Please enter 1 or 2.")
            except ValueError as e:
                print("error",e)

    def delete_marbles(self, color, marbles):
        self.board[color] = self.board[color] - marbles

    def analysis (self):
        if self.version == "standard":
            return self.board["red"] - self.board["blue"]
        else:
            return self.board["blue"] - self.board["red"]
        
            
    def compute_score(self):
        self.score=self.board["red"] * 2 + self.board["blue"] * 3

    

    def minmax_procedure(self, depth, alpha, beta, maximize):
        if self.is_terminal():
            if self.version == "misere":
                return 1 if self.board["red"] == 0 else -1
            else:
                return -1 if self.board["red"] == 0 else 1
        if depth == 0:
            return self.analysis()
        if maximize:
            perfect_score = -float('inf')
            for color in ["red", "blue"]:
                for marbles in [1, 2]:
                    if self.board[color] >= marbles:
                        self.delete_marbles(color, marbles)
                        score = self.minmax_procedure(depth - 1, alpha, beta, False)
                        self.board[color] = self.board[color] + marbles
                        perfect_score = max(perfect_score, score)
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            break
            return perfect_score
        else:
            perfect_score=float('inf')
            for color in ["red","blue"]:
                for marbles in [1,2]:
                    if self.board[color] >= marbles:
                        self.delete_marbles(color, marbles)
                        score=self.minmax_procedure(depth -1, alpha, beta, True)
                        self.board[color] = self.board[color] + marbles
                        perfect_score = min(perfect_score, score)
                        beta= min(beta, score)
                        if beta <= alpha:
                            break
            return perfect_score
            
    def machine_turn(self):
        perfect_score = -float('inf')
        perfect_move = None
        for color in ["red", "blue"]:
            for marbles in [1, 2]:
                if self.board[color] >= marbles:
                    self.delete_marbles(color, marbles)
                    score=self.minmax_procedure(self.depth, -float('inf'), float('inf'), False)
                    self.board[color] += marbles
                    if score > perfect_score:
                        perfect_score = score
                        perfect_move = (color, marbles)
        self.delete_marbles(perfect_move[0], perfect_move[1])
        print("Machine removed {} {} marbles".format(perfect_move[1], perfect_move[0]))

    def actual_game(self):
        current_player = self.first_player
        while not self.is_terminal():
            self.printing_board()
            if current_player == "human":
                color=input("Enter color, 'red' or 'blue' to remove marble: ")
                marbles=self.input_validation("Enter 1 or 2 to remove marbles:")
                if marbles > self.board[color]:
                    print("you can't remove that number of marbles. there are only {} {} marbles left".format(self.board[color]))
                    continue
                self.delete_marbles(color, marbles)
            else:
                self.machine_turn()
            if self.is_terminal():
                self.compute_score()
                if current_player == "human":
                    print("Congratulations, You win!")
                else:
                    print("Machine won, Better luck next time.")
            if self.board["red"] == 0:
                print("game over, You removed all red marbles.")
                break
            current_player = "Machine" if current_player == "human" else "human"
        self.compute_score()
        print("Your final score is:", self.score)





                       

