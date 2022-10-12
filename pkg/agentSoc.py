## AGENTE SOCORRISTA
### O agente socorrista leva suprimentos o mais rapidamente possível para as vítimas localizadas.
### O socorrista só entra em ação após o explorador ter finalizado a exploração do ambiente.
import sys
import os

## Importa Classes necessarias para o funcionamento
from model import Model
from problem import Problem
from state import State

## Importa o algoritmo para o plano
from socPlan import SocPlan

##Importa o Planner
# sys.path.append(os.path.join("pkg", "planner"))
# from planner import Planner

## Classe que define o Agente
class AgentSoc:
    def __init__(self, model, configDict, mazeMap, victims):
        """ 
        Construtor do agente socorrista
        @param model referencia o ambiente onde o agente estah situado
        """
       
        self.model = model

        ## Obtem o mapa do ambiente
        self.mazeMap = mazeMap
        self.rescuedVictims = []

        ## Obtem o tempo que tem para executar
        self.tl = configDict["Ts"]
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
        
        # Define o estado atual do agente = estado inicial
        self.currentState = self.prob.initialState

        # Define o estado objetivo:        
        # self.prob.defGoalState(randint(0,model.rows-1), randint(0,model.columns-1))
        
        # definimos um estado objetivo que veio do arquivo ambiente.txt
        self.prob.defGoalState(model.maze.board.posGoal[0],model.maze.board.posGoal[1])
        # print("*** Objetivo do agente: ", self.prob.goalState)
        print("*** Total de vitimas existentes no ambiente: ", self.model.getNumberOfVictims())


        """
        DEFINE OS PLANOS DE EXECUÇÃO DO AGENTE
        """
        
        ## Custo da solução
        self.costAll = 0

        ## Cria a instancia do plano para se movimentar aleatoriamente no labirinto (sem nenhuma acao) 
        self.plan = SocPlan(model.rows, model.columns, self.prob.goalState, initial, "goal", self.mesh, mazeMap, victims, self.tl)

        ## adicionar crencas sobre o estado do ambiente ao plano - neste exemplo, o agente faz uma copia do que existe no ambiente.
        ## Em situacoes de exploracao, o agente deve aprender em tempo de execucao onde estao as paredes
        self.plan.setWalls(model.maze.walls)
        
        ## Adiciona o(s) planos a biblioteca de planos do agente
        self.libPlan=[self.plan]

        ## inicializa acao do ciclo anterior com o estado esperado
        self.previousAction = "nop"    ## nenhuma (no operation)
        self.expectedState = self.currentState



    ## Metodo que define a deliberacao do agente 
    def deliberate(self):
        ## Verifica se há algum plano a ser executado
        if len(self.libPlan) == 0:
            return -1   ## fim da execucao do agente, acabaram os planos
        
        self.plan = self.libPlan[0]

        print("\n*** Inicio do ciclo raciocinio ***")
        print("Pos agente no amb.: ", self.positionSensor())

        ## Redefine o estado atual do agente de acordo com o resultado da execução da ação do ciclo anterior
        self.currentState = self.positionSensor()
        self.plan.updateCurrentState(self.currentState) # atualiza o current state no plano
        print("Ag cre que esta em: ", self.currentState)

        ## Verifica se a execução do acao do ciclo anterior funcionou ou nao
        if not (self.currentState == self.expectedState):
            print("---> erro na execucao da acao ", self.previousAction, ": esperava estar em ", self.expectedState, ", mas estou em ", self.currentState)

        ## Funcionou ou nao, vou somar o custo da acao com o total 
        self.costAll += self.prob.getActionCost(self.previousAction)
        print ("Custo até o momento (com a ação escolhida):", self.costAll) 

        ## consome o tempo gasto
        self.tl -= self.prob.getActionCost(self.previousAction)
        print("Tempo disponivel: ", self.tl)

        ## Verifica se atingiu o estado objetivo
        ## Poderia ser outra condição, como atingiu o custo máximo de operação
        #if self.prob.goalTest(self.currentState):
        #    print("!!! Objetivo atingido !!!")
        #    del self.libPlan[0]  ## retira plano da biblioteca
        
        ## Verifica se tem vitima na posicao atual    
        victimId = self.victimPresenceSensor()
        if victimId > 0 and victimId not in self.rescuedVictims:
            print ("vitima socorrida em ", self.currentState, " id: ", victimId, " sinais vitais: ", self.victimVitalSignalsSensor(victimId))
            self.rescuedVictims.append(victimId)


        ## Define a proxima acao a ser executada
        ## currentAction eh uma tupla na forma: <direcao>, <state>
        result = self.plan.chooseAction()
        print("Ag deliberou pela acao: ", result[0], " o estado resultado esperado é: ", result[1])

        ## Executa esse acao, atraves do metodo executeGo 
        self.executeGo(result[0])
        self.previousAction = result[0]
        self.expectedState = result[1]       

        return 1

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
