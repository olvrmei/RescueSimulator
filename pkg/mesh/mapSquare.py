from distutils.command.config import config
import square
import os
from datetime import datetime
## Classe que define o Mesh de quadrados
class MapSquare:
    def __init__(self, width, heigth, sideSquare, screen, configData, posBegin = (0,0), load = False):
        """
        @param width: Largura que a malha vai ter
        @param heigth: Altura que a malha vai ter
        @param sideSquare: Lado de cada quadrado
        @param screen: Screen do Pygame
        @param posBegin: Posicao de inicio
        @param load: Nome do arquivo que contem o mapa inicial (com os objetos e suas posicoes)
        """
        
        self.width = width
        self.heigth = heigth
        self.screen = screen
        self.sideSquare = sideSquare
        self.posBegin = posBegin

        ## Lista de quadrados
        self.listPlaces = []
        ## Variavel que armazena qual quadrado foi selecionado
        self.selectPlace = False

        ## posições das vitimas
        self.victimLocations = configData.getVitimas()

        ## Posicao do agente e do objetivo
        self.posAgent = configData.getBase()
        # self.posGoal = (3,3)

        # posições das paredes
        self.wallLocations = configData.getParedes()

        ## Variavel que armazena o arquivo que contem o mapa inicial
        self.load = load
        
        ## Chama o metodo para gerar a malha
        self.generateMap()

    ## Metodo que gera a malha de triangulos
    def generateMap(self):
        yr = 0
        y = self.posBegin[1]
        ## Percorre as linhas
        while y < self.heigth + self.posBegin[1]:
            x = self.posBegin[0]
            xr = 0
            line = []
            ## Percorre as colunas
            while x < self.width  + self.posBegin[0]:
                line.append(square.Square((x, y), self.sideSquare, self.screen, (yr, xr)))
                x += self.sideSquare
                xr += 1
            yr += 1
            y += self.sideSquare
            self.listPlaces.append(line)

        # print(self.listPlaces)

        for pos in self.victimLocations:
            self.listPlaces[pos[0]][pos[1]].itemInside = "Vitima"
            self.listPlaces[pos[0]][pos[1]].color = (255, 0, 0)

        for pos in self.wallLocations:
            self.listPlaces[pos[0]][pos[1]].itemInside = "Parede"
            self.listPlaces[pos[0]][pos[1]].color = (0, 0, 255)


        ##Faz o carregamento de um mapa salvo
        if self.load != False:
            ## Cria um objeto para armazenar cada informação
            things = {}
            ## Le o arquivo
            arq = open(os.path.join("config_data" ,self.load+".txt"),"r")
            for line in arq:
                ## O formato de cada linha é:
                ## Nome x,y x,y x,y
                values = line.split(" ")
                ## O primeiro dado é o nome do objeto, seguido por varias posicoes 
                things[values.pop(0)] = values

            ## Percorre os elementos que foram definidos
            for i in things:
                for j in things[i]:
                    pos = j.split(",")
                    # print(pos)
                    ## Define que naquela posicao vai ter determinado objeto
                    # self.listPlaces[int(pos[0])][int(pos[1])].itemInside = i
                    # ## Atualiza a cor do lugar
                    # self.listPlaces[int(pos[0])][int(pos[1])].updateColor()

            ## Seta as posicoes do robo e do objetivo
            # if "Agente" in things:
            #     pos = things["Agente"][0].split(",")
            #     self.posAgent = (int(pos[0]), int(pos[1]))
            # if "Objetivo" in things:
            #     pos = things["Objetivo"][0].split(",")
            #     self.posGoal = (int(pos[0]), int(pos[1]))


    ## Metodo que verifica o clique do mouse
   
    def checkClick(self, posMouse):

        ## Se já tiver selecionado um quadrado antes
        
        if self.selectPlace != False:
            obj = self.selectPlace.checkClickItens(posMouse)
            if obj != False:
                if obj.itemInside == "Agente":                   
                    self.listPlaces[self.posAgent[0]][self.posAgent[1]].agent = False
                    self.posAgent = obj.ide
                    obj.agent = True
                # elif obj.itemInside == "Objetivo":
                    
                #     self.listPlaces[self.posGoal[0]][self.posGoal[1]].goal = False
                #     self.posGoal = obj.ide
                #     obj.goal = True
                obj.itemInside = False
            self.selectPlace = False
            return True  
        else:
            ## Se não, verifica os quadrados e ve se algum deles foi clicado
            for i in self.listPlaces:
                for j in i:
                    if self.selectPlace != False:
                        break
                    ## Se sim, seta ele para a variavel
                    self.selectPlace = j.checkClick(posMouse)
            return False


    ## Metodo que mostra os quadrados na tela
    def show(self):
        for i in self.listPlaces:
            for j in i:
                j.show()

    ## Metodo que retorna a lista de quadrados
    def getListPlaces(self):
        return self.listPlaces

    ## Salva o mapa em um arquivo
    def save(self):
        things = {}
        x = 0
        ## Percorre a matriz com os lugares
        while x < len(self.listPlaces):
            y = 0
            while y < len(self.listPlaces[x]):
                ## Pega o que tem cada de cada bloco
                typeBlock = self.listPlaces[x][y].itemInside
                ## Se tiver alguma coisa, irá salvar
                if typeBlock != False:
                    ## Se o tipo do bloco já estiver dentro o things, apenas inclui mais um
                    if typeBlock in things:
                        things[typeBlock] = things[typeBlock] + " " + str(x) + "," + str(y)
                    ## Caso contrário adiciona o tip também
                    else:
                        things[typeBlock] = str(x) + "," + str(y)
                y += 1
            x += 1
        ## Ajusta tudo para ficar em um unica string
        config = ""
        for i in things:
            config += i + " " + things[i] + "\n"
        ## Pega a data e hora atual, para gerar sempre um nome diferente para cada arquivo
        today = datetime.now()
        name = str(today.year) + "" + str(today.month) + "" + str(today.day) + "" + str(today.hour) + "" + str(today.minute) 
        ## Salva o arquivo
        fil = open(os.path.join("config_data" ,name+".txt"), "w")
        fil.write(config)
        fil.close()
