from copy import deepcopy

class GOInterface:
    def print_board(self, board):
        for row in board:
            for col in row:
                print(col, end=' ')
            print()

    def copy_board(self, board):
        board_copy = deepcopy(board)
        return board_copy

    def compute_score(self, board, piece_type):
        cnt = 0
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == piece_type:
                    cnt += 1
        return cnt

    def opponent(self, piece_type):
        return 3-piece_type

    def neighbors(self, i, j, board):
        top = i-1
        bottom = i+1
        left = j-1
        right = j+1

        n = []
        if top >= 0:
            n.append((board[top][j], top, j))
        if bottom < len(board):
            n.append((board[bottom][j], bottom, j))
        if left >= 0:
            n.append((board[i][left], i, left))
        if right < len(board):
            n.append((board[i][right], i, right))

        return n

    def compute_groups(self, board):
        groups = [[], []]
        seen = set()
        for i in range(len(board)):
            for j in range(len(board)):
                if (i, j) not in seen and board[i][j]:
                    group = self.compute_group_dfs((i, j), set(), board)
                    groups[board[i][j] - 1].append(group)
                    seen |= group
        return groups
    
    def compute_group_dfs(self, coords, visited, board):
        visited |= {coords}
        neighbors = self.neighbors(coords[0], coords[1], board)
        for piece, i, j in neighbors:
            if piece == board[coords[0]][coords[1]] and (i,j) not in visited:
                self.compute_group_dfs((i, j), visited, board)
        return visited

    def compute_regions(self, board, groups):
        regions = [[], []]
        for side in range(len(groups)):
            for group in groups[side]:
                region = set()
                for point in group:
                    neighbors = self.neighbors(point[0], point[1], board)
                    neighbors = [(i, j) for n, i, j in neighbors if n != board[point[0]][point[1]]]
                    region |= set(neighbors)
                regions[side].append(region)
        return regions                    

    def print_regions(self, board, regions):
        for side in range(len(regions)):
            b = self.copy_board(board)
            for region in regions[side]:
                for i, j in region:
                    b[i][j] = '+'
            self.print_board(b)
            print()

    def compute_liberties(self, board, groups):
        liberties = [[], []]
        for i in range(len(groups)):
            for group in groups[i]:
                liberty = set()
                for point in group:
                    neighbors = self.neighbors(point[0], point[1], board)
                    liberty |= set([(i,j) for piece, i, j in neighbors if not piece])
                liberties[i].append(liberty)
        return liberties

    def get_liberty_counts(self, liberties):
        return [[len(liberty) for liberty in side] for side in liberties]
    
    def compute_edge_stones(self, board):
        stones = [[], []]
        stones[0] = [stone for stone in board[0] if stone == 1]
        stones[0] += [stone for stone in board[len(board)-1] if stone == 1]
        stones[1] = [stone for stone in board[0] if stone == 2]
        stones[1] += [stone for stone in board[len(board)-1] if stone == 2]
        for i in range(1, len(board)-1):
            if board[i][0] == 1:
                stones[0].append(board[i][0])
            if board[i][len(board)-1] == 1:
                stones[0].append(board[i][4])
            if board[i][0] == 2:
                stones[1].append(board[i][0])
            if board[i][len(board)-1] == 2:
                stones[1].append(board[i][4])
        counts = [len(st) for st in stones]
        return counts
        
    def compute_liberty_sums(self, board):
        sums = [0, 0]
        for i, row in enumerate(board):
            for j, col in enumerate(row):
                if col:
                    neighbors = self.neighbors(i, j, board)
                    neighbors = [(n, i, j) for n, i, j in neighbors if not n]
                    if col == 1:
                        sums[0] += len(neighbors)
                    if col == 2:
                        sums[1] += len(neighbors)
        return sums

    def compute_true_liberty_sums(self, board):
        sums = [0, 0]
        black = set()
        white = set()
        for i, row in enumerate(board):
            for j, col in enumerate(row):
                if col:
                    neighbors = self.neighbors(i, j, board)
                    if col == 1:
                        neighbors = [(i, j) for n, i, j in neighbors if not n and (i, j) not in black]
                        black |= set(neighbors)
                        sums[0] += len(neighbors)
                    if col == 2:
                        neighbors = [(i, j) for n, i, j in neighbors if not n and (i, j) not in white]
                        white |= set(neighbors)
                        sums[1] += len(neighbors)
        return sums

    def compute_territory(self, board):
        sums = [0, 0]
        for row in board:
            for col in row:
                if col == 1:
                    sums[0] += 1
                if col == 2:
                    sums[1] += 1
        return sums

    def compute_score(self, board):
        komi = 2.5
        scores = self.compute_territory(board)
        return [scores[0], scores[1]+komi]

    def compute_euler_number(self, board):
        e = [0, 0]
        for c in range(len(e)):
            b = self.copy_board(board)
            for i in range(len(b)):
                for j in range(len(b[i])):
                    if b[i][j] != (c+1):
                        b[i][j] = 0
            q1 = qD = q3 = 0
            for i in range(len(b) - 1):
                for j in range(len(b[i]) - 1):
                    window = [[b[i][j], b[i][j+1]], [b[i+1][j], b[i+1][j+1]]]
                    count = len([col for row in window for col in row if col == (c+1)])
                    if count == 1:
                        q1 += 1
                    if count == 3:
                        q3 += 1
                    if count == 2 and window[0][1] == window[1][0]:
                        qD += 1
            e[c] = (q1 + q3 - (2 * qD)) / 4

        return e

    def compute_convolutions(self, board):
        weights = { 
            (0, 0): 0.25, (0, 1): 0.5, (0, 2): 0.25,
            (1, 0): 0.5, (1, 1): 1, (1, 2): 0.5,
            (2, 0): 0.25, (2, 1): 0.5, (2, 2): 0.25
        }
        c = [0, 0]
        for side in range(len(c)):
            b = self.copy_board(board)
            for i in range(len(b) - 2):
                for j in range(len(b[i]) - 2):
                    window = [[b[i+m][j+k] for k in range(3)] for m in range(3)]
                    total = sum([1 if col==side+1 else 0 for row in window for col in row if col])
                    conv = total/9
                    c[side] += weights[(i, j)] * conv
        return [round(conv, 3) for conv in c]

    def evaluate_board(self, weights, territory=None, liberty=None, euler=None, edge_move=None, convolution=None):
        
        evaluation = 0
        evaluation += weights['territory'] * territory if territory else 0
        evaluation += weights['liberty'] * liberty if liberty else 0
        evaluation += weights['euler'] * euler if euler else 0
        evaluation += weights['edge_stone'] * edge_move if edge_move else 0
        evaluation += weights['convolution'] * convolution if convolution else 0
        
        return round(evaluation, 3)

    def compute_liberty(self, board, point):
        group = self.compute_group_dfs(point, set(), board)
        liberty = set()
        for point in group:
            neighbors = self.neighbors(point[0], point[1], board)
            liberty |= set([(i,j) for piece, i, j in neighbors if not piece])
        return liberty

    def apply_move(self, previous, move, piece_type):
        i, j = move
        board = self.copy_board(previous)
        board[i][j] = piece_type
        return board

    def compute_captures(self, board, move, piece_type):
        next = self.apply_move(board, move, piece_type)
        captures = []
        opponent = self.opponent(piece_type)
        g = self.compute_groups(next)
        l = self.compute_liberties(next, g)
        for group, liberty in zip(g[opponent-1], l[opponent-1]):
            if len(liberty) == 0:
                captures.append(group)
        return captures

    def compute_num_captures(self, captures):
        return len(captures)

    def remove_captured_pieces(self, board, captures):
        for group in captures:
                for i, j in group:
                    board[i][j] = 0
        return board

    def generate_successor(self, board, move, piece_type):
        if move == 'PASS':
            return self.copy_board(board)
        next = self.apply_move(board, move, piece_type)
        captures = self.compute_captures(board, move, piece_type) 
        if captures:
            next = self.remove_captured_pieces(next, captures)
        return next    
    
    def is_same(self, board_a, board_b):
        for row_a, row_b in zip(board_a, board_b):
            for col_a, col_b in zip(row_a, row_b):
                if col_a != col_b:
                    return False
        return True

    def is_valid_move(self, previous, board, move, piece_type):
        i, j = move
        if board[i][j]:
            return False
        else:
            captures = self.compute_captures(board, move, piece_type)
            next = self.apply_move(board, move, piece_type)
            if captures:
                next = self.remove_captured_pieces(next, captures)
            if not len(self.compute_liberty(next, move)):
                return False
        return not self.is_same(next, previous)
    
    def get_legal_moves(self, previous, board, piece_type):
        moves = [(i, j) for i in range(5) for j in range(5)]
        moves = [move for move in moves if self.is_valid_move(previous, board, move, piece_type)]
        moves.append('PASS')
        return moves