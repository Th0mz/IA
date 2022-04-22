# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 67:
# 95599 Joao Ramalho
# 95680 Tomas Tavares

import sys
from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search

ROW = 0
COL = 1
VALUE = 2


def sequencesCopy (sequences):
    new_sequences = []
    for sequence in sequences:
        new_sequence = []
        for position in sequence:
            new_sequence.append(position)
        new_sequences.append(new_sequence)
    return new_sequences

def copyBoardLine(board, row):
    new_board = []
    for i in range(len(board)):
        new_line = board[i]
        if i == row:
            new_line = new_line.copy()
        
        new_board.append(new_line)

    return new_board


class NumbrixState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = NumbrixState.state_id
        NumbrixState.state_id += 1


    def __lt__(self, other):
        return self.id < other.id

    def number_blank_positions (self):
        return self.board.get_number_of_blank_positions()

    def apply_action(self, action):
        row, col, value = action

        board_representation = copyBoardLine(self.board.get_board(), row)
        available_values = self.board.get_available_values().copy()
        number_sequences = sequencesCopy(self.board.get_number_sequences())
        sequences_sizes = self.board.get_sequences_sizes().copy()
        lowest_sequence_index = self.board.get_lowest_sequence_index()
        lowest_sequence_value = self.board.get_lowest_sequence_value()
        next_sequence_index = self.board.get_next_sequence_index()
        next_sequence_value = self.board.get_next_sequence_value()
        direction = self.board.get_direction()
        number_of_blank_positions = self.board.get_number_of_blank_positions()

        if (not self.board.is_blank_position(row, col)):
            return None

        board_representation[row][col] = value
        available_values[value - 1] = False
        number_of_blank_positions -= 1

        board = Board(board_representation, available_values, number_sequences, sequences_sizes, lowest_sequence_index, lowest_sequence_value, next_sequence_index, next_sequence_value, direction, number_of_blank_positions)
        board.merge_sequences_action(action)

        return board

    def get_board(self):
        return self.board



class Board:
    """ Representação interna de um tabuleiro de Numbrix. """
    num_cells = None
    size = None

    def __init__(self, board, available_values, number_sequences, sequences_sizes, lowest_sequence_index, lowest_sequence_value, next_sequence_index, next_sequence_value, direction, number_of_blank_positions) -> None:
        # board representation
        self.board = board
        self.available_values = available_values

        # number sequences
        self.number_sequences = number_sequences
        self.sequences_sizes = sequences_sizes
        self.lowest_sequence_index = lowest_sequence_index
        self.lowest_sequence_value = lowest_sequence_value

        self.next_sequence_index = next_sequence_index
        self.next_sequence_value = next_sequence_value

        self.direction = direction

        # TODO : se isto não for usado para nada remover
        self.number_of_blank_positions = number_of_blank_positions

    def __repr__(self) -> str:
        board_string = ""
        for row in range(Board.size):
            for col in range(Board.size):
                element = self.get_number(row, col)
                board_string += f"{element}\t"

            board_string_size = len(board_string)
            board_string = board_string[:board_string_size - 1] + "\n"
        return board_string
            

    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """
        if (not (0 <= row <= Board.size - 1)) or (not (0 <= col <= Board.size - 1)):
            return None

        return self.board[row][col]
    
    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """
        
        return (self.get_number(row + 1, col), self.get_number(row - 1, col))
        
    
    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """
        
        return (self.get_number(row , col - 1), self.get_number(row , col + 1))
    
    def get_adjacencies(self, row , col):
        relative_positions = [[0, 1], [0, -1], [-1, 0], [1,0]]
        adjacencies = []
        
        for pos in relative_positions:
            new_row, new_col = pos[ROW] + row, pos[COL] + col

            if(self.get_number(new_row, new_col) != None):
                adjacencies.append((new_row, new_col))

        return adjacencies

    def get_blank_adjacencies(self, row, col):
        relative_positions = [[0, 1], [0, -1], [-1, 0], [1,0]]
        adjacencies = []
        
        for pos in relative_positions:
            new_row, new_col = pos[ROW] + row, pos[COL] + col

            if(self.get_number(new_row, new_col) == 0):
                adjacencies.append((new_row, new_col))

        return adjacencies

    def check_adjacencies(self, row, col, relative_value):
        adjacencies = self.get_adjacencies(row, col)
        value = self.get_number(row, col) + relative_value

        for adjacency in adjacencies:
            if(self.get_number(adjacency[ROW], adjacency[COL]) == value):
                return adjacency
        
        return None

    
    @staticmethod    
    def parse_instance(filename: str):
        """ Lê o ficheiro cujo caminho é passado como argumento e retorna
        uma instância da classe Board. """
        
        size = None
        board_representation = []
        available_values = []
        number_sequences = []
        number_of_blank_positions = 0

        with open(filename) as file:
            # set board size
            size = int(file.readline())
            Board.num_cells = size ** 2
            Board.size = size
            available_values = [True for i in range(Board.num_cells)]
                
            # construct board internal representation
            lines = file.readlines()

            i, j = (0, 0)
            for line in lines:
                board_line = []
                for element in line.split("\t"):
                    element = int(element)
                    board_line.append(element)

                    # check if the element is a blank space
                    if element != 0:
                        available_values[element - 1] = False
                        number_sequences.append([(i, j)])
                    else:
                        number_of_blank_positions += 1

                    j = (j + 1) % size
                i = (i + 1) % size      

                board_representation.append(board_line)

        # fill number sequences
        sequences_sizes = [1 for i in range(Board.num_cells)]
        board = Board(board_representation, available_values, number_sequences, sequences_sizes, None, None, None, None, 1, number_of_blank_positions)

        board.calculate_paths()

        return board
    
    def get_board(self):
        return self.board

    def get_number_sequences(self):
        return self.number_sequences

    def get_sequences_sizes(self):
        return self.sequences_sizes

    def get_number_of_blank_positions(self):
        return self.number_of_blank_positions

    def get_lowest_sequence_index (self):
        return self.lowest_sequence_index

    def get_lowest_sequence_value (self):
        return self.lowest_sequence_value

    def get_next_sequence_index (self):
        return self.next_sequence_index

    def get_next_sequence_value (self):
        return self.next_sequence_value

    def get_direction (self):
        return self.direction

    def get_lowest_sequence_info (self):
        reference = 0
        if self.direction == 1:
            reference = -1

        position = self.number_sequences[self.lowest_sequence_index][reference]
        return (position, self.lowest_sequence_value)

    def get_next_sequence_info (self):
        reference = -1
        if self.direction == 1:
            reference = 0

        if (self.next_sequence_index == None):
            return (None, self.lowest_sequence_value)

        position = self.number_sequences[self.next_sequence_index][reference]
        return (position, self.next_sequence_value)

    def is_blank_position(self, row, col):
        value = self.get_number(row, col)
        return value == 0

    def get_available_values(self):
        return self.available_values

    def is_adjency (self, x, y):
        return abs(x[ROW] - y[ROW]) + abs(x[COL] - y[COL]) == 1

    def is_successor (self, x, y):    
            row_x, col_x = x
            row_y, col_y = y 

            value_x = self.get_number(row_x, col_x)
            value_y = self.get_number(row_y, col_y)

            return value_x != 0 and value_y != 0 and abs(value_x - value_y) == 1


    def merge_sequences_action(self, action):

        def get_sequence(position):
            row, col = position
            for i in range(len(self.number_sequences)):
                if (row, col) == self.number_sequences[i][0]:
                    return (0, i)

                if (row, col) == self.number_sequences[i][-1]:
                    return (-1, i)

            return None
        
        row, col, value = action
        self.number_sequences.append([(row, col)])

        position, index = (0, len(self.number_sequences) - 1)

        # join to the smallest sequence
        lowest_position = 0
        next_position = -1
        if self.direction == 1:
            lowest_position = -1
            next_position = 0

        if (self.next_sequence_index != None):
            next = self.number_sequences[self.next_sequence_index][next_position]

        self.merge_sequences(index, self.lowest_sequence_index, position, lowest_position)

        self.lowest_sequence_value += self.direction
        self.lowest_sequence_index = len(self.number_sequences) - 1
        
        if (self.next_sequence_index != None):
            next_position, next_index = get_sequence(next)
            self.next_sequence_index = next_index
        
        # check if it can join to the next sequence
        if self.next_sequence_index != None and self.is_adjency(next, (row, col)) and self.is_successor(next, (row, col)):
            self.merge_sequences(next_index, self.lowest_sequence_index, next_position, lowest_position)
            self.lowest_sequence_index = len(self.number_sequences) - 1
            
            new_row, new_col = self.number_sequences[self.lowest_sequence_index][lowest_position]
            self.lowest_sequence_value = self.get_number(new_row, new_col)

            self.update_next_sequence()

        # change direction if the biggest value in the lowest
        # sequence is the biggest value that we can put on the board
        if (self.direction == 1 and self.lowest_sequence_value == Board.num_cells):
            self.direction = -1
            row, col = self.number_sequences[self.lowest_sequence_index][0]
            self.lowest_sequence_value = self.get_number(row, col)
            self.update_next_sequence()


    def update_next_sequence(self):
        
        # TODO : fazer update_next_sequence abstrato => não importa a direção
        # esta implementação assume que estamos a andar para a frente

        next_value = -1
        if (self.direction == 1):
            next_value = Board.num_cells + 1

        next_index = None
        for i in range(len(self.number_sequences)):
            if (i != self.lowest_sequence_index):
                row, col = self.number_sequences[i][0]
                value = self.get_number(row, col)
                # TODO : isto da para fazer em apenas 1 if 
                if (self.direction == 1 and value < next_value):
                    next_value = value
                    next_index = i
                elif (self.direction == -1 and value > next_value):
                    next_value = value
                    next_index = i

        if (next_index == None):
            # TODO : now im assuming that direction == 1
            # => there is no next sequence
            self.next_sequence_value = next_value
            self.next_sequence_index = None
            return

        self.next_sequence_index = next_index
        self.next_sequence_value = next_value

    def merge_sequences(self, index_i, index_j, position_i, position_j):
        sequence_i = self.number_sequences[index_i]
        sequence_j = self.number_sequences[index_j]

        if (len(sequence_i) == 1 or len(sequence_j) == 1):
            if (self.get_number(sequence_i[position_i][ROW], sequence_i[position_i][COL]) < self.get_number(sequence_j[position_j][ROW], sequence_j[position_j][COL])):
                position_i = -1
                position_j = 0
            else:
                position_i = 0
                position_j = -1

        new_sequence = [0, 0]
        new_sequence[position_i] = sequence_j[position_i]
        new_sequence[position_j] = sequence_i[position_j]

        max_index = max(index_i, index_j)
        min_index = min(index_i, index_j)
        self.number_sequences.pop(max_index)
        self.number_sequences.pop(min_index)
        self.number_sequences.append(new_sequence)

        new_sequence_size = self.sequences_sizes.pop(max_index) + self.sequences_sizes.pop(min_index)
        self.sequences_sizes.append(new_sequence_size)

    def calculate_paths(self):      

        def merge_sequence():
            i, j = (0, 0)
            while (i < len(self.number_sequences)):
                for j in range(len(self.number_sequences)):
                    if (i != j):
                        sequence_i = self.number_sequences[i]
                        sequence_j = self.number_sequences[j]

                        # check if can merge fist element 
                        # of i with last element of j
                        if (self.is_adjency(sequence_i[0], sequence_j[-1]) and self.is_successor(sequence_i[0], sequence_j[-1])):
                            self.merge_sequences(i, j, 0, -1)
                            return True
                        
                        # check if can merge fist element 
                        # of j with last element of i
                        if (self.is_adjency(sequence_j[0], sequence_i[-1]) and self.is_successor(sequence_j[0], sequence_i[-1])):
                            self.merge_sequences(i, j, -1, 0)
                            return True
                i += 1
            
            return False
        
        while merge_sequence():
            pass
        
        self.lowest_sequence_value = Board.num_cells + 1
        self.lowest_sequence_index = None
        for i in range(len(self.number_sequences)):
            sequence = self.number_sequences[i]
            row, col = sequence[-1]
            value = self.get_number(row, col)
            if self.lowest_sequence_value > value:
                self.lowest_sequence_value = value
                self.lowest_sequence_index = i

        self.update_next_sequence()



class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        super().__init__(NumbrixState(board))

    def path_between(self, board, start_node, goal_node, depth):
        def dfs(visited, node, depth):
            row , col = node
            dist = abs(row - start_node[ROW]) + abs(col - start_node[COL])

            if (node not in visited) and (dist < depth):
                visited.append(node)

                if (dist + 1 == depth) and board.is_adjency(node, goal_node):
                    return True

                for adjacency in board.get_blank_adjacencies(row, col):
                    if (dfs(visited, adjacency, depth)):
                        return True
            
            return False
            
        return dfs([], start_node, depth)
 
    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        actions = []
        
        board = state.get_board()
        lowest_position, lowest_value = board.get_lowest_sequence_info()
        next_position, next_value = board.get_next_sequence_info()
        direction = board.get_direction()


        # TODO : alterar de forma a que seja dinamico com a mudança de direção
        if (direction == 1 and board.get_lowest_sequence_value() >= board.get_next_sequence_value() - 1):
            return []
        
        if (direction == -1 and board.get_lowest_sequence_value() <= board.get_next_sequence_value() + 1):
            return []

        lowest_row, lowest_col = lowest_position
        adjacencies = state.get_board().get_blank_adjacencies(lowest_row, lowest_col)

        if (next_position != None):
            next_row, next_col = next_position
        
        radius = abs(next_value - (lowest_value + direction))

        for adjency in adjacencies:
            adj_row, adj_col = adjency
            
            if (next_position == None) or (abs(next_row - adj_row) + abs(next_col - adj_col) <= radius):
                actions.append((adj_row, adj_col, lowest_value + direction))

        if (len(actions) == 1 or next_position == None):
            return actions
        
        # if there is more than one possible action check if all of the actions
        # can reach the next_sequence by a blank path
        for i in range(len(actions) - 1, -1, -1):    
            row, col, _ = actions[i]
            position = (row, col)
            
            has_path_between = self.path_between(board, position, next_position, radius)
            if (not has_path_between):
                actions.pop(i)

        return actions

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        
        new_board = state.apply_action(action)
        new_state = NumbrixState(new_board)
        return new_state

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """
        
        board = state.get_board()
        if (board.get_number_of_blank_positions() != 0):
            return False

        return len(board.get_number_sequences()) == 1

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        
        # TODO : dont just consider the biggest sequence but all sequences
        pass        


def main():
    input_file = sys.argv[1]
    board = Board.parse_instance(input_file)
    
    # Usar uma técnica de procura para resolver a instância,
    problem = Numbrix(board)

    # Retirar a solução a partir do nó resultante,
    goal_node = depth_first_tree_search(problem)

    # Imprimir para o standard output no formato indicado.
    print(goal_node.state.board, end="")

if __name__ == "__main__":
    main()
    