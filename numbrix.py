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


class NumbrixState:
    state_id = 0

    def __init__(self, board, last_action):
        self.board = board
        self.last_action = last_action
        self.id = NumbrixState.state_id
        NumbrixState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    def get_blank_positions(self):
        positions = [(i, j) for i in range(self.board.get_size()) for j in range(self.board.get_size())]
        
        return list(filter(lambda position: self.board.is_blank_position(position[ROW], position[COL]),
                positions))

    def number_blank_positions (self):
        blank_positions = 0
        for is_available in self.board.get_available_values():
            if is_available:
                blank_positions += 1

        return blank_positions

    def get_value_possibilities(self, row, col):
        return self.board.get_possible_values(row, col)

    def apply_action(self, action):
        row, col, value = action
        board = self.board.get_representation().copy()
        available_values = self.board.get_available_values().copy()
        number_sequences = sequencesCopy(self.board.get_number_sequences())
        sequences_sizes = self.board.get_sequences_sizes().copy()
        number_of_blank_positions = self.board.get_number_of_blank_positions()

        if (not self.board.is_blank_position(row, col)):
            return None

        board[row * self.board.size + col] = value
        available_values[value - 1] = False
        number_of_blank_positions -= 1

        board = Board(board, self.board.get_size(), available_values, number_sequences, sequences_sizes, number_of_blank_positions)
        board.merge_sequences_action(action)

        return board 

    def get_board(self):
        return self.board

    def get_last_action(self):
        return self.last_action

class Board:
    """ Representação interna de um tabuleiro de Numbrix. """
    num_cells = None

    def __init__(self, representation, size, available_values, number_sequences, sequences_sizes, number_of_blank_positions) -> None:
        self.representation = representation
        self.size = size
        self.available_values = available_values
        self.number_sequences = number_sequences
        self.sequences_sizes = sequences_sizes
        self.number_of_blank_positions = number_of_blank_positions

    def __repr__(self) -> str:
        board_representation = ""
        for row in range(self.size):
            for col in range(self.size):
                element = self.get_number(row, col)
                board_representation += f"{element}\t"

            board_representation_size = len(board_representation)
            board_representation = board_representation[:board_representation_size - 1] + "\n"
        return board_representation
            

    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """
        if (not (0 <= row <= self.size - 1)) or (not (0 <= col <= self.size - 1)):
            return None

        return self.representation[row * self.size + col]
    
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

    def check_adjacencies(self, row, col, relative_value):
        adjacencies = self.get_adjacencies(row, col)
        value = self.get_number(row,col) + relative_value

        for adjacency in adjacencies:

            if(self.get_number(adjacency[ROW], adjacency[COL]) == value):
                return adjacency
        
        return None

    
    @staticmethod    
    def parse_instance(filename: str):
        """ Lê o ficheiro cujo caminho é passado como argumento e retorna
        uma instância da classe Board. """
        
        size = None
        representation = []
        available_values = []
        number_sequences = []
        number_of_blank_positions = 0

        with open(filename) as file:
            # set board size
            size = int(file.readline())
            Board.num_cells = size ** 2
            available_values = [True for i in range(Board.num_cells)]
                
            # construct board internal representation
            lines = file.readlines()
            for line in lines:
                for element in line.split("\t"):
                    element = int(element)
                    representation.append(element)

                    # check if the element is a blank space
                    if element != 0:
                        available_values[element - 1] = False
                    else:
                        number_of_blank_positions += 1

        # fill number sequences
        number_sequences = [[(row, col)] for row in range(size) for col in range(size)]
        sequences_sizes = [1 for i in range(Board.num_cells)]
        board = Board(representation, size, available_values, number_sequences, sequences_sizes, number_of_blank_positions)

        board.calculate_paths()
        
        return board
    
    def get_representation(self):
        return self.representation

    def get_number_sequences(self):
        return self.number_sequences

    def get_sequences_sizes(self):
        return self.sequences_sizes

    def get_size(self):
        return self.size

    def get_number_of_blank_positions(self):
        return self.number_of_blank_positions

    def is_blank_position(self, row, col):
        value = self.get_number(row, col)
        return value == 0

    def is_available_value(self, value):
        if not (1 <= value <= Board.num_cells):
            return False

        return self.available_values[value - 1]

    def get_possible_values(self, row, col):

        def get_number_position (number):
            for i in range(len(self.representation)):
                if self.representation[i] == number:
                    return (i // self.size, i % self.size)

            return None

        def is_in_sequence_range(row, col, number):
            radius = 1
            adj_number = None
            if (not self.is_available_value(number - radius) and number - radius >= 1):
                 adj_number = number - radius 
            elif (not self.is_available_value(number + radius) and number + radius <= Board.num_cells):
                adj_number = number + radius
            else:
                return False

            adj_position = get_number_position(adj_number)
            adj_row, adj_col = adj_position

            # manhattan distance must be smaller than the difference bettween the
            # 2 adjacent values in order to be able to connect the 2 values
            return radius == 1 and abs(row - adj_row) + abs(col - adj_col) <= radius

        possible_values = []
        for number in range(1, Board.num_cells + 1):
            if (self.is_available_value(number) and is_in_sequence_range(row, col, number)):
                possible_values.append(number)

        return possible_values

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
        position, index = get_sequence((row, col))
        
        adjacencies = self.get_adjacencies(row, col)
        for adjency in adjacencies:
            if (self.is_successor((row, col), adjency)):
                adj_sequence_info = get_sequence(adjency)
                if (adj_sequence_info != None):
                    adj_position, adj_index = adj_sequence_info
                    self.merge_sequences(index, adj_index, position, adj_position)

                    sequence_info = get_sequence((row, col))
                    if (sequence_info == None):
                        return

                    position, index = sequence_info


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





class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        super().__init__(NumbrixState(board, None))
 
    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        actions = []
        for blank_position in state.get_blank_positions():
            row, col = blank_position
            for number in state.get_value_possibilities(row, col):
                actions.append(blank_position + (number,))
        
        return actions

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        
        if (action not in self.actions(state)):
            # TODO : refactor this exception
            raise Exception

        new_board = state.apply_action(action)
        new_state = NumbrixState(new_board, action)
        return new_state

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """
        
        #predecessor
        #sucesor
        if(state.get_board().get_number(0, 0) == 1):
            successor_coord = state.get_board().check_adjacencies(0, 0, 1)
            
            if successor_coord == None:
                return False
            
            successor = state.get_board().get_number(successor_coord[ROW], successor_coord[COL])
            predecessor = 1
        elif(state.get_board().get_number(0,0) == Board.num_cells):
            predecessor_coord = state.get_board().check_adjacencies(0, 0, -1)
            
            if predecessor_coord == None:
                return False
            
            predecessor = state.get_board().get_number(predecessor_coord[ROW], predecessor_coord[COL])
            successor = Board.num_cells
        else:
            predecessor_coord = state.get_board().check_adjacencies(0, 0, -1)
            successor_coord = state.get_board().check_adjacencies(0, 0, 1)

            if (predecessor_coord == None or successor_coord == None):
                return False

            predecessor = state.get_board().get_number(predecessor_coord[ROW], predecessor_coord[COL])
            successor = state.get_board().get_number(successor_coord[ROW], successor_coord[COL])
        
        while predecessor > 1:
            predecessor_coord = state.get_board().check_adjacencies(predecessor_coord[ROW], predecessor_coord[COL], -1)

            if(predecessor_coord == None):
                return False
            
            predecessor = state.get_board().get_number(predecessor_coord[0], predecessor_coord[1])

        while successor < (Board.num_cells):
            successor_coord = state.get_board().check_adjacencies(successor_coord[ROW], successor_coord[COL], 1)

            if(successor_coord == None):
                return False
            
            successor = state.get_board().get_number(successor_coord[0], successor_coord[1])

        return True

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        
        # TODO : dont just consider the biggest sequence but all sequences
        state = node.state
        sequences_sizes = state.get_board().get_sequences_sizes()

        cells_in_sequence = 0
        for sequence_size in sequences_sizes:
            if sequence_size > 1:
                cells_in_sequence += sequence_size

        scaling_factor = 1 - 1 / (1 + state.number_blank_positions())
        return ((2 * Board.num_cells) - cells_in_sequence - max(sequences_sizes)) * scaling_factor


def main():
    input_file = sys.argv[1]
    board = Board.parse_instance(input_file)
    
    # Usar uma técnica de procura para resolver a instância,
    problem = Numbrix(board)

    # Retirar a solução a partir do nó resultante,
    goal_node = depth_first_tree_search(problem)

    # Imprimir para o standard output no formato indicado.
    if (goal_node == None):
        raise Exception

    print(goal_node.state.board, end="")

if __name__ == "__main__":
    main()
    