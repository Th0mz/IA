# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 67:
# 95599 Joao Ramalho
# 95680 Tomas Tavares

from hashlib import new
from logging.handlers import BaseRotatingHandler
import sys
from tkinter import N
from turtle import pos

from setuptools import sic
from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search


ROW = 0
COL = 1
VALUE = 2

class NumbrixState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = NumbrixState.state_id
        NumbrixState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    def get_blank_positions(self):
        positions = [(i, j) for i in range(self.board.get_size()) for j in range(self.board.get_size())]
        
        return list(filter(lambda position: self.board.is_blank_position(position[ROW], position[COL]),
                positions))

    def get_value_possibilities(self, row, col):
        return range(1, (self.board.size)**2 + 1)

    def apply_action(self, action):
        self.board.put_value(action[ROW], action[COL], action[VALUE])
        return Board(self.board.get_representation(), self.board.get_size())

    def get_board(self):
        return self.board

class Board:
    """ Representação interna de um tabuleiro de Numbrix. """

    def __init__(self, representation, size) -> None:
        self.representation = representation
        self.size = size

    def __repr__(self) -> str:
        board_representation = ""
        for representation_line in self.representation:
            for element in representation_line:
                board_representation += f"{element} "

            board_representation += "\n"
        return board_representation
            

    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """
        if (not (0 <= row <= self.size - 1)) or (not (0 <= col <= self.size - 1)):
            return None

        return self.representation[col][row]
    
    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """
        
        return (self.get_number(row + 1, col), self.get_number(row - 1, col))
        
    
    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """
        
        return (self.get_number(row , col - 1), self.get_number(row , col + 1))
    
    def check_adjacencies(self, row, col, relative_value):
        relative_positions = [[0, 1], [0, -1], [-1, 0], [1,0]]
        value = self.get_number(row,col) + relative_value

        for pos in relative_positions:
            new_row, new_col = pos[0] + row, pos[1] + col

            if(self.get_number(new_row, new_col) == value):
                return (new_row, new_col)
        
        return None

    
    @staticmethod    
    def parse_instance(filename: str):
        """ Lê o ficheiro cujo caminho é passado como argumento e retorna
        uma instância da classe Board. """
        
        size = None
        representation = []

        with open(input_file) as file:
            # set board size
            size = int(file.readline())
            
            # construct board internal representation
            lines = file.readlines()
            for line in lines:
                representation_line = []
                for element in line.split("\t"):
                    representation_line.append(int(element))

                representation.append(representation_line)
        
        return Board(representation, size)
    
    def get_representation(self):
        return self.representation

    def get_size(self):
        return self.size

    def put_value(self, row, col, value):
        if (not self.is_blank_position(row, col)):
            return 

        self.representation[col][row] = value

    def is_blank_position(self, row, col):
        value = self.get_number(row, col)
        return value == 0


class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        super().__init__(NumbrixState(board))
 
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
        new_state = NumbrixState(new_board)
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
        # TODO
        pass
    
    # TODO: outros metodos da classe


if __name__ == "__main__":
    # Ler o ficheiro de input de sys.argv[1],
    if (len(sys.argv) != 2):
        print("Invalid command expected : python numbrix.py <input_file_path>")
        exit()

    input_file = sys.argv[1]
    board = Board.parse_instance(input_file)
    
    numbrix = Numbrix(board)
    print(numbrix.goal_test(numbrix.initial))
    # Usar uma técnica de procura para resolver a instância,
    
    # Retirar a solução a partir do nó resultante,

    # Imprimir para o standard output no formato indicado.
