from distutils.command.config import config
from ipaddress import v4_int_to_packed
import sys
import os
import time

from pkg.data import Data

## Importa as classes que serao usadas
sys.path.append(os.path.join("pkg"))
from model import Model
from agentRnd import AgentRnd
from agentExp import AgentExp
from agentSoc import AgentSoc



## Metodo utilizado para permitir que o usuario construa o labirindo clicando em cima
def buildMaze(model):
    model.drawToBuild()
    step = model.getStep()
    while step == "build":
        model.drawToBuild()
        step = model.getStep()
    ## Atualiza o labirinto
    model.updateMaze()

def desempenhoAgenteExplorador(model, agentExp):
    # Resultados do agente explorador
    print("*** Desempenho Agente Explorador ***")

    numeroVitimasEncontradas = agentExp.getNumberOfVictimsFound()
    totalVitimas = model.getNumberOfVictims()

    #  pve
    pve = numeroVitimasEncontradas / totalVitimas
    print("Porcentual de vítimas encontradas(pve): ", pve)

    # tve
    if numeroVitimasEncontradas > 0:
        tve = agentExp.getTotalCost() / numeroVitimasEncontradas
    else:
        tve = 0

    print("Tempo por vítima encontrada(tve): ", tve)

    # veg

    dadosVitimasEncontradas = agentExp.getVictimsData()

    ve1 = []
    ve2 = []
    ve3 = []
    ve4 = []

    if len(dadosVitimasEncontradas) > 0:
        for vitima in dadosVitimasEncontradas.keys():
            if dadosVitimasEncontradas[vitima][7] == 1.0:
                ve1.append(vitima)
            elif dadosVitimasEncontradas[vitima][7] == 2.0:
                ve2.append(vitima)
            elif dadosVitimasEncontradas[vitima][7] == 3.0:
                ve3.append(vitima)
            elif dadosVitimasEncontradas[vitima][7] == 4.0:
                ve4.append(vitima)

    dadosVitimas = model.getVictimsVitalSignals()

    V1 = []
    V2 = []
    V3 = []
    V4 = []

    if len(dadosVitimas) > 0:
        for vitima in dadosVitimas:
            if vitima[7] == 1.0:
                V1.append(vitima)
            elif vitima[7] == 2.0:
                V2.append(vitima)
            elif vitima[7] == 3.0:
                V3.append(vitima)
            elif vitima[7] == 4.0:
                V4.append(vitima)
    
    veg = (4 * len(ve1) + 3 * len(ve2) + 2 * len(ve3) + len(ve4)) / (4 * len(V1) + 3 * len(V2) + 2 * len(V3) + len(V4))

    print("Porcentual ponderado de vítimas encontradas por extrato de gravidade: ", veg)


def main():

    configData = Data("./config_data/ambiente.txt", "./config_data/sinaisvitais.txt")

    # Cria o ambiente (modelo) = Labirinto com suas paredes
    mesh = "square"

    # nome do arquivo de configuracao do ambiente - deve estar na pasta <proj>/config_data
    loadMaze = "ambiente"

    model = Model(configData, mesh, loadMaze)
    buildMaze(model)

    model.maze.board.posAgent
    # print(model.maze.board.posAgent)
    # model.maze.board.posGoal
    # print(model.maze.board.posGoal)
    # Define a posição inicial do agente no ambiente - corresponde ao estado inicial
    model.setAgentPos(model.maze.board.posAgent[0],model.maze.board.posAgent[1])

    # model.updateMaze()

    # model.setGoalPos(model.maze.board.posGoal[0],model.maze.board.posGoal[1])  
    model.draw()

    # Cria o agente explorador
    # agent = AgentRnd(model, configData.ambiente)
    agentExp = AgentExp(model, configData.ambiente)

    # Ciclo de raciocinio do agente explorador
    agentExp.deliberate()
    while agentExp.deliberate() != -1:
        model.draw()
        time.sleep(0.3) # para dar tempo de visualizar as movimentacoes do agente no labirinto
    model.draw()  

    desempenhoAgenteExplorador(model, agentExp)
    # Cria o agente socorrista
    agentSoc = agentSoc(model, configData.ambiente, agentExp.getMazeMap())

    agentSoc.deliberate()
    while agentSoc.deliberate() != -1:
        model.draw()
        time.sleep(0.3) # para dar tempo de visualizar as movimentacoes do agente no labirinto
    model.draw()  


    ## agente explorador
        # agente delibera
        # agente se movimenta
        # se encontra vitima, adiciona ao array de vitimas
        # se encontra parede, adiciona ao array de paredes
        # diminui o tempo disponivel
        #calcula o tempo de retorno
        # se tempo disponivel > tempo de retorno, repete
        # senão volta para a base

    ## agente socorrista
        # agente calcula quais vitimas consegue salvar
        # agente salva as vitimas
        # agente volta para a base

    ## analise de resultados



    # Ciclo de raciocínio do agente
    # agent.deliberate()
    # while agent.deliberate() != -1:
    #     model.draw()
    #     time.sleep(0.3) # para dar tempo de visualizar as movimentacoes do agente no labirinto
    # model.draw()    
    time.sleep(10)

if __name__ == '__main__':
    main()


    