from GO import GO
from GOInterface import GOInterface

class Agent:
    INFINITY = 10000000000

    def __init__(self, previous, current, piece_type):
        self.side = piece_type
        self.state = GO(previous, current, self.side)
        self.interface = GOInterface()
        self.score = self.interface.compute_score(self.state.current)
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.type = 'AGENT'
    
    def is_best_to_pass(self):
        '''
            GENERAL STRATEGY
            Initial Passing Strategy to check that if the opponent passed
            and my current score is greater than the opponent then the
            winning move is to pass rather than carry the game forward
        '''
        if self.interface.is_same(self.state.previous, self.state.current):
            if self.score[self.side - 1] > self.score[self.state.opp - 1]:
                return True
        return False

    def update_result(self, result):
        if result == self.side:
            self.wins += 1
        elif result == 0:
            self.draws += 1
        else:
            self.losses += 1

    def get_performance(self):
        total_played = self.wins + self.losses + self.draws

        return self.wins/total_played, self.losses/total_played, self.draws/total_played

    def update_state(self, state):
        self.state = GO(self.interface.copy_board(state.previous_board), self.interface.copy_board(state.board), self.side)