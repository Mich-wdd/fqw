import math

import pygame
from positions import Position


def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def linear_curve(positions, t, screen, color=(2, 242, 2), trigger=False):
    p0_x = (1 - t) * positions[0].x
    p0_y = (1 - t) * positions[0].y

    p1_x = t * positions[1].x
    p1_y = t * positions[1].y

    curve = (p0_x + p1_x, p0_y + p1_y)

    if trigger:
        # pygame.draw.line(screen, (0, 0, 0), (positions[0].x, positions[0].y), (positions[1].x, positions[1].y), 1)
        pygame.draw.line(screen, color, (positions[0].x, positions[0].y), (int(curve[0]), int(curve[1])), 4)
        pygame.draw.circle(screen, color, (int(curve[0]), int(curve[1])), 8)
    return int(curve[0]), int(curve[1])


def quadratic_curve(positions, t, screen, color, curve_list, green, trigger=False):
    p0_x = pow((1 - t), 2) * positions[0].x
    p0_y = pow((1 - t), 2) * positions[0].y

    p1_x = 2 * (1 - t) * t * positions[1].x
    p1_y = 2 * (1 - t) * t * positions[1].y

    p2_x = t ** 2 * positions[2].x
    p2_y = t ** 2 * positions[2].y

    curve = (p0_x + p1_x + p2_x, p0_y + p1_y + p2_y)
    if trigger:
        pygame.draw.line(screen, (0, 0, 0), (positions[0].x, positions[0].y), (positions[1].x, positions[1].y), 1)
        pygame.draw.line(screen, (0, 0, 0), (positions[1].x, positions[1].y), (positions[2].x, positions[2].y), 1)
        first_line = [positions[0], positions[1]]
        second_line = [positions[1], positions[2]]

        a = linear_curve(first_line, t, screen, green, False)
        b = linear_curve(second_line, t, screen, green, False)

        pygame.draw.line(screen, green, a, b, 2)
        pygame.draw.circle(screen, color, (int(curve[0]), int(curve[1])), 8)
    curve_list.append((int(curve[0]), int(curve[1])))


def draw_cubic_curve(positions, t, screen, color, curve_list, green, blue, quad_curve, quad_curve1, quad_curve2,
                     radius):
    p0_x = pow((1 - t), 3) * positions[0].x
    p0_y = pow((1 - t), 3) * positions[0].y

    p1_x = 3 * pow((1 - t), 2) * t * positions[1].x
    p1_y = 3 * pow((1 - t), 2) * t * positions[1].y

    p2_x = 3 * (1 - t) * pow(t, 2) * positions[2].x
    p2_y = 3 * (1 - t) * pow(t, 2) * positions[2].y

    p3_x = pow(t, 3) * positions[3].x
    p3_y = pow(t, 3) * positions[3].y

    curve = (p0_x + p1_x + p2_x + p3_x, p0_y + p1_y + p2_y + p3_y)

    # pygame.draw.line(screen, (0, 0, 0), (positions[0].x, positions[0].y), (positions[1].x, positions[1].y), 1)
    # pygame.draw.line(screen, (0, 0, 0), (positions[1].x, positions[1].y), (positions[2].x, positions[2].y), 1)
    # pygame.draw.line(screen, (0, 0, 0), (positions[2].x, positions[2].y), (positions[3].x, positions[3].y), 1)

    first_line = [positions[0], positions[1]]
    second_line = [positions[1], positions[2]]
    third_line = [positions[2], positions[3]]
    fourth_line = [positions[0], positions[1], positions[2]]
    fifth_line = [positions[1], positions[2], positions[3]]
    sixth_line = [positions[0], positions[2], positions[3]]

    a = linear_curve(first_line, t, screen, green, False)
    b = linear_curve(second_line, t, screen, green, False)
    c = linear_curve(third_line, t, screen, green, False)

    # pygame.draw.line(screen, green, a, b, 2)
    # pygame.draw.line(screen, green, b, c, 2)

    quadratic_curve(fourth_line, t, screen, (100, 100, 0), quad_curve, green, False)
    quadratic_curve(fifth_line, t, screen, (100, 100, 0), quad_curve1, green, False)
    quadratic_curve(sixth_line, t, screen, (100, 100, 0), quad_curve2, green, False)

    position_1 = Position(a[0], a[1])
    position_2 = Position(b[0], b[1])
    position_3 = Position(c[0], c[1])

    line1 = [position_1, position_2]
    line2 = [position_2, position_3]

    start = linear_curve(line1, t, screen, blue, False)
    end = linear_curve(line2, t, screen, blue, False)

    hyp = distance(start, end)
    cos = (end[0] - start[0]) / hyp
    sin = (end[1] - start[1]) / hyp
    current_point = (curve[0], curve[1])
    direction_end = (current_point[0] + 100 * cos, current_point[1] + 100 * sin)
    pygame.draw.line(screen, blue, current_point, direction_end, 3)

    # pygame.draw.line(screen, blue, start, end, 2)

    pygame.draw.circle(screen, color, (int(curve[0]), int(curve[1])), radius)
    curve_list.append((int(curve[0]), int(curve[1])))
