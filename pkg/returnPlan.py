from turtle import position
from state import State
import math
import copy

class ReturnPlan:

    def __init__(self, problem, initialState, name = "retornaParaBase"):

        # inicializa variáveis
        self.problem = problem
        self.initialState = initialState
        self.currentState = initialState
        self.goalState = problem.getInitialState()
        self.name = name

        # inicializa heurísticas
        self.openList = [(self.initialState.row, self.initialState.col)]
        self.lastCoordinate = dict()
        # g(n) -> custo para chegar a n
        self.gHeuristic = dict()
        # f(n) = h(n) + g(n) -> custo estimado para chegar no objetivo passando por n
        self.fHeuristic = dict()

        # custo inicial para chegar em qualquer nó é inifinito, exceto para o nó inicial que é 0
        for i in range(0,self.problem.getMaxRows()):
            for j in range(0,self.problem.getMaxColumns()):
                self.gHeuristic[(i,j)] = math.inf
                self.fHeuristic[(i,j)] = math.inf
        self.gHeuristic[(self.initialState.row, self.initialState.col)] = 0
        
        self.path = self.calculatePath()
        self.totalCost = self.calculateCost()

    def calculateHeuristics(self, currentState):
        # Calcula as heurísticas(h(n)) do estado atual -> distância de Manhattan = |x1-x2| + |y1-y2|
        if self.goalState and currentState:
            return abs(currentState.row - self.goalState.row) + abs(currentState.col - self.goalState.col)

    def getLowestF(self):
        # Retorna o nó com menor f(n) da lista aberta
        lowestF = math.inf
        lowestFNode = None
        for node in self.openList:
            if self.fHeuristic[node] < lowestF:
                lowestF = self.fHeuristic[node]
                lowestFNode = node
        return lowestFNode

    def reconstructPath(self, currentState):
        # Reconstroi o caminho percorrido até o estado atual
        path = []
        while currentState in self.lastCoordinate.keys():
            path.append(currentState)
            currentState = self.lastCoordinate[currentState]
        path = path.reversed()
        path.pop(0) # remove o estado inicial
        return path

    def updateCurrentState(self, newState):
        self.currentState = newState

    def calculatePath(self):
        while len(self.openList) > 0:
            # pega o nó com menor f(n) da lista aberta
            currentNode = self.getLowestF()

            # se o nó atual é o objetivo, retorna o caminho
            if currentNode == (self.goalState.row, self.goalState.col):
                return self.reconstructPath(currentNode)

            # remove o nó atual da lista aberta
            self.openList.remove(currentNode)

            rowIterator = [-1, -1, -1,  0, 0,  1, 1, 1]
            colIterator = [-1,  0,  1, -1, 1, -1, 0, 1]

            for i in range(0, len(rowIterator)):
                neighbor = (currentNode[0] - rowIterator[i], currentNode[1] - colIterator[i])
                
                if self.isCoordinateValid(neighbor):
                    tentativeG = self.gHeuristic[currentNode] + self.neighborNodeCost(currentNode, neighbor, (rowIterator[i], colIterator[i]))

                    if tentativeG < self.gHeuristic[neighbor]:
                        self.lastCoordinate[neighbor] = currentNode
                        self.gHeuristic[neighbor] = tentativeG
                        self.fHeuristic[neighbor] = tentativeG + self.calculateHeuristics(neighbor)
                        if neighbor not in self.openList:
                            self.openList.append(neighbor)
        return []

    def calculateCost(self):
        if len(self.path) > 0:
            if (self.initialState.row - self.path[0][0]) != 0 and (self.initialState.col - self.path[0][1]) != 0:
                cost = 1.5
            else: 
                cost = 1
            for i in range(0, len(self.path) - 1):
                if (self.path[i+1][0] - self.path[i][0]) == 0 or (self.path[i+1][1] - self.path[i][1]) == 0:
                    cost += 1
                else:
                    cost += 1.5
            return cost
        return 0

    def getNextPosition(self):
        # Retorna a próxima posição do caminho
        if len(self.path) > 0:
            movePos = self.path.pop(0)
        else:
            return "nop", self.currentState

        moveDirection = {
            "N": (-1, 0),
            "S": (1, 0),
            "L": (0, 1),
            "O": (0, -1),
            "NO": (-1, -1),
            "NE": (-1, 1),
            "SE": (1, 1),
            "SO": (1, -1)
        }

        delta = (movePos[0] - self.currentState.row, movePos[1] - self.currentState.col)
        action = list(moveDirection.keys())[list(moveDirection.values()).index(delta)]
        return action, State(movePos[0], movePos[1])

    def chooseAction(self):
        return self.getNextPosition()

    def getPlanCost(self):
        return self.totalCost

# TODO: Verificar se ta certo
    def neighborNodeCost(self, currentState, neighborNode, offset):
        # Calcula o custo para chegar no nó vizinho
        isPossibleToMove = self.isPossibleToMove(neighborNode)
        if not isPossibleToMove:
            return math.inf

        # não tem paredes no lugar e não está indo na diagonal
        if offset[0] == 0 or offset[1] == 0:
            return 1
        
        # se está indo na diagonal, não pode se mover ou obstaculos no caminho
        isPossibleToMove = self.isPossibleToMove((currentState.row - offset[0], currentState.col)) and self.isPossibleToMove((currentState.row, currentState.col - offset[1]))

        if not isPossibleToMove:
            return math.inf

        return 1.5

# TODO: Verificar se ta certo
    def isCoordinateValid(self, position):
        return position.row >= 0 and position.row < self.problem.getMaxRows() and position.col >= 0 and position.col < self.problem.getMaxColumns()

# TODO: Verificar se ta certo
    def isPossibleToMove(self, position):
        return self.problem.mazeBelief[position.row][position.col] >= 0 and self.isCoordinateValid(position)


