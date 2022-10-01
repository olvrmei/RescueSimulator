import pygame, time, math, sys, os
from random import *
from pygame.locals import *
import boxItens

class Square:
    def __init__(self, ref, side, screen, ide):
        """
        @param ref: Posicao de referencia para iniciar o desenho
        @param side: Tamanho do lado
        @param screen: Screen do pygame
        @param ide: Identificado x,y
        """
        self.ref = ref
        self.side = side
        self.ide = ide
        self.screen = screen

        ##Se tiver algo dentro dele, ira ser True
        self.color = False
        self.itemInside = False
        self.agent = False
        self.goal = False
        self.victim = False

        ## Variaveis usadas para definir se um objeto é acionavel
        self.actionable = False
        self.stateAction = False


    ## Seta se o agente está dentro
    def setAgent(self, agentIn):
        self.agent = agentIn

    ## Seta se o objetivo está dentro
    def setGoal(self, goalIn):
        self.goal = goalIn

    ## Desenha o quadrado
    def show(self):
        ## A depender do que tem dentro, muda a cor
        if self.color != False:
            pygame.draw.rect(self.screen,self.color,(self.ref[0],self.ref[1],self.side,self.side))
        elif self.agent == True:
            pygame.draw.rect(self.screen,(0,255,0),(self.ref[0],self.ref[1],self.side,self.side))
        elif self.color != False:
            pygame.draw.rect(self.screen,self.color,(self.ref[0],self.ref[1],self.side,self.side))
        # elif self.goal == True:
        #     pygame.draw.rect(self.screen,(240,230,140),(self.ref[0],self.ref[1],self.side,self.side))
        elif self.color != False:
            pygame.draw.rect(self.screen,self.color,(self.ref[0],self.ref[1],self.side,self.side))
        elif self.victim == True:
            pygame.draw.rect(self.screen,(240,0,0),(self.ref[0],self.ref[1],self.side,self.side))
        else:
            pygame.draw.rect(self.screen,(255,255,255),(self.ref[0],self.ref[1],self.side,self.side))
        ## Desenha o contorno preto
        pygame.draw.rect(self.screen,(0,0,0),(self.ref[0],self.ref[1],self.side,self.side),1)
            
    ## Verifica se clicou dentro do quadrado
    def checkClick(self, posMouse):
        if posMouse[0] < self.ref[0] or posMouse[0] > self.ref[0] + self.side:
            return False
        elif posMouse[1] < self.ref[1] or posMouse[1] > self.ref[1] + self.side:
            return False
        else:
            ## Se clicou dentro, pinta o quadrado de preto
            pygame.draw.rect(self.screen,(0,0,0),(self.ref[0],self.ref[1],self.side,self.side))
            ## E abre a caixa de opções que podem estar dentro do quadrado
            self.openOptions()
            return self
        
    ## Abre a caixa de opções de blocos que podem estar dentro do quadrado
    def openOptions(self):
        self.selectItens = boxItens.BoxItens(self.screen)
        self.selectItens.show()

    ## Verifica se foi clicado em algum desses itens
    ## E define isso nos itens
    def checkClickItens(self, posMouse):
        self.itemInside = self.selectItens.checkClickIten(posMouse)
        if self.itemInside == "Agente":
            self.agent = True
            return self
        # elif self.itemInside == "Objetivo":
        #     self.goal = True
        #     return self
        self.updateColor()
        return False
    
    ## Metodo que atualiza a cor do bloco de acordo com o item
    def updateColor(self):
        if self.itemInside == "Parede":
            self.color = (139,69,19)
        elif self.itemInside == "Cone":
            self.color = (255,69,0)
        elif self.itemInside == "Caixa":
            self.color = (205,133,63)
        elif self.itemInside == "Lâmpada":
            self.color = (0,0,0)
            self.actionable = True
        elif self.itemInside == "Agente":
            self.agent = True
        # elif self.itemInside == "Objetivo":
        #     self.goal = True
        elif self.itemInside == "Vitima":
            self.victim = True
        else:
            self.color = False
    
    ## Método que define as ações dos objetos acionáveis
    def doAction(self, action):
        ## No momento, só tem a lampada. Então a unica ação dela é ligar ou desligar
        if self.itemInside == "Lâmpada":
            if self.stateAction == False:
                self.color = (255,255,0)
                self.stateAction = True
            else:
                self.color = (0,0,0)
                self.stateAction = False
            self.show()
        ## Para adicionar mais elementos, coloque no aqui

