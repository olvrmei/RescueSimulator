from view import View
from maze import Maze

class Model:
    """Model implementa um ambiente na forma de um labirinto com paredes e com um agente.
     A indexação da posição do agente é feita sempre por um par ordenado (lin, col). Ver classe Labirinto."""

    def __init__(self, configData, mesh, load):
        """Construtor de modelo do ambiente físico (labirinto)
        @param rows: número de linhas do labirinto
        @param columns: número de colunas do labirinto
        @param mesh: define o tipo malha a ser usado
        @param load: define o nome do arquivo que contém o mapa a ser usado
        """

        self.rows = configData.getXMax()
        self.columns = configData.getYMax()
        self.mesh = mesh

        if self.rows <= 0:
            self.rows = 5
        if self.columns <= 0:
            self.columns = 5

        

        ## Seta a posicao do agente
        self.agentPos = configData.getBase()
        ## Seta a posicao do objetivo
        self.goalPos = [3,3]

        ## Cria a view
        self.view = View(self)
        ## Cria o labirinto
        self.maze = Maze(configData, self.mesh, self.view.getScreen(), load)
        ## Seta para o view o labirinto criado
        self.view.setBoard(self.maze.getBoard())


    ## Metodo que desenha tudo no pygame
    def draw(self):
        self.view.draw()

    ## Metodo que desenha o labirinto no pygame
    def drawToBuild(self):
        self.view.drawToBuild()

    ## Metodo que retorna o step do view
    def getStep(self):
        return self.view.getStep()

    ## Metodo que atualiza o labirinto
    def updateMaze(self):
        self.maze.updateWalls()

    def getNumberOfVictims(self):
        """ @return número total de vítimas no arquivo que define o ambiente """
        return self.maze.numberOfVictims

  
    def isPossibleToMove(self, from_row, from_col, to_row, to_col):
        """Verifica se eh possivel ir de (from_row, from_col) para (to_row, to_col)
        @param from_row: linha origem
        @param from_col: coluna origem
        @param to_row: linha para onde vai o agente
        @param to_col: col para onde vai o agente """

        ## vai para fora do labirinto
        if (to_col < 0 or to_row < 0):
            return -1
        if (to_col >= self.maze.maxColumns or to_row >= self.maze.maxRows):
            return -1
        
        ## vai para cima de uma parede
        if self.maze.walls[to_row][to_col] == 1:
            return -1

        row_dif = to_row - from_row
        col_dif = to_col - from_col

        ## vai na diagonal? Caso sim, nao pode ter paredes acima & dir. ou acima & esq. ou abaixo & dir. ou abaixo & esq.
        if (row_dif !=0 and col_dif != 0):
            if (self.maze.walls[from_row + row_dif][from_col] == 1 and
                self.maze.walls[from_row][from_col + col_dif] == 1):
                return -1
        
        return 1


    ## Metodo que atualiza a posicao do agente
    def setAgentPos(self, row, col):
        """Utilizada para colocar o agente em uma posicao especifica do ambiente
        @param row: a linha onde o agente será situado.
        @param col: a coluna onde o agente será situado.
        @return 1 se o posicionamento é possível, -1 se não for."""
        if (col < 0 or row < 0):
            return -1
        if (col >= self.maze.maxColumns or row >= self.maze.maxRows):
            return -1
        
        if self.maze.walls[row][col] == 1:
            return -1

        self.agentPos[0] = row
        self.agentPos[1] = col
        return 1

    ## Metodo que define a posicao do objetivo
    def setGoalPos(self, row, col):
        """Utilizada para colocar o objetivo na posição inicial.
        @param row: a linha onde o objetivo será situado.
        @param col: a coluna onde o objetivo será situado.
        @return 1 se o posicionamento é possível, -1 se não for."""
        if (col < 0 or row < 0):
            return -1
        if (col >= self.maze.maxColumns or row >= self.maze.maxRows):
            return -1
        if self.maze.walls[row][col] == 1:
            return -1

        self.goalPos[0] = row
        self.goalPos[1] = col
        return 1

    ## Metodo que executa a acao de movimento do plano 
    def go(self, action):
        """
            Esse metodo deve ser alterado de acordo com o action a ser passado
        """
        #result = plan.do()
        #step = result[0]
        if action == "N":
            row = self.agentPos[0] - 1
            col = self.agentPos[1]
        elif action == "S":
            row = self.agentPos[0] + 1
            col = self.agentPos[1]
        elif action == "O":
            row = self.agentPos[0]
            col = self.agentPos[1] - 1
        elif action == "L":
            row = self.agentPos[0]
            col = self.agentPos[1] + 1
        elif action =="NE":
            row = self.agentPos[0] - 1
            col = self.agentPos[1] + 1
        elif action =="NO":
            row = self.agentPos[0] - 1
            col = self.agentPos[1] - 1
        elif action =="SE":
            row = self.agentPos[0] + 1
            col = self.agentPos[1] + 1
        elif action =="SO":
            row = self.agentPos[0] + 1
            col = self.agentPos[1] - 1
        else:
            row = self.agentPos[0]
            col = self.agentPos[1]

        
        if (self.isPossibleToMove(self.agentPos[0], self.agentPos[1], row, col) == 1):
            self.setAgentPos(row, col)            
    
    
    def getVictimVitalSignals(self, victimId):
        """ retorna os sinais vitais da vítima identificada pelo id
        @param victimId é a posição da vítima dentro do vetor de sinais vitais
        @return a lista de sinais vitais ou uma lista vazia caso a vítima nao exista
        """
        if victimId < self.getNumberOfVictims():
            return self.maze.vitalSignals[victimId - 1]

        return []

    def getDifficultyOfAcess(self, victimId):
        """ retorna os dados de dificuldade de acesso à vítima identificada pelo id
        @param victimId é a posição da vítima dentro do vetor de sinais vitais
        @return a lista de sinais vitais ou uma lista vazia caso a vítima nao exista
        """
        if victimId < self.getNumberOfVictims():
            return self.maze.diffAccess[victimId - 1]
        return []

    def isThereVictim(self):
        """ retorna o id da vitima que está na posicao corrente do agente.
        O id é um número sequencial de 1 em diante atribuído pela ordem de aparição no arquivo ambiente.txt (ver maze.py)
        @return id >= 1 quando há vítima e, caso contrário retorna 0 """
        
        row = self.agentPos[0]
        col = self.agentPos[1]
        victimId = self.maze.victims[row][col]
        return victimId

    ## Metodo que executa uma acao (de não movimento)
    def do(self, posAction, action = True):
        ## Pega o bloco que deve ser executado a ação, e chama o metodo de execucao dela
        self.maze.board.listPlaces[posAction[0]][posAction[1]].doAction(action)
        return True

    def getVictimsVitalSignals(self):
        return self.maze.vitalSignals
