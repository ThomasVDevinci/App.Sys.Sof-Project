from GameTree import GameTree


class AIPlayer:
    def __init__(self, game):
        self.game = game

    def depth_first_search(self, node):
        # Implement your DFS algorithm here
        pass

    def find_best_move(self):
        game_tree = GameTree(self.game)
        game_tree.generate_tree(3)  # Generate the game tree to a depth of 3
        return self.depth_first_search(game_tree)
