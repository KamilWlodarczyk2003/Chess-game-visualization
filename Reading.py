class MoveReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.moves = self.read_moves()

    def read_moves(self):
        moves_list = []
        with open(self.file_path, 'r') as file:
            for line in file:
                start, end = line.strip().split('-')
                moves_list.append((start, end))
        return moves_list