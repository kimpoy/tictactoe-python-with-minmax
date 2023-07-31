import pygame
import sys
import numpy
import random
import copy

pygame.init()

width = 600
height = 600
background = (175, 211 ,226)

row = 3
column = 3

line_weight = 10
line_color = (249, 245, 235)

box = width // column
boxOne = height // column

screen = pygame.display.set_mode((width, height))
screen.fill(background)

offset = 50
circleWidth = 15
radius = 50
