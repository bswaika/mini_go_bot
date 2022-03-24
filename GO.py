from GOInterface import GOInterface

class GO(GOInterface):
    def __init__(self, prev_board, board, piece_type):
        self.previous = prev_board
        self.current = board
        self.test_board = None
        self.side = piece_type
        self.opp = self.opponent(self.side)
        self.groups = self.compute_groups(self.current)
        self.liberties = self.compute_liberties(self.current, self.groups)

    def get_groups(self):
        return self.groups

    def get_liberties(self):
        return self.liberties
    
    def get_liberty_counts(self):
        return super().get_liberty_counts(self.liberties)

    def get_legal_moves(self):
        return super().get_legal_moves(self.previous, self.current, self.side)
    
    def generate_successor(self, move):
        return super().generate_successor(self.current, move, self.side)
    
    def compute_score(self):
        score = super().compute_score(self.current)
        return score[self.side - 1]

    def get_evaluation(self):
        true_liberty = super().compute_true_liberty_sums(self.current)
        territory = super().compute_territory(self.current)
        edge_stone = super().compute_edge_stones(self.current)
        euler_number = super().compute_euler_number(self.current)
        convolution = super().compute_convolutions(self.current)

        evaluation_vector = (
            true_liberty[self.side - 1] - true_liberty[self.opp - 1],
            territory[self.side - 1] - territory[self.opp - 1],
            edge_stone[self.side - 1] - edge_stone[self.opp - 1],
            euler_number[self.side - 1] - euler_number[self.opp - 1],
            convolution[self.side - 1] - convolution[self.opp - 1] 
        )

        return evaluation_vector