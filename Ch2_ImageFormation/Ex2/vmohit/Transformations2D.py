import pygame
import numpy as np
import copy

######## CLASSES ################################

class Quadrilateral:
    def __init__(self, points, color):
        self.points = points
        self.color = color
    
    def draw(self):
        pygame.draw.polygon(screen, self.color, self.points)

    def centroid(self):
        x_coordinate = sum([p[0] for p in self.points]) / len(self.points)
        y_coordinate = sum([p[1] for p in self.points]) / len(self.points)
        return [x_coordinate, y_coordinate]

class Transformation:
    def __init__(self, matrix):
        self.matrix = matrix
    
    def transform(self, point):
        homogeneous_point = np.array(list(point) + [1])
        transformed_point = self.matrix @ homogeneous_point
        if transformed_point[2] != 0:
            transformed_point = transformed_point / transformed_point[2]
        return transformed_point

# returns None if the transformation fails    
def applyTransformation(q, transformation):
    new_q = copy.deepcopy(q)
    for i in range(len(new_q.points)):
        transformed_point = transformation.transform(new_q.points[i])
        if transformed_point[2]==0: return None
        if (transformed_point[0] < 0  or transformed_point[0] >= WIDTH):
            return None
        if (transformed_point[1] < 0  or transformed_point[1] >= HEIGHT):
            return None
        new_q.points[i] = [transformed_point[0], transformed_point[1]]
    return new_q

# IMPORTANT: assumes that transformations[0] is applied first, then transformations[1], then transformations[2] and so on
def chainTransformations(transformations):
    matrix = None
    for transformation in transformations:
        if matrix is None:
            matrix = transformation.matrix
        else:
            matrix = transformation.matrix @ matrix
    return Transformation(matrix)

def translationTransformation(tx, ty):
    matrix = np.array([[1, 0, tx], 
                        [0, 1, ty], 
                        [0, 0, 1]])
    return Transformation(matrix)

def rotateClockwiseAroundOriginTransformation(theta):
    matrix = np.array([[np.cos(theta), -np.sin(theta), 0], 
                        [np.sin(theta), np.cos(theta), 0], 
                        [0, 0, 1]])
    return Transformation(matrix)

def rotationClockwiseAroundPointTransformation(point, theta):
    recenter_around_origin = translationTransformation(*[-v for v in point])
    rotate_clockwise_around_origin = rotateClockwiseAroundOriginTransformation(theta)
    relocate_to_original_position = translationTransformation(*point)
    return chainTransformations([recenter_around_origin, rotate_clockwise_around_origin, relocate_to_original_position])

def scaleAroundOriginTransformation(scale_factor):
    matrix = np.array([[scale_factor, 0, 0], 
                        [0, scale_factor, 0], 
                        [0, 0, 1]])
    return Transformation(matrix)

def scaleAroundPointTransformation(point, scale_factor):
    recenter_around_origin = translationTransformation(*[-v for v in point])
    scale_around_origin = scaleAroundOriginTransformation(scale_factor)
    relocate_to_original_position = translationTransformation(*point)
    return chainTransformations([recenter_around_origin, scale_around_origin, relocate_to_original_position])

def deformAlongYAxisTransformation(deform_factor):
    # for deform_factor < 1 it squishes it and for deform factor > 1 is stretches shapes along y-axis
    matrix = np.array([[1, 0, 0], 
                        [0, deform_factor, 0], 
                        [0, 0, 1]])
    return Transformation(matrix)

def deformAroundPointAtAnAngleTransformation(point, theta, deform_factor):
    recenter_around_origin = translationTransformation(*[-v for v in point])
    rotate_clockwise_around_origin = rotateClockwiseAroundOriginTransformation(theta)
    deform_along_y_axis = deformAlongYAxisTransformation(deform_factor)
    rotate_back_around_origin = rotateClockwiseAroundOriginTransformation(-theta)
    relocate_to_original_position = translationTransformation(*point)
    return chainTransformations([recenter_around_origin, rotate_clockwise_around_origin, 
                                 deform_along_y_axis, 
                                 rotate_back_around_origin, relocate_to_original_position])

def rotateAlongYAxisTransformation(matrix_x_coeff):
    matrix = np.array([[1, 0, 0], 
                        [0, 1, 0], 
                        [matrix_x_coeff, 0, 1]])
    return Transformation(matrix)

def rotateAlongYAxisAroundPointTransformation(point, matrix_x_coeff):
    recenter_around_origin = translationTransformation(*[-v for v in point])
    rotate_along_y_axis = rotateAlongYAxisTransformation(matrix_x_coeff)
    relocate_to_original_position = translationTransformation(*point)
    return chainTransformations([recenter_around_origin, rotate_along_y_axis, relocate_to_original_position])

def rotateAlongXAxisTransformation(matrix_y_coeff):
    matrix = np.array([[1, 0, 0], 
                        [0, 1, 0], 
                        [0, matrix_y_coeff, 1]])
    return Transformation(matrix)

def rotateAlongXAxisAroundPointTransformation(point, matrix_y_coeff):
    recenter_around_origin = translationTransformation(*[-v for v in point])
    rotate_along_x_axis = rotateAlongXAxisTransformation(matrix_y_coeff)
    relocate_to_original_position = translationTransformation(*point)
    return chainTransformations([recenter_around_origin, rotate_along_x_axis, relocate_to_original_position])

#################################################

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 500, 500
BACKGROUND_COLOR = (255, 255, 255)

COLORS = {
    "red": (255, 0, 0)
}

# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background
    screen.fill(BACKGROUND_COLOR)

    # Draw the arbitrary quadrilateral
    q = Quadrilateral([[40, 40], [120, 40], [80, 80], [60, 80]], COLORS["red"]) # weird quadrilateral
    q = Quadrilateral([[40, 40], [120, 40], [120, 120], [40, 120]], COLORS["red"]) # square

    q.draw()

    translated_q = applyTransformation(q, translationTransformation(150, 200))
    # translated_q.draw()

    translated_and_rotated_q = applyTransformation(translated_q, 
            rotationClockwiseAroundPointTransformation(translated_q.centroid(), np.pi / 4))
    
    translated_and_rotated_and_scaled_q = applyTransformation(translated_and_rotated_q, 
            scaleAroundPointTransformation(translated_and_rotated_q.centroid(), 2))

    translated_and_rotated_and_scaled_and_deformed_along_an_axis_q = \
        applyTransformation(translated_and_rotated_and_scaled_q, 
            deformAroundPointAtAnAngleTransformation(translated_and_rotated_and_scaled_q.centroid(), np.pi / 4, 1/2))

    t3 = translated_and_rotated_and_scaled_and_deformed_along_an_axis_q

    t4 = applyTransformation(t3, 
            rotationClockwiseAroundPointTransformation(t3.centroid(), np.pi / 4))

    t5 = applyTransformation(t4, 
            rotateAlongYAxisAroundPointTransformation(t4.centroid(), -1 / (2 * 80)))
    
    t5 = applyTransformation(t5, 
            rotateAlongXAxisAroundPointTransformation(t5.centroid(), 1 / (2 * 160)))

    t5.draw()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
