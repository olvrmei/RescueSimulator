from maze import Maze
from state import State
from cardinal import *


class Problem:
    """Representação de um problema a ser resolvido por um algoritmo de busca clássica.
    A formulação do problema - instância desta classe - reside na 'mente' do agente."""


    def __init__(self):
        self.initialState = State(0,0)
        self.goalState = State(0,0)

    def createMaze(self, maxRows, maxColumns, maze = False):
        """Este método instancia um labirinto - representa o que o agente crê ser o labirinto.
        As paredes devem ser colocadas fora desta classe porque este.
        @param maxRows: máximo de linhas do labirinto.
        @param maxColumns: máximo de colunas do labirinto."""
        self.mazeBelief = maze
        self.maxRows = maxRows
        self.maxColumns = maxColumns
        self.cost = [[0.0 for j in range(maxRows*maxColumns)]for i in range(8)]

    def defInitialState(self, row, col):
        """Define o estado inicial.
        @param row: linha do estado inicial.
        @param col: coluna do estado inicial."""
        self.initialState.row = row
        self.initialState.col = col

    def getInitialState(self):
        """Retorna o estado inicial.
        @return estado inicial."""
        return self.initialState

    def getMaxRows(self):
        return self.maxRows

    def getMaxColumns(self):
        return self.maxColumns
        
    def defGoalState(self, row, col):
        """Define o estado objetivo.
        @param row: linha do estado objetivo.
        @param col: coluna do estado objetivo."""
        self.goalState.row = row
        self.goalState.col = col

    def getActionCost(self, action):
        """Retorna o custo da ação.
        @param action:
        @return custo da ação"""
        if action == "victim":
            return 2

        if (action=="nop"):
            return 0

        if (action == "N" or action == "L" or action == "O" or action == "S"):   
            return 1.0
        
        return 1.5

    def goalTest(self, currentState):
        """Testa se alcançou o estado objetivo.
        @param currentState: estado atual.
        @return True se o estado atual for igual ao estado objetivo."""
        if currentState == self.goalState:
            return True
        else:
            return False


