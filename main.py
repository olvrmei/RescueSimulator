from distutils.command.config import config
import sys
import os
import time

from pkg.data import Data

## Importa as classes que serao usadas
sys.path.append(os.path.join("pkg"))
from model import Model
from agentRnd import AgentRnd


## Metodo utilizado para permitir que o usuario construa o labirindo clicando em cima
def buildMaze(model):
    model.drawToBuild()
    step = model.getStep()
    while step == "build":
        model.drawToBuild()
        step = model.getStep()
    ## Atualiza o labirinto
    model.updateMaze()

def main():

    configData = Data("./config_data/ambiente.txt", "./config_data/sinaisVitais.txt")

    # Cria o ambiente (modelo) = Labirinto com suas paredes
    mesh = "square"

    # nome do arquivo de configuracao do ambiente - deve estar na pasta <proj>/config_data
    loadMaze = "ambiente"

    model = Model(configData.getYMax(), configData.getXMax(), mesh, loadMaze)
    buildMaze(model)

    model.maze.board.posAgent
    print(model.maze.board.posAgent)
    model.maze.board.posGoal
    print(model.maze.board.posGoal)
    # Define a posição inicial do agente no ambiente - corresponde ao estado inicial
    model.setAgentPos(model.maze.board.posAgent[0],model.maze.board.posAgent[1])
    model.setGoalPos(model.maze.board.posGoal[0],model.maze.board.posGoal[1])  
    model.draw()

    # Cria um agente
    agent = AgentRnd(model, configData.ambiente)

    # Ciclo de raciocínio do agente
    agent.deliberate()
    while agent.deliberate() != -1:
        model.draw()
        time.sleep(0.3) # para dar tempo de visualizar as movimentacoes do agente no labirinto
    model.draw()    
        
if __name__ == '__main__':
    main()
