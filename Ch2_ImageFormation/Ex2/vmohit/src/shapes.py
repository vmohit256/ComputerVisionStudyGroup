import pygame
import numpy as np
import copy
import math

class Quadrilateral:
    def __init__(self, points, color, pygame_context):
        self.pygame_context = pygame_context
        self.points = copy.deepcopy(points)
        self.color = color
    
    def draw(self):
        pygame.draw.polygon(self.pygame_context.screen, self.color, self.points)

    def centroid(self):
        x_coordinate = sum([p[0] for p in self.points]) / len(self.points)
        y_coordinate = sum([p[1] for p in self.points]) / len(self.points)
        return [x_coordinate, y_coordinate]

    # returns None if the transformation fails   
    def applyTransformation(self, transformation):
        new_q = Quadrilateral(self.points, self.color, self.pygame_context)
        for i in range(len(new_q.points)):
            transformed_point = transformation.transform(new_q.points[i])
            if transformed_point[2]==0: return None
            if (transformed_point[0] < 0  or transformed_point[0] >= self.pygame_context.width):
                return None
            if (transformed_point[1] < 0  or transformed_point[1] >= self.pygame_context.height):
                return None
            new_q.points[i] = [transformed_point[0], transformed_point[1]]
        return new_q
    
class Grid:
    # intially, each grid is always a grid of rectangles
    def __init__(self, four_corners, step_length=10):
        self.four_corners = copy.deepcopy(four_corners)
        self.step_length = step_length
        ref_point = four_corners[0]
        if four_corners[1][0] != ref_point[0]:
            x_delta_neighbor = four_corners[1]
            y_delta_neighbor = four_corners[3]
        else:
            x_delta_neighbor = four_corners[3]
            y_delta_neighbor = four_corners[1]
        
        self.quadrilaterals = []

        sign = lambda x: 1 if x>=0 else -1

        x_total_delta = math.floor(x_delta_neighbor[0] - ref_point[0])
        x_step = math.floor(sign(x_total_delta) * step_length)
        x_deltas = list(range(0, x_total_delta, x_step)) + [x_total_delta]
        
        y_total_delta = math.floor(y_delta_neighbor[1] - ref_point[1])
        y_step = math.floor(sign(y_total_delta) * step_length)
        y_deltas = list(range(0, y_total_delta, y_step)) + [y_total_delta]

        for j in range(1, len(y_deltas)):
            self.quadrilaterals.append([])
            for i in range(1, len(x_deltas)):
                color = (max(0, math.ceil(255 * (1 - (i-1)/len(x_deltas) - (j-1)/len(y_deltas)))),
                         math.ceil(255 * j / len(y_deltas)),
                         math.ceil(255 * i / len(y_deltas)))
                points = [
                    [ref_point[0] + (i-1) * x_step, ref_point[1] + (j-1) * y_step],
                    [ref_point[0] + i * x_step, ref_point[1] + (j-1) * y_step],
                    [ref_point[0] + i * x_step, ref_point[1] + j * y_step],
                    [ref_point[0] + (i-1) * x_step, ref_point[1] + j * y_step]
                ]
                self.quadrilaterals[-1].append(Quadrilateral(points, color))

    def draw(self):
        Quadrilateral(self.four_corners, (255, 0, 0)).draw()
        for quad_row in self.quadrilaterals:
            for quadrilateral in quad_row:
                quadrilateral.draw()

    def centroid(self):
        x_coordinate = sum([p[0] for p in self.four_corners]) / len(self.four_corners)
        y_coordinate = sum([p[1] for p in self.four_corners]) / len(self.four_corners)
        return [x_coordinate, y_coordinate]
    
    # returns None if the transformation fails on any of the quadrilaterals  
    def applyTransformation(self, transformation):
        new_grid = Grid(self.four_corners, self.step_length)
        for i in range(len(new_grid.quadrilaterals)):
            for j in range(len(new_grid.quadrilaterals[i])):
                new_grid.quadrilaterals[i][j] = new_grid.quadrilaterals[i][j]\
                    .applyTransformation(transformation)
                if new_grid.quadrilaterals[i][j] is None:
                    return None
        q = Quadrilateral(new_grid.four_corners, (255, 0, 0)).applyTransformation(transformation)
        if q is None:
            return None
        new_grid.four_corners = q.points
        return new_grid