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
from turtle import position

from setuptools import sic
from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search


class NumbrixState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = NumbrixState.state_id
        NumbrixState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id
        
    # TODO: outros metodos da classe


class Board:
    """ Representação interna de um tabuleiro de Numbrix. """

    def __init__(self, representation, size) -> None:
        self.representation = representation
        self.size = size

    def get_representation(self):
        return self.representation
        
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

    # TODO: outros metodos da classe


class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        super().__init__(NumbrixState(board.get_representation()))

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        # TODO
        pass

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        # TODO
        pass

  def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """
        # TODO
        pass  

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

    # Usar uma técnica de procura para resolver a instância,
    
    # Retirar a solução a partir do nó resultante,

    # Imprimir para o standard output no formato indicado.
