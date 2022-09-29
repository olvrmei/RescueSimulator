import triangle
import math, os
from datetime import datetime
## Método que cria a malha de triangulos
class MapTriangle:
    def __init__(self, qtdWidth, qtdHeigth, side, angle, screen, posBegin = (50,50), load = False):
        """
        @param qtdWidth: qtd de triangulos em cada linha
        @param qtdHeigth: qtd de linhas (1 triangulo por linha
        @param side: Tamanho dos dois lados iguais do triangulo isóceles
        @param angle: Angulo de abertura dos dois lados iguais
        @param screen: Screen do Pygame
        @param posBegin: Posicao inicial
        @param load: Nome do arquivo que contem o mapa inicial (com os objetos e suas posicoes)
        """
        
        self.qtdWidth = qtdWidth
        self.qtdHeigth = qtdHeigth
        self.screen = screen
        self.side = side
        self.angle = angle
        self.posBegin = posBegin
        ## Calcula a altura dos triangulos
        self.heightTriangle = side*math.cos(angle)
        ## Calcula a base dos triangulos
        self.baseTriangle = math.sqrt(side**2 - (self.heightTriangle**2))

        ## Variavel que armazena o triangulo que foi clicado
        self.selectPlace = False
        ## Lista de todos os triangulos
        self.listPlaces = []

        ## Variavel que armazena o arquivo que contem o mapa inicial
        self.load = load
        
        ## Posicao do agente e do objetivo
        self.posAgent = (0,0)
        # self.posGoal = (1,1)
        ## Chama o metodo para gerar a malha de triangulos
        self.generateMap()

    ## Metodo para gerar a malha de triangulos
    def generateMap(self):
        y = self.posBegin[1]
        control = True
        posYCorrect = y
        contY = 0
        ## Percorre as linhas
        while contY < self.qtdHeigth:
            x = self.posBegin[0]
            contX = 0
            line = []
            ## Fica invertendo entre os dois tipos de triangulos (para cima e para baixo)
            if control == True:
                line.append(triangle.Triangle((x, y), self.side, self.angle, 0, self.screen, (contY, contX)))
                first = 1
                second = 0
                
            else:
                line.append(triangle.Triangle((x, y), self.side, self.angle, 1, self.screen, (contY, contX)))
                first = 0
                second = 1
                
            posYCorrect = line[-1].getP2()[1]
            x += self.baseTriangle
            contX = 1
            ## Percorre as colunas
            while contX < self.qtdWidth:
                """
                OBS: Como os triangulos tem seus lados com números não inteiros, se colocar pela posição sozinha, vai acabar ficando torto a linha.
                Por isso colocamos o próximo triangulo de acordo com o eixo X do anterior, para todos ficarem alinhados
                """
                line.append(triangle.Triangle((line[-1].getP2()[0], posYCorrect), self.side, self.angle, first, self.screen, (contY, contX)))
                contX += 1
                if contX >= self.qtdWidth:
                    break
                line.append(triangle.Triangle((line[-1].getP2()[0], y), self.side, self.angle, second, self.screen, (contY, contX)))
                x += (2*self.baseTriangle)
                contX += 1
            self.listPlaces.append(line)
            ## Soma a base a cada dois triangulos
            if control == True:    
                y += 2*self.heightTriangle
            ## Inverte o tipo do triangulo que começa a linha
            control = not control
            contY += 1

        ##Faz o carregamento de um mapa salvo
        if self.load != False:
            ## Cria um objeto para armazenar cada informação
            things = {}
            ## Le o arquivo
            arq = open(os.path.join("pkg","mesh", "loads", self.load+".txt"),"r")
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
                    ## Define que naquela posicao vai ter determinado objeto
                    self.listPlaces[int(pos[0])][int(pos[1])].itemInside = i
                    ## Atualiza a cor do lugar
                    self.listPlaces[int(pos[0])][int(pos[1])].updateColor()
                    
            ## Seta as posicoes do robo e do objetivo
            if "Robô" in things:
                pos = things["Robô"][0].split(",")
                self.posAgent = (int(pos[0]), int(pos[1]))
            if "Objetivo" in things:
                pos = things["Objetivo"][0].split(",")
                self.posGoal = (int(pos[0]), int(pos[1]))
    
    ## Metodo que verifica o clique do mouse
    def checkClick(self, posMouse):
        ## Se já tiver selecionado um quadrado antes
        if self.selectPlace != False:
            obj = self.selectPlace.checkClickItens(posMouse)
            if obj != False:
                print(obj)
                if obj.itemInside == "Robô":                   
                    self.listPlaces[self.posAgent[0]][self.posAgent[1]].agent = False
                    self.posAgent = obj.ide
                    obj.agent = True
                elif obj.itemInside == "Objetivo":
                    
                    self.listPlaces[self.posGoal[0]][self.posGoal[1]].goal = False
                    self.posGoal = obj.ide
                    obj.goal = True
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
        fil = open(os.path.join("pkg","mesh", "loads" ,name+".txt"), "w")
        fil.write(config)
        fil.close()
