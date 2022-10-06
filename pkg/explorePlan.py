from random import randint
from state import State

class ExplorePlan:
    def __init__(self, maxRows, maxColumns, goal, initialState, name = "none", mesh = "square"):
        """
        Define as variaveis necessárias para a utilização do plano do explorador de busca online
        """
        self.walls = []
        self.maxRows = maxRows
        self.maxColumns = maxColumns
        self.initialState = initialState
        self.currentState = initialState
        self.goalPos = goal
        self.actions = []
        self.name = name

        self.actions = ["O", "SO", "S", "SE", "L", "NE", "N", "NO"]
        self.untried = dict()
        self.unbacktracked = dict()
        self.result = dict()

        for i in range(self.maxRows):
            for j in range(self.maxColumns):
                self.untried[(i,j)] = self.actions
                self.unbacktracked[(i,j)] = []
    

    def updateWalls(self, pos_x, pos_y):
        """ Adiciona uma parede no labirinto 
        @param pos_x: posicao x da parede
        @param pos_y: posicao y da parede
        """
        self.walls.append((pos_x, pos_y))
        

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

    def randomizeNextPosition(self):
        """ Sorteia uma direcao e calcula a posicao futura do agente 
        @return: tupla contendo a acao (direcao) e o estado futuro resultante da movimentacao """
        possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]
        movePos = { "N" : (-1, 0),
                   "S" : (1, 0),
                   "L" : (0, 1),
                   "O" : (0, -1),
                   "NE" : (-1, 1),
                   "NO" : (-1, -1),
                   "SE" : (1, 1),
                   "SO" : (1, -1)}

        rand = randint(0, 7)
        movDirection = possibilities[rand]
        state = State(self.currentState.row + movePos[movDirection][0], self.currentState.col + movePos[movDirection][1])

        return movDirection, state


    def nextPosition(self):
        """ Sorteia uma direcao e calcula a posicao futura do agente 
        @return: tupla contendo a acao (direcao) e o estado futuro resultante da movimentacao """
        movePos = { "N" : (-1, 0),
                   "S" : (1, 0),
                   "L" : (0, 1),
                   "O" : (0, -1),
                   "NE" : (-1, 1),
                   "NO" : (-1, -1),
                   "SE" : (1, 1),
                   "SO" : (1, -1)}
        
        #possibilities = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]
        possibilities = self.untried[(self.currentState.row, self.currentState.col)]
        currentPos = (self.currentState.row, self.currentState.col)
        
        if len(possibilities) > 0:
            rand = randint(0, len(possibilities) - 1)
            movDirection = possibilities[rand]
            possibilities.pop(rand)
            self.untried[currentPos] = possibilities 
            state = State(currentPos[0] + movePos[movDirection][0], currentPos[1] + movePos[movDirection][1])
            return (movDirection, state)
        
        if len(self.unbacktracked[currentPos]) > 0:
            lastPos = self.unbacktracked[currentPos].pop()
            state = State(lastPos[0], lastPos[1])
            direction = (lastPos[0] - currentPos[0], lastPos[1] - currentPos[1])
            movDirection = list(movePos.keys())[list(movePos.values()).index(direction)]
            return (movDirection, state)
        
        return self.randomizeNextPosition()


    def chooseAction(self):
        """ Escolhe o proximo movimento de forma aleatoria. 
        Eh a acao que vai ser executada pelo agente. 
        @return: tupla contendo a acao (direcao) e uma instância da classe State que representa a posição esperada após a execução
        """

        ## Tenta encontrar um movimento possivel dentro do tabuleiro 
        result = self.nextPosition()
        currentPos = (self.currentState.row, self.currentState.col)
        nextPos = (result[1].row, result[1].col)

        if self.isPossibleToMove(result[1]) and (currentPos, result[0]) not in self.result.keys():
            self.result[(currentPos, result[0])] = nextPos
            self.unbacktracked[nextPos].insert(0, currentPos)

        if not self.isPossibleToMove(result[1]):
            result = self.chooseAction()

        return result

    def do(self):
        """
        Método utilizado para o polimorfismo dos planos

        Retorna o movimento e o estado do plano (False = nao concluido, True = Concluido)
        """
        
        nextMove = self.move()
        return (nextMove[1], self.goalPos == State(nextMove[0][0], nextMove[0][1]))   
    
    def updateCurrentState(self, state):
        """ Atualiza o estado atual do agente 
        @param state: instancia da classe State - um par (lin, col) - que aqui indica a posicao futura 
        """
        self.currentState = state


        
       
        
        
