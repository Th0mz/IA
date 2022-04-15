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

def arrayCopy (array):
    new_array = []
    for value in array:
        new_array.append(value)

    return new_array


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

    def get_value_possibilities(self, row, col):
        return self.board.get_possible_values(row, col)

    def apply_action(self, action):
        row, col, value = action
        board = arrayCopy(self.board.get_representation())
        available_values = arrayCopy(self.board.get_available_values())
        number_sequences = arrayCopy(self.board.get_number_sequences())

        if (not self.board.is_blank_position(row, col)):
            return None

        board[row * self.board.size + col] = value
        available_values[value - 1] = False

        # check if the added value is in a sequence that already exists
        for i in range(len(number_sequences)):
            sequence_start = number_sequences[i][0]
            if (self.is_adjency((row, col), sequence_start) and True):
                number_sequences[i] = [(row, col)] + number_sequences[i]
                # TODO
                return Board(board, self.board.get_size(), available_values, number_sequences)

            sequence_end = number_sequences[i][-1]
            if (self.is_adjency((row, col), sequence_end) and True):
                number_sequences[i] = number_sequences[i] + [(row, col)]
                # TODO
                return Board(board, self.board.get_size(), available_values, number_sequences)


        # check if it forms a new sequence

        # create that sequence

        return Board(board, self.board.get_size(), available_values, number_sequences)      

    def is_adjency (x, y):
        return abs(x[ROW] - y[ROW]) + abs(x[COL] + y[COL]) == 1 

    def get_board(self):
        return self.board

    def get_last_action(self):
        return self.last_action

class Board:
    """ Representação interna de um tabuleiro de Numbrix. """

    def __init__(self, representation, size, available_values, number_sequences) -> None:
        self.representation = representation
        self.size = size
        self.available_values = available_values
        self.number_sequences = number_sequences

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

        with open(filename) as file:
            # set board size
            size = int(file.readline())

            available_values = [True for i in range(size**2)]
                
            # construct board internal representation
            lines = file.readlines()
            for line in lines:
                for element in line.split("\t"):
                    element = int(element)
                    representation.append(element)

                    # check if the element is a blank space
                    if element != 0:
                        available_values[element - 1] = False

            # fill number sequences
        
        return Board(representation, size, available_values, number_sequences)
    
    def get_representation(self):
        return self.representation

    def get_number_sequences(self):
        return self.number_sequences

    def get_size(self):
        return self.size

    def is_blank_position(self, row, col):
        value = self.get_number(row, col)
        return value == 0

    def get_possible_values(self, row, col):

        # check if the blank square is surrounded by 
        # 2 consecutive values on the vertical
        vertical_adjacent = self.adjacent_vertical_numbers(row, col)
        if ((vertical_adjacent[0] and vertical_adjacent[1]) and (abs(vertical_adjacent[0] - vertical_adjacent[1]) == 2)):
            value = min(vertical_adjacent[0], vertical_adjacent[1]) + 1
            if (self.is_available_value(value)):
                return [value]
            
            return []
        
        # check if the blank square is surrounded by 
        # 2 consecutive values on the horizontal
        horizontal_adjacent = self.adjacent_horizontal_numbers(row, col)
        if ((horizontal_adjacent[0] and horizontal_adjacent[1]) and (abs(horizontal_adjacent[0] - horizontal_adjacent[1]) == 2)):
            value = min(horizontal_adjacent[0], horizontal_adjacent[1]) + 1
            if (self.is_available_value(value)):
                return [value]
            
            return []

        possible_values = []
        for number in range(1, self.size**2 + 1):
            if (self.is_available_value(number)):
                possible_values.append(number)

        return possible_values

    def get_available_values(self):
        return self.available_values

    def is_available_value(self, value):
        if not (1 <= value <= self.size**2):
            return False

        return self.available_values[value - 1]


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
        elif(state.get_board().get_number(0,0) == state.get_board().get_size()**2):
            predecessor_coord = state.get_board().check_adjacencies(0, 0, -1)
            
            if predecessor_coord == None:
                return False
            
            predecessor = state.get_board().get_number(predecessor_coord[ROW], predecessor_coord[COL])
            successor = state.get_board().get_size()**2
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

        while successor < (state.get_board().get_size()**2):
            successor_coord = state.get_board().check_adjacencies(successor_coord[ROW], successor_coord[COL], 1)

            if(successor_coord == None):
                return False
            
            successor = state.get_board().get_number(successor_coord[0], successor_coord[1])

        return True

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        
        state = node.state
        sequences = state.get_board().get_number_sequences()
        biggest_sequence = 0
        for sequence in sequences:
            sequence_len = len(sequence)
            if sequence_len > biggest_sequence:
                biggest_sequence = sequence_len

        num_cells = state.get_board().get_size() ** 2
        return num_cells - biggest_sequence

def main():
    # Ler o ficheiro de input de sys.argv[1],
    if (len(sys.argv) != 2):
        print("Invalid command expected : python numbrix.py <input_file_path>")
        exit()

    input_file = sys.argv[1]
    board = Board.parse_instance(input_file)
    
    # Usar uma técnica de procura para resolver a instância,
    problem = Numbrix(board)

    # Retirar a solução a partir do nó resultante,
    goal_node = astar_search(problem)

    # Imprimir para o standard output no formato indicado.
    print(goal_node.state.board, end="")


if __name__ == "__main__":
    # DEBUG : 
    import cProfile
    cProfile.run('main()', "output.dat")

    import pstats
    from pstats import SortKey

    with open('time.txt', 'w') as f:
        p = pstats.Stats("output.dat", stream=f)
        p.sort_stats("time").print_stats()

    with open('calls.txt', 'w') as f:
        p = pstats.Stats("output.dat", stream=f)
        p.sort_stats("calls").print_stats()

    