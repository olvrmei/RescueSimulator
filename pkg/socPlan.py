from random import randint
from state import State
from pkg.algoritmoGenetico import AlgoritmoGenetico

class SocPlan:
    def __init__(self, maxRows, maxColumns, goal, initialState, mazeMap, victims, time, name = "RescuePlan", mesh = "square"):
        """
        Define as variaveis necessárias para a utilização do random plan por um unico agente.
        """
        self.name = name
        self.walls = []
        self.maxRows = maxRows
        self.maxColumns = maxColumns
        self.initialState = initialState
        self.currentState = initialState
        self.goalPos = goal
        self.actions = []
        self.mazeMap = mazeMap
        self.victims = victims
        self.time = time
        self.graph = []
        self.dists = []

        # print("vitimas SocPlan: ", self.victims)

        # Inicia matriz
        for i in range(self.maxRows):
            col = []
            for j in range(self.maxColumns):
                col.append([])
            self.graph.append(col)   

        for row in range(self.maxRows):
            for col in range(self.maxColumns):
                for dir in ["N", "S", "L", "O"]:
                    if self.isPossibleToMove(State(row, col)):
                        self.graph[row][col].append(dir)
       
        self.algoritmoGen = AlgoritmoGenetico(self.graph, self.maxRows, self.maxColumns, self.dists, self.victims, self.time, self.initialState)
        self.calculateAG()
        

    def calculateAG(self):
        self.algoritmoGen.calculate()
        self.actions = self.algoritmoGen.getBestSolution()
        print("Melhor solução: ", self.actions)

    def getVictimsDist(self):
        for i in range(len(self.victims)):
            col = []
            for j in range(len(self.victims)):
                col.append(None)
            self.dists.append(col)
        
        for i in range(len(self.victims)):
            pos_x = self.victims[i][0]
            self.dists[i][i] = 0
            for j in range(i+1, len(self.victims)):
                pos_y = self.victims[j][0]
                res = self.calculateCost(pos_x, pos_y)
                self.dists[i][j] = res
                reverse_path = [self.reverse(x) for x in res[1]]
                self.dists[j][i] = (res[0], reverse_path)

    def reverse(self, direction):
        if direction == "N":
            return "S"
        elif direction == "S":
            return "N"
        elif direction == "L":
            return "O"
        elif direction == "O":
            return "L"

    def calculateCost(self, pos_x, pos_y):
        pass

    def updateCurrentState(self, state):
         self.currentState = state

    def isPossibleToMove(self, toState):
        """Verifica se eh possivel ir da posicao atual para o estado (lin, col) considerando 
        a posicao das paredes do labirinto e movimentos na diagonal
        @param toState: instancia da classe State - um par (lin, col) - que aqui indica a posicao futura 
        @return: True quando é possivel ir do estado atual para o estado futuro """


        ## vai para fora do labirinto
        if (toState.col < 0 or toState.row < 0):
            return False

        if (toState.col >= self.maxColumns or toState.row >= self.maxRows):
            return False
        
        if len(self.walls) == 0:
            return True
        
        ## vai para cima de uma parede
        if (toState.row, toState.col) in self.walls:
            return False

        # vai na diagonal? Caso sim, nao pode ter paredes acima & dir. ou acima & esq. ou abaixo & dir. ou abaixo & esq.
        delta_row = toState.row - self.currentState.row
        delta_col = toState.col - self.currentState.col

        ## o movimento eh na diagonal
        if (delta_row !=0 and delta_col != 0):
            if (self.currentState.row + delta_row, self.currentState.col) in self.walls and (self.currentState.row, self.currentState.col + delta_col) in self.walls:
                return False
        
        return True

    def nextPosition(self):
         """ Sorteia uma direcao e calcula a posicao futura do agente 
         @return: tupla contendo a acao (direcao) e o estado futuro resultante da movimentacao """
         possibilities = ["N", "S", "L", "O"]
         movePos = { "N" : (-1, 0),
                    "S" : (1, 0),
                    "L" : (0, 1),
                    "O" : (0, -1)}

         rand = randint(0, 7)
         movDirection = possibilities[rand]
         state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])

         return movDirection, state

    def chooseAction(self):
        """ Escolhe o proximo movimento de forma aleatoria. 
        Eh a acao que vai ser executada pelo agente. 
        @return: tupla contendo a acao (direcao) e uma instância da classe State que representa a posição esperada após a execução
        """

        ## Tenta encontrar um movimento possivel dentro do tabuleiro 
        # result = self.randomizeNextPosition()

        # while not self.isPossibleToMove(result[1]):
        #     result = self.randomizeNextPosition()

        # return result

        movePos = { "N" : (-1, 0),
                    "S" : (1, 0),
                    "L" : (0, 1),
                    "O" : (0, -1)}

        if len(self.actions) > 0:
            action = self.actions.pop(0)
            state = State(self.currentState.row + movePos[action][0], self.currentState.col + movePos[action][1])
            return action, state


    def do(self):
        """
        Método utilizado para o polimorfismo dos planos

        Retorna o movimento e o estado do plano (False = nao concluido, True = Concluido)
        """
        
        nextMove = self.move()
        return (nextMove[1], self.goalPos == State(nextMove[0][0], nextMove[0][1]))   
    
     


        
       
        
        
