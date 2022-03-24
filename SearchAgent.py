from Agent import Agent
from GO import GO

class SearchAgent(Agent):
    def __init__(self, previous, current, piece_type, weights, use_sorted=True, pruning_stats=False):
        super().__init__(previous, current, piece_type)
        self.weights = weights
        self.pruning_stats = pruning_stats
        if self.pruning_stats:
            self.searched_nodes = 0
            self.pruned_nodes = 0
        self.use_sorted = use_sorted

    def update_pruning_stats(self, searched, pruned):
        self.pruned_nodes += pruned
        self.searched_nodes += searched

    def get_search_depth(self, length):
        if length > 20:
            depth = 3 #2 (alternates)
        elif length <= 20 and length > 15:
            depth = 4 #3 (alternates)
        elif length <= 15 and length > 10:
            depth = 4
        elif length <= 10 and length > 5:
            depth = 5
        else:
            depth = 5
        
        return depth

    def evaluate(self, state):
        L, T, E, H, C = state.get_evaluation()
        return min(self.interface.evaluate_board(self.weights, T, L, H, E, C), state.compute_score())

    def init_alpha_beta(self, alpha, beta):
        moves = self.state.get_legal_moves()
        best_move = None
        score = -self.INFINITY
        counter = 0

        if moves == ['PASS']:
            return moves[0]

        depth = self.get_search_depth(len(moves))        

        for move in moves:
            counter += 1
            next_board = self.state.generate_successor(move)
            next_state = GO(self.interface.copy_board(self.state.current), next_board, self.state.opp)
            current = -self.alpha_beta(-beta, -alpha, next_state, depth-1)
            if current > score:
                best_move = move
                score = current
            if score > alpha:
                alpha = score
            if alpha >= beta:
                if self.pruning_stats:
                    self.update_pruning_stats(len(moves), len(moves)-counter)
                return alpha, best_move
        
        if self.pruning_stats:
            self.update_pruning_stats(len(moves), len(moves)-counter)
        return score, best_move

    def init_sorted_alpha_beta(self, alpha, beta, m=None, l=None):
        if not m:
            moves = self.state.get_legal_moves()
        else:
            moves = m
        
        best_move = None
        score = -self.INFINITY
        counter = 0

        if moves == ['PASS']:
            return moves[0]

        depth = self.get_search_depth(len(moves) if not l else l)

        next_states = [GO(self.interface.copy_board(self.state.current), self.state.generate_successor(move), self.state.opp) for move in moves]
        evaluations = [self.evaluate(next_state) for next_state in next_states]
        mse = [(m, s, -e) for m, s, e, in zip(moves, next_states, evaluations)]
        mse.sort(key=lambda x: x[2], reverse=True)

        for move, next_state, _ in mse:
            counter += 1
            current = -self.sorted_alpha_beta(-beta, -alpha, next_state, depth-1, (1, depth) if move == 'PASS' else (0, depth))
            if current > score:
                best_move = move
                score = current
            if score > alpha:
                alpha = score
            if alpha >= beta:
                if self.pruning_stats:
                    self.update_pruning_stats(len(moves), len(moves)-counter)
                return alpha, best_move
        
        if self.pruning_stats:
            self.update_pruning_stats(len(moves), len(moves)-counter)
        return score, best_move

    def alpha_beta(self, alpha, beta, state, depth):
        if depth == 0:
            return self.evaluate(state)
        
        score = -self.INFINITY
        moves = state.get_legal_moves()
        counter = 0

        for move in moves:
            counter += 1
            next_board = state.generate_successor(move)
            next_state = GO(self.interface.copy_board(state.current), next_board, state.opp)
            current = -self.alpha_beta(-beta, -alpha, next_state, depth-1)
            if current > score:
                score = current
            if score > alpha:
                alpha = score
            if alpha >= beta:
                if self.pruning_stats:
                    self.update_pruning_stats(len(moves), len(moves)-counter)
                return alpha
        
        if self.pruning_stats:
             self.update_pruning_stats(len(moves), len(moves)-counter)
        return score

    def sorted_alpha_beta(self, alpha, beta, state, depth, passes):
        if depth == 0:
            return self.evaluate(state)
        
        if passes[0] == 2:
            return self.evaluate(state)

        score = -self.INFINITY
        
        moves = state.get_legal_moves()
        next_states = [GO(self.interface.copy_board(state.current), state.generate_successor(move), state.opp) for move in moves]
        evaluations = [self.evaluate(next_state) for next_state in next_states]
        mse = [(m, s, -e) for m, s, e, in zip(moves, next_states, evaluations)]
        mse.sort(key=lambda x: x[2], reverse=True)
        
        counter = 0

        for m, next_state, _ in mse:
            counter += 1
            if m == 'PASS':
                p = (passes[0] + 1, depth) if passes[1] == depth + 1 else (1, depth)
            else:
                p = passes
            current = -self.sorted_alpha_beta(-beta, -alpha, next_state, depth-1, p)
            if current > score:
                score = current
            if score > alpha:
                alpha = score
            if alpha >= beta:
                if self.pruning_stats:
                    self.update_pruning_stats(len(moves), len(moves)-counter)
                return alpha
        
        if self.pruning_stats:
            self.update_pruning_stats(len(moves), len(moves)-counter)
        return score

    def get_input(self, state, piece_type):
        self.update_state(state)
        if self.is_best_to_pass():
            return 'PASS'
        if self.use_sorted:
            move = self.init_sorted_alpha_beta(-self.INFINITY, self.INFINITY)[1]
            return move
        return self.init_alpha_beta(-self.INFINITY, self.INFINITY)[1]

    def get_move(self, m=None, l=None):
        if self.is_best_to_pass():
            return 'PASS'
        if self.use_sorted:
            move = self.init_sorted_alpha_beta(-self.INFINITY, self.INFINITY, m, l)[1]
            return move
        return self.init_alpha_beta(-self.INFINITY, self.INFINITY)[1]