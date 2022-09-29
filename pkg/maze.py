import sys
import os
import math

## Importa os tipos de malha disponíveis
sys.path.append(os.path.join("pkg", "mesh"))
import mapSquare, mapTriangle

## Classe que define o labirinto onde o agente esta
class Maze:
    """Maze representa um labirinto com paredes. A indexação das posições do labirinto é dada por par ordenado (linha, coluna).
    A linha inicial é zero e a linha máxima é (maxLin - 1). A coluna inicial é zero e a máxima é (maxCol - 1)."""

    def __init__(self, maxRows, maxColumns, mesh = "square", screen = False, load = False):
        """Construtor do labirinto
        @param maxRows: número de linhas do labirinto
        @param maxColumns: número de colunas do labirinto
        @param mesh: String com o nome da malha
        @param screen: Screen do pygame para a execucao
        """
        self.maxRows = maxRows
        self.maxColumns = maxColumns
        self.screen = screen
        # Matriz que representa o labirinto sendo as posições = 1 aquelas que contêm paredes
        self.walls = [[0 for j in range(maxColumns)] for i in range(maxRows)]  

        # Matriz que representa as posicoes das vitimas sendo as posições >= 1 aquelas que contêm vitimas
        # cada vitima eh identificada por um numero inteiro sequencial (id)
        self.victims = [[0 for j in range(maxColumns)] for i in range(maxRows)]

        # lista que contem os sinais vitais de cada uma das vitimas. É uma lista composta por sublistas 
        # onde o índice de uma sublista corresponde ao id da vítima (ver self.victims)
        self.vitalSignals = []

        # Lista que contem os dados de dificuldade de acesso a cada uma das vitimas. É uma lista composta por
        # sublistas onde o índice de uma sublista corresponde ao ide da vítima (anda junto com self.victims)
        self.diffAccess = []

        self.numberOfVictims = 0 # conta contas vitimas foram colocadas no ambiente 

        ## A depender do tipo de malha, os parametros mudam
        if mesh == "square":
            ## Cria uma malha com quadradaos
            ## Passa a largura e altura que deve ser preenchida por quadrados de determinado lado, a tela, e a posicao inicial para comecar
            ## para a malha inteira caber na tela, pegar a menor razao entre altura/linhas e larg/colunas para determinar o tamanho do lado do quadrado
            rowRate = 600/self.maxRows
            colRate = 900/self.maxColumns
            side = rowRate
            if colRate < colRate: 
                side=colRate 
            self.board = mapSquare.MapSquare(self.maxRows*side, self.maxColumns*side, side, self.screen, (0,0), load)
        elif mesh == "triangle":
            ## Define o tamanho dos dois lados iguais do triangulo isoceles
            side = 78
            ## Define o angulo de abertura dos dois lados com o tamanho acima (em radianos)
            angle = 0.261799
            ## Cria uma malha retangular
            ## Passa a quantidade de retangulos em X e em Y, o lado, o angulo, a rela e a posicao inicial para comecar
            self.board = mapTriangle.MapTriangle(maxColumns, maxRows, side, angle, self.screen, (50,50), load)
        else:
            self.board = False


    def updateWalls(self):
       
        ## Metodo que atualiza a lista dos objetos (vitimas) que estao no labirinto
        vs_file = open(os.path.join("config_data" ,"sinaisvitais.txt"),"r")
        # diff_file = open(os.path.join("config_data" ,"difacesso.txt"),"r")


        ## Pega a matriz com todos os lugares (seja quadrado ou triangulo)
        aux = self.board.getListPlaces()
        for i in aux:
            for j in i:
                ## Verifica o tipo do objeto, e coloca sua identificacao na matriz walls 
                if j.itemInside == "Parede":
                    pos = j.ide
                    self.walls[pos[0]][pos[1]] = 1
                elif j.itemInside == "Vitima":
                    pos = j.ide
                    self.numberOfVictims = self.numberOfVictims + 1
                    self.victims[pos[0]][pos[1]] = self.numberOfVictims
                    
                    vs_line = vs_file.readline()
                    if vs_line:
                        values = [float(signal) for signal in vs_line.split(" ")]
                        print("sinais vitais da vitima em (", pos[0], ",", pos[1], ") : ", values)
                        self.vitalSignals.append([])
                        self.vitalSignals[self.numberOfVictims-1].append(values)
                    else:
                        print("!!! warning: número de vítimas do ambiente maior do que número de sinais vitais")
                
                    # diff_line = diff_file.readline()
                    # if diff_line:
                    #     values = [float(signal) for signal in diff_line.split(" ")]
                    #     print("dif. de acesso a vitima em (", pos[0], ",", pos[1], ") : ", values)
                    #     self.diffAccess.append([])
                    #     self.diffAccess[self.numberOfVictims-1].append(values)
                    # else:
                    #     print("!!! warning: número de vítimas do ambiente maior do que número de dif. de acesso")

    ## Metodo que retorna a instancia criada da mesh
    def getBoard(self):
        return self.board
