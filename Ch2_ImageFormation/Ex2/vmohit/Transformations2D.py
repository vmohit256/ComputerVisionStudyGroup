import pygame
import numpy as np
import copy
import math

from src.pygame_utils import PyGameContext, COLORS
from src.shapes import Quadrilateral, Grid
from src.transformations import *

# Initialize Pygame
py_game_context = PyGameContext(width=800, height=800)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background
    py_game_context.screen.fill(py_game_context.background_color)

    # Draw the arbitrary quadrilateral
    q = Quadrilateral([[40, 40], [120, 40], [80, 80], [60, 80]], COLORS["red"], py_game_context) # weird quadrilateral
    q = Quadrilateral([[10, 10], [50, 10], [50, 50], [10, 50]], COLORS["red"], py_game_context) # square
    # q = Grid([[40, 40], [120, 40], [120, 120], [40, 120]])

    q.draw()

    # translation
    t1 = q.applyTransformation(translationTransformation(100, 0))
    t1.draw()

    # translation + rotation
    t2 = t1\
        .applyTransformation(translationTransformation(100, 0))
    
    t2 = t2\
        .applyTransformation( 
            rotationClockwiseAroundPointTransformation(t2.centroid(), np.pi / 4))
    t2.draw()

    # translation + rotation + scaling
    t3 = t2\
        .applyTransformation(translationTransformation(100, 150))
    t3 = t3\
        .applyTransformation( 
            scaleAroundPointTransformation(t3.centroid(), 3))
    t3.draw()

    # translation + rotation + scaling + deformation along an axis
    t4 = t3\
        .applyTransformation(translationTransformation(250, 0))
    t4 = t4\
        .applyTransformation( 
            deformAroundPointAtAnAngleTransformation(t4.centroid(), np.pi / 4, 1/2))
    t4.draw()

    # translation + rotation + scaling + deformation along an axis + rotate along y-axis
    t5 = t4\
        .applyTransformation(translationTransformation(-250, 250))
    t5 = t5\
        .applyTransformation( 
            rotationClockwiseAroundPointTransformation(t5.centroid(), np.pi / 4))
    t5 = t5.applyTransformation(
            rotateAlongYAxisAroundPointTransformation(t5.centroid(), -1 / (2 * 80)))
    t5.draw()

    # translation + rotation + scaling + deformation along an axis + rotate along x-axis
    t6 = t4\
        .applyTransformation(translationTransformation(-250, 500))
    t6 = t6\
        .applyTransformation( 
            rotationClockwiseAroundPointTransformation(t6.centroid(), np.pi / 4))
    t6 = t6.applyTransformation(
            rotateAlongXAxisAroundPointTransformation(t6.centroid(), -1 / (2 * 40)))
    t6.draw()

    # everything combined
    t7 = t5\
        .applyTransformation(translationTransformation(200, 100))
    t7 = t7.applyTransformation(
            rotateAlongXAxisAroundPointTransformation(t7.centroid(), -1 / (2 * 80)))
    t7.draw()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
