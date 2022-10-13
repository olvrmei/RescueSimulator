## AGENTE EXPLORADOR
### O agente explorador tem por objetivo construir um mapa do ambiente e localizar as vítimas 
### coletando seus sinais vitais (e.g. de respiração, pulsação). Este agente também obtém dados
### sobre a dificuldade de acesso ao ponto onde está cada vítima.
### Executa raciocíni on-line: percebe --> [delibera] --> executa ação --> percebe --> ...
import sys
import os
from pandas import DataFrame

from pkg.returnPlan import ReturnPlan


## Importa Classes necessarias para o funcionamento
sys.path.append(os.path.join("pkg"))
from model import Model
from problem import Problem
from state import State

## Importa o algoritmo para o plano
from explorePlan import ExplorePlan

##Importa o Planner
# sys.path.append(os.path.join("pkg", "planner"))
# from planner import Planner

## Classe que define o Agente
class AgentExp:
    def __init__(self, model, configDict):
        """ 
        Construtor do agente explorador
        @param model referencia o ambiente onde o agente estah situado
        """

        self.model = model

        # Dict com dado das vítimas encontradas
        # victimsData[victimId] = [sinais vitais, dificuldade de acesso]
        self.victimsData = dict()

        # Mapa do ambiente
        # Inicialmente define como livre todas as posições

        # self.mazeMap = [["" for _ in range(self.model.columns)] for _ in range(self.model.rows)]
        # for r in range(0, model.rows):
        #     for c in range(0, model.columns):
        #         self.updateMazeMap([r,c],"unknown")

        

        ## Obtem o tempo que tem para executar
        self.tl = configDict["Te"]
        print("Tempo disponivel: ", self.tl)
        
        ## Pega o tipo de mesh, que está no model (influência na movimentação)
        self.mesh = self.model.mesh


        ## Cria a instância do problema na mente do agente (sao suas crencas)
        self.prob = Problem()
        self.prob.createMaze(model.rows, model.columns, model.maze)
      
    
        # O agente le sua posica no ambiente por meio do sensor
        initial = self.positionSensor()
        self.prob.defInitialState(initial.row, initial.col)
        print("*** Estado inicial do agente: ", self.prob.initialState)

        self.mazeMap = [["unknown" for _ in range(0,initial.col+1)] for _ in range(0,initial.row+1)]

        self.printMazeMap()
        
        # Define o estado atual do agente = estado inicial
        self.currentState = self.prob.initialState

        # Define o estado objetivo:        
        # self.prob.defGoalState(randint(0,model.rows-1), randint(0,model.columns-1))
        
        # definimos um estado objetivo que veio do arquivo ambiente.txt
        # self.prob.defGoalState(model.maze.board.posGoal[0],model.maze.board.posGoal[1])
        # print("*** Objetivo do agente: ", self.prob.goalState)
        print("*** Total de vitimas existentes no ambiente: ", self.model.getNumberOfVictims())


        """
        DEFINE OS PLANOS DE EXECUÇÃO DO AGENTE
        """
        
        ## Custo da solução
        self.costAll = 0

        ## Cria a instancia do plano para se movimentar aleatoriamente no labirinto (sem nenhuma acao) 
        self.plan = ExplorePlan(model.rows, model.columns, self.prob.goalState, initial, "goal", self.mesh)

        ## adicionar crencas sobre o estado do ambiente ao plano - neste exemplo, o agente faz uma copia do que existe no ambiente.
        ## Em situacoes de exploracao, o agente deve aprender em tempo de execucao onde estao as paredes
        # self.plan.setWalls(model.maze.walls)
        
        ## Adiciona o(s) planos a biblioteca de planos do agente
        self.libPlan=[self.plan]

        ## inicializa acao do ciclo anterior com o estado esperado
        self.previousAction = "nop"    ## nenhuma (no operation)
        self.expectedState = self.currentState



    ## Metodo que define a deliberacao do agente 
    def deliberate(self):
        # se encontra vitima, adiciona ao array de vitimas
        # se encontra parede, adiciona ao array de paredes
        # diminui o tempo disponivel
        #calcula o tempo de retorno
        # se tempo disponivel > tempo de retorno, repete
        # senão volta para a base

        ## Verifica se há algum plano a ser executado
        if len(self.libPlan) == 0:
            print("Não há mais planos a serem executados")
            return -1   ## fim da execucao do agente, acabaram os planos
        
        if self.tl <= 0:
            print("Tempo esgotado")
            return -1

        if self.plan.name != "retornaParaBase": 
            # caso tenha que retornar para base
            # self.currentState = self.positionSensor()
            # self.plan.updateCurrentState(self.currentState) # atualiza o current state no plano
            # print("AgExp cre que esta em: ", self.currentState)

            self.shouldReturnToBase()

        # if self.plan.name != "retornaParaBase": 
        #     # caso tenha que retornar para base
        #     self.currentState = self.positionSensor()
        #     self.plan.updateCurrentState(self.currentState) # atualiza o current state no plano
        #     # print("AgExp cre que esta em: ", self.currentState)

        #     self.shouldReturnToBase()

        self.plan = self.libPlan[0]

        print("\n\n*** Inicio do ciclo raciocinio ***")
        print("Pos agente no amb.: ", self.positionSensor())

        ## Redefine o estado atual do agente de acordo com o resultado da execução da ação do ciclo anterior
        self.currentState = self.positionSensor()
        self.plan.updateCurrentState(self.currentState) # atualiza o current state no plano
        print("AgExp cre que esta em: ", self.currentState)

        ## Verifica se a execução do acao do ciclo anterior funcionou ou nao
        if not (self.currentState == self.expectedState):
            print("---> erro na execucao da acao ", self.previousAction, ": esperava estar em ", self.expectedState, ", mas estou em ", self.currentState)
            
            self.updateMazeMap([self.expectedState.row, self.expectedState.col], "obstacle")
            self.plan.updateWalls(self.expectedState.row, self.expectedState.col)



        ## Funcionou ou nao, vou somar o custo da acao com o total 
        self.costAll += self.prob.getActionCost(self.previousAction)
        print ("Custo até o momento (com a ação escolhida):", self.costAll)

        ## consome o tempo gasto
        self.tl -= self.prob.getActionCost(self.previousAction)
        print("Tempo disponivel: ", self.tl)
        
        ## Verifica se tem vitima na posicao atual    
        victimId = self.victimPresenceSensor()
        if victimId > 0 and (not self.positionExistsOnMazeMap(self.currentState) or self.mazeMap[self.currentState.row][self.currentState.col] != victimId):
            print ("vitima encontrada em ", self.currentState, " id: ", victimId, " sinais vitais: ", self.victimVitalSignalsSensor(victimId))

            # atualiza custo total
            self.costAll += self.prob.getActionCost("victim")
            print ("Custo até o momento (com a ação escolhida):", self.costAll)

            # consome o tempo gasto
            self.tl -= self.prob.getActionCost("victim")
            print("Tempo disponivel: ", self.tl)

            # atualiza o mapa do labirinto
            self.updateVictimsData(victimId, self.currentState, self.victimVitalSignalsSensor(victimId))
            self.updateMazeMap([self.currentState.row, self.currentState.col], str(victimId))
        
        if  not self.positionExistsOnMazeMap(self.currentState) or self.mazeMap[self.currentState.row][self.currentState.col] == "unknown":
            self.updateMazeMap([self.currentState.row, self.currentState.col], "free")

        self.printMazeMap()

        if self.plan.name != "retornaParaBase": 
        #     # caso tenha que retornar para base
        #     self.currentState = self.positionSensor()
        #     self.plan.updateCurrentState(self.currentState) # atualiza o current state no plano
        #     # print("AgExp cre que esta em: ", self.currentState)

            self.shouldReturnToBase()


        if self.plan.name == "retornaParaBase":
            if self.currentState == self.prob.initialState:
                print("Retornou para a base")
                return -1
        
        self.plan = self.libPlan[0]

        ## Define a proxima acao a ser executada
        ## currentAction eh uma tupla na forma: <direcao>, <state>
        result = self.plan.chooseAction()
        print("Ag deliberou pela acao: ", result[0], " o estado resultado esperado é: ", result[1])

        if self.previousAction == "nop" and result[0] == "nop":
            print("Nao ha mais acoes a serem executadas")
            return -1
        ## Executa esse acao, atraves do metodo executeGo 
        self.executeGo(result[0])
        self.previousAction = result[0]
        self.expectedState = result[1]       

        return 1

    def positionExistsOnMazeMap(self, position):
        if position.row >= 0 and position.row < len(self.mazeMap) and position.col >= 0 and position.col < len(self.mazeMap[0]):
            return True
        return False

    def printMazeMap(self):
        print("\nMapa atual: \n")
        print(DataFrame(self.mazeMap))
        #for row in self.mazeMap:
        #    print(row, "\n")

    ## Metodo que executa as acoes
    def executeGo(self, action):
        """Atuador: solicita ao agente físico para executar a acao.
        @param direction: Direcao da acao do agente {"N", "S", ...}
        @return 1 caso movimentacao tenha sido executada corretamente """

        ## Passa a acao para o modelo
        result = self.model.go(action)
        
        ## Se o resultado for True, significa que a acao foi completada com sucesso, e ja pode ser removida do plano
        ## if (result[1]): ## atingiu objetivo ## TACLA 20220311
        ##    del self.plan[0]
        ##    self.actionDo((2,1), True)
            

    ## Metodo que pega a posicao real do agente no ambiente
    def positionSensor(self):
        """Simula um sensor que realiza a leitura do posição atual no ambiente.
        @return instancia da classe Estado que representa a posição atual do agente no labirinto."""
        pos = self.model.agentPos
        return State(pos[0],pos[1])

    def victimPresenceSensor(self):
        """Simula um sensor que realiza a deteccao de presenca de vitima na posicao onde o agente se encontra no ambiente
           @return retorna o id da vítima"""     
        return self.model.isThereVictim()

    def victimVitalSignalsSensor(self, victimId):
        """Simula um sensor que realiza a leitura dos sinais da vitima 
        @param o id da vítima
        @return a lista de sinais vitais (ou uma lista vazia se não tem vítima com o id)"""     
        return self.model.getVictimVitalSignals(victimId)

    def victimDiffOfAcessSensor(self, victimId):
        """Simula um sensor que realiza a leitura dos dados relativos à dificuldade de acesso a vítima
        @param o id da vítima
        @return a lista dos dados de dificuldade (ou uma lista vazia se não tem vítima com o id)"""     
        return self.model.getDifficultyOfAcess(victimId)
    
    ## Metodo que atualiza a biblioteca de planos, de acordo com o estado atual do agente
    def updateLibPlan(self):
        for i in self.libPlan:
            i.updateCurrentState(self.currentState)

    def actionDo(self, posAction, action = True):
        self.model.do(posAction, action)

    def updateVictimsData(self, victimId, victimPos, vitalSigns):
        self.victimsData[victimId] = [(victimPos.row, victimPos.col), vitalSigns]

    def updateMazeMap(self, pos, label):

        if len(self.mazeMap) < pos[0] + 1:
            self.mazeMap.append(["unknown" for _ in range(len(self.mazeMap[0]))])
        
        if len(self.mazeMap[0]) < pos[1] + 1:
            for row in self.mazeMap:
                row.append("unknown")
        """
        Map labels: unknown | obstacle | victimId
        """
        self.mazeMap[pos[0]][pos[1]] = label

    def shouldReturnToBase(self):
    #  1.5 + 1.5 = 3 -> tempo para fazer uma ação e voltar pra mesma posição -> "margem de erro"
        if self.tl - 3 <= self.costAll :
            plan = ReturnPlan(self.prob, self.currentState, self.mazeMap)
            
            if self.tl - plan.getPlanCost() <= 3:
                print("AgExp vai volta para a base")
                print("\n*** Cálculo para retornar à base ***")
                print("Caminho de retorno para a base: ", plan.getPath())
                print("Custo total do caminho de retorno para a base: ", plan.getPlanCost(), "\n")
                self.libPlan.pop(0)
                self.libPlan.append(plan)

    def getNumberOfVictimsFound(self):
        return len(self.victimsData)

    def getTotalCost(self):
        return self.costAll

    def getVictimsData(self):
        return self.victimsData

    def getMazeMap(self):
        return self.mazeMap