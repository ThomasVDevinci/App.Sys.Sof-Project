import copy


class GameTree:
    def __init__(self, game):
        self.game = copy.deepcopy(game)
        self.children = []

    def generate_tree(self, depth):
        if depth == 0 or self.game.check_win():
            return
        for column in range(7):
            child_game = copy.deepcopy(self.game)
            child_game.drop_piece(column)
            child_game.switch_player()
            child_node = GameTree(child_game)
            child_node.generate_tree(depth - 1)
            self.children.append(child_node)
