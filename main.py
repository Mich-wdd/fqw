import math
import pygame
import os
from positions import Position
from curves import linear_curve, draw_cubic_curve


def parameter_calculation(my_angle):
    global gates, gates_center, robot_final_coordinates, p1, p2, cubic_positions
    gates = [(gates_x, height / 2 - 200), (gates_x, height / 2 + 200)]
    gates_center = Position(gates_x, height / 2)
    hypotenuse = distance(ball_coordinates, gates_center)
    cos = (ball_coordinates.x - gates_center.x) / hypotenuse
    sin = (ball_coordinates.y - gates_center.y) / hypotenuse
    robot_final_coordinates = Position(
        ball_coordinates.x + (ball_radius + robot_radius) * cos,
        ball_coordinates.y + (ball_radius + robot_radius) * sin)
    p1 = Position(robot_coordinates.x + vector * math.cos(my_angle), robot_coordinates.y - vector * math.sin(my_angle))
    p2 = Position(robot_final_coordinates.x + vector * cos, robot_final_coordinates.y + vector * sin)
    cubic_positions = [robot_coordinates, p1, p2, robot_final_coordinates]


def distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def check_borders(my_point):
    return 0 < my_point.y < height and 0 < my_point.x < width


def re_checking(current_point, old_point):
    if not check_borders(current_point):
        current_point.x = old_point.x
        current_point.y = old_point.y
        return False
    return True


os.environ["SDL_VIDEO_CENTERED"] = '1'

width, height = 1920, 1080
size = (width, height)

# Param
gates_x = 1800
ball_coordinates = Position(1000, 400)
ball_radius = 10
robot_coordinates = Position(1800, 100)
robot_radius = 50
vector = 500
angle = start_phi = phi = math.radians(45)

p1 = p2 = robot_final_coordinates = gates_center = Position()
gates = [(gates_x, height / 2 - 200), (gates_x, height / 2 + 200)]

cubic_positions = []
curve1 = []
curve2 = []
curve3 = []
cubic_curve = []

parameter_calculation(phi)

pygame.init()
pygame.display.set_caption("RoboSoccer")
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 32)

white = (235, 235, 235)
black = (20, 20, 20)
red = (242, 2, 2)
green = (2, 242, 2)
blue = (2, 146, 255)

t = 0
speed = 0.005
acceleration = 0.001
omega = 0.005

# max_x = max(robot_coordinates.x, robot_final_coordinates.x, p1.x, p2.x)
# min_x = min(robot_coordinates.x, robot_final_coordinates.x, p1.x, p2.x)
# max_y = max(robot_coordinates.y, robot_final_coordinates.y, p1.y, p2.y)
# min_y = min(robot_coordinates.y, robot_final_coordinates.y, p1.y, p2.y)

run = True
go = False
initial_turn = 0
start = True
end = False

while run:
    screen.fill(white)
    pygame.draw.line(screen, (0, 0, 0), gates[0], gates[1], 3)
    pygame.draw.line(screen, (0, 0, 0), (gates[0][0] - 10, gates[0][1]), (gates[0][0] + 10, gates[0][1]), 3)
    pygame.draw.line(screen, (0, 0, 0), (gates[1][0] - 10, gates[1][1]), (gates[1][0] + 10, gates[1][1]), 3)
    if not end:
        pygame.draw.circle(screen, green, ball_coordinates.point(), ball_radius)
    if start:
        pygame.draw.circle(screen, red, robot_coordinates.point(), robot_radius)
        if initial_turn == 0:
            pygame.draw.line(screen, (0, 0, 0), robot_coordinates.point(), p1.point(), 3)
    for point in cubic_positions:
        point.display(screen, black)
    clock.tick(fps)
    frameRate = int(clock.get_fps())
    pygame.display.set_caption("Bezier Curve - FPS : {}".format(frameRate))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_RETURN:
                if check_borders(p1):
                    start = False
                else:
                    p1_old = p1
                    flag = 0
                    while initial_turn == 0:
                        print(p1.x, p1.y)
                        start_phi = angle = phi
                        if not 0 < p1.y < height:
                            if p1.y < 0:
                                if 0 < phi < math.pi / 2 or flag == 1:
                                    print('p1.y < 0; phi < math.pi / 2 or flag == 1')
                                    p1 = Position(
                                        robot_coordinates.x + math.sqrt(
                                            vector ** 2 - (robot_coordinates.y - robot_radius) ** 2),
                                        robot_radius)
                                    if not re_checking(p1, p1_old):
                                        flag = 2
                                    else:
                                        initial_turn = 1
                                        phi = math.acos((p1.x - robot_coordinates.x) / vector)
                                        continue
                                if math.pi > phi > math.pi / 2 or flag == 2:
                                    print('p1.y < 0; phi > math.pi / 2 or flag == 2')
                                    p1 = Position(
                                        robot_coordinates.x - math.sqrt(
                                            vector ** 2 - (robot_coordinates.y - robot_radius) ** 2),
                                        robot_radius)
                                    if not re_checking(p1, p1_old):
                                        flag = 1
                                    else:
                                        initial_turn = 2
                                        phi = math.acos((p1.x - robot_coordinates.x) / vector)
                                        continue
                            elif p1.y > height:
                                if math.pi < phi < 3 * math.pi / 2 or flag == 1:
                                    print('p1.y > height; phi < 3 * math.pi / 2 or flag == 1')
                                    print("(", p1.x, p1.y, ")", "(", p1_old.x, p1_old.y, ")", flag)
                                    p1 = Position(
                                        robot_coordinates.x - math.sqrt(
                                            vector ** 2 - (height - robot_radius - robot_coordinates.y) ** 2),
                                        height - robot_radius)
                                    if not re_checking(p1, p1_old):
                                        flag = 2
                                        print("(", p1.x, p1.y, ")", "(", p1_old.x, p1_old.y, ")", flag)
                                    else:
                                        initial_turn = 1
                                        phi = math.acos((p1.x - robot_coordinates.x) / vector)
                                        continue
                                if 2 * math.pi > phi > 3 * math.pi / 2 or flag == 2:
                                    print('p1.y > height; phi > 3 * math.pi / 2 or flag == 2')
                                    p1 = Position(
                                        robot_coordinates.x + math.sqrt(
                                            vector ** 2 - (height - robot_radius - robot_coordinates.y) ** 2),
                                        height - robot_radius)
                                    if not re_checking(p1, p1_old):
                                        flag = 1
                                    else:
                                        initial_turn = 2
                                        phi = 2*math.pi - math.acos((p1.x - robot_coordinates.x) / vector)
                                        continue

                        elif not 0 < p1.x < width:
                            if p1.x < 0:
                                if math.pi / 2 < phi < math.pi or flag == 1:
                                    print('p1.x < 0; phi < math.pi or flag == 1')
                                    print("(", p1.x, p1.y, ")", "(", p1_old.x, p1_old.y, ")", flag)
                                    p1 = Position(robot_radius, robot_coordinates.y - math.sqrt(
                                        vector ** 2 - (robot_coordinates.x - robot_radius) ** 2))
                                    if not re_checking(p1, p1_old):
                                        flag = 2
                                        print("(", p1.x, p1.y, ")", "(", p1_old.x, p1_old.y, ")", flag)
                                    else:
                                        initial_turn = 1
                                        phi = math.acos((p1.x - robot_coordinates.x) / vector)
                                        continue
                                if 3 * math.pi / 2 > phi > math.pi or flag == 2:
                                    print('p1.x < 0; phi > math.pi or flag == 2')
                                    print("(", p1.x, p1.y, ")", "(", p1_old.x, p1_old.y, ")", flag)
                                    p1 = Position(robot_radius, robot_coordinates.y + math.sqrt(
                                        vector ** 2 - (robot_coordinates.x - robot_radius) ** 2))
                                    if not re_checking(p1, p1_old):
                                        flag = 1
                                        print("(", p1.x, p1.y, ")", "(", p1_old.x, p1_old.y, ")", flag)
                                    else:
                                        initial_turn = 2
                                        phi = 2 * math.pi - math.acos((p1.x - robot_coordinates.x) / vector)
                                        continue
                            if p1.x > width:
                                if 0 < phi < math.pi / 2 or flag == 1:
                                    print('p1.x > width; 0 < phi < math.pi / 2 or flag == 1')
                                    p1 = Position(width - robot_radius, robot_coordinates.y - math.sqrt(
                                        vector ** 2 - (width - robot_coordinates.x - robot_radius) ** 2))
                                    if not re_checking(p1, p1_old):
                                        flag = 2
                                        print("(", p1.x, p1.y, ")", "(", p1_old.x, p1_old.y, ")", flag)
                                    else:
                                        initial_turn = 2
                                        phi = 2 * math.pi - math.acos((p1.x - robot_coordinates.x) / vector)
                                        continue
                                if 3 * math.pi / 2 < phi < 2 * math.pi or flag == 2:
                                    print('p1.x > width; 3 * math.pi / 2 < phi < 2 * math.pi or flag == 2')
                                    p1 = Position(width - robot_radius, robot_coordinates.y + math.sqrt(
                                        vector ** 2 - (width - robot_coordinates.x - robot_radius) ** 2))
                                    if not re_checking(p1, p1_old):
                                        flag = 1
                                    else:
                                        initial_turn = 1
                                        phi = 2 * math.pi - math.acos((p1.x - robot_coordinates.x) / vector)
                                        continue
                        print(angle, start_phi, phi, math.degrees(phi))

    if initial_turn != 0:
        # print(0, math.pi/2, math.pi, 3*math.pi/2, 2*math.pi)
        if initial_turn == 1:
            # if start_phi < phi and angle < phi:
            #     angle -= 2*math.pi
            # print('hi')
            angle = angle - omega
            if angle <= phi:
                angle = phi
                initial_turn = 0
                start = False
        elif initial_turn == 2:
            if start_phi > phi and angle > phi:
                angle -= 2 * math.pi
            print('hi2')
            angle = angle + omega
            if angle >= phi:
                angle = phi
                initial_turn = 0
                start = False
        parameter_calculation(angle)
        direction_end = (robot_coordinates.x + 100 * math.cos(angle), robot_coordinates.y - 100 * math.sin(angle))
        pygame.draw.line(screen, blue, robot_coordinates.point(), direction_end, 3)

    if not start and not end:
        # screen.fill(white)
        # pygame.draw.line(screen, (0, 0, 0), gates[0], gates[1], 3)
        # pygame.draw.line(screen, (0, 0, 0), (gates[0][0] - 10, gates[0][1]), (gates[0][0] + 10, gates[0][1]), 3)
        # pygame.draw.line(screen, (0, 0, 0), (gates[1][0] - 10, gates[1][1]), (gates[1][0] + 10, gates[1][1]), 3)
        # pygame.draw.circle(screen, green, ball_coordinates, ball_radius)

        draw_cubic_curve(cubic_positions, t, screen, red, cubic_curve, green, blue, curve1, curve2, curve3,
                         robot_radius)

        if len(cubic_curve) > 2:
            # pygame.draw.lines(screen, (179, 179, 179), False, curve1, 3)
            # pygame.draw.lines(screen, (179, 179, 179), False, curve3, 3)
            # pygame.draw.lines(screen, (179, 179, 179), False, curve2, 3)
            pygame.draw.lines(screen, red, False, cubic_curve, 5)

        if t >= 1:
            t = 0
            end = True

        t += speed

    if end:
        pygame.draw.circle(screen, red, robot_final_coordinates.point(), robot_radius)
        linear_curve((ball_coordinates, gates_center), t, screen, green, True)

        if len(cubic_curve) > 2:
            pygame.draw.lines(screen, red, False, cubic_curve, 5)

        if t >= 1:
            t = 0
            cubic_curve.clear()
            curve1.clear()
            curve2.clear()
            curve3.clear()
            end = False

        t += speed

    pygame.display.update()

pygame.quit()
