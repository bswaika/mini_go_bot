from SearchAgent import SearchAgent

class MoveGenerator:
    def __init__(self, files=['input.txt', 'output.txt']):
        self.side, self.previous, self.current = self.parse(files[0])
        # self.exec_move_counter(files[2])
        # remaining_moves = 24 - self.moves
        self.search_agent = SearchAgent(self.previous, self.current, self.side, self.get_search_weights())
        move = self.search_agent.get_move()
        self.generate(move, files[1])

    def count_board(self):
        p_count = 0
        c_count = 0
        for row in self.previous:
            for col in row:
                if col != 0:
                    p_count += 1

        for row in self.current:
            for col in row:
                if col != 0:
                    c_count += 1
        
        return p_count, c_count

    def exec_move_counter(self, filename):
        p, c = self.count_board()
        if self.side == 1 and p == 0 and c == 0:
            self.moves = 0
            with open(filename, 'w') as outfile:
                outfile.write('1')
            return
        if self.side == 2 and p == 0 and c == 1:
            self.moves = 1
            with open(filename, 'w') as outfile:
                outfile.write('2')
            return
        with open(filename, 'w') as outfile:
            self.moves = int(outfile.readline())
            outfile.write(str(self.moves + 2))
        return

    def get_search_weights(self):
        return {
            'territory': 1, 
            'liberty': 0.75, 
            'euler': -3, 
            'edge_stone': -1.5, 
            'convolution': 2
        }

    def parse(self, file):
        with open(file) as infile:
            piece = int(infile.readline())
            lines = infile.readlines()
            previous_board = []
            current_board = []  
            for line in lines[:5]:
                row = []
                for char in line:
                    if char != '\n':
                        row.append(int(char))
                previous_board.append(row)
            for line in lines[5:]:
                row = []
                for char in line:
                    if char != '\n':
                        row.append(int(char))
                current_board.append(row)

        return piece, previous_board, current_board
    
    def generate(self, move, file):
        with open(file, 'w') as outfile:
            if move == 'PASS':
                outfile.write(move)
            else:
                outfile.write(str(move[0]) + ',' + str(move[1]))
