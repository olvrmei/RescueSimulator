import pygame, time, math, sys, os
from pygame.locals import *
import item


class BoxItens:
    def __init__(self, screen):
        ## Screen do pygame
        self.screen = screen
        ## Define o tamanho da janela que abre ao clicar em um bloco
        self.size = (300, 500)
        ## Posicao do fundo
        self.posBackground = (self.screen.get_width()/2 - self.size[0]/2, self.screen.get_height()/2 - self.size[1]/2)

        ## Itens disponíveis
        self.items = []
        self.items.append(item.Item("Robô", "robot.png", (50, 65), (self.posBackground[0] + 20, self.posBackground[1] + 70 ), self.screen))
        # self.items.append(item.Item("Objetivo", "goal.png", (60, 60), (self.posBackground[0] + 90, self.posBackground[1] + 70 ), self.screen))

        self.items.append(item.Item("Cone", "cone.png", (50, 65), (self.posBackground[0] + 20, self.posBackground[1] + 180 ), self.screen))
        self.items.append(item.Item("Parede", "wall.png", (60, 60), (self.posBackground[0] + 90, self.posBackground[1] + 180 ), self.screen))
        self.items.append(item.Item("Caixa", "box.png", (60, 60), (self.posBackground[0] + 170, self.posBackground[1] + 180 ), self.screen))

        self.items.append(item.Item("Lâmpada", "bulb.png", (60, 60), (self.posBackground[0] + 20, self.posBackground[1] + 290 ), self.screen))

       
        
    def show(self):
        ## Desenha o fundo branco com o contoro preto
        pygame.draw.rect(self.screen, (255,255,255), [self.posBackground[0], self.posBackground[1], self.size[0], self.size[1]])
        pygame.draw.rect(self.screen, (0,0,0), [self.posBackground[0], self.posBackground[1], self.size[0], self.size[1]], 1)
        ## Mostra todos os itens
        for i in self.items:
            i.show()

    ## Verifica se algum item foi clicado. Se sim, retorna o item
    def checkClickIten(self, posMouse):
        for i in self.items:
            itemClicked = i.checkClick(posMouse)
            if itemClicked != False:
                break
        return itemClicked
        
