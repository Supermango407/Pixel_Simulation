import pygame
import timeit
import random
import math
from main import PixelRenderer, get_time
from pixel_help import border


# class FractalPoint():
#     def __init__(self, position: pygame.Vector3, cell: pygame.Vector3) -> None:
#         self.position = position
#         self.cell = cell


def fractal_draw(x, y, time):
    shade = randomizer.random()
    distances = [1]
    # divisions = window_size//cell_divisions
    close_points = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            for k in range(-1, 2):
                cell_in = (int(i+x//cell_size), int(j+y//cell_size), int(k+time//cell_size))
                point_in_box = points[cell_in[0]%cell_count][cell_in[1]%cell_count][cell_in[2]%cell_count]
                relative_position = (point_in_box[0]+cell_in[0]*cell_size, point_in_box[1]+cell_in[1]*cell_size, point_in_box[2]+cell_in[2]*cell_size)
                close_points.append(relative_position)

    # print(f"\t{(x//cell_count, y//cell_count)}\n{keys}")
    for point in close_points:
        # print((x, y, time), key, end=' ')
        # print()
        # print(point)
        # distances.append(point.distance_to([x, y, time]))
        # distances.append(math.sqrt((point[0] - x)**2 + (point[1] - y)**2)/window_size)
        distances.append(math.sqrt((point[0] - x)**2 + (point[1] - y)**2 + (point[2] - time)**2)/cell_size)

    shade = min(distances)
    # print(shade)
    # shade = 1

    # if (x, y) in points:
    #     shade = 1
    # else:
    #     shade = 0

    # return (255*int(points[keys[0]].x/window_size), 255*int(points[keys[0]].y/window_size), 255*int(points[keys[0]].z/window_size))
    return 0.5, shade, 1


def fractal_outline_draw(x, y, time):
    return border(x, y, time, fractal_draw)


def start():
    pass
    # time = timeit.timeit(renderer.update, number=1)
    # print(1/time)

    # setup="from __main__ import fractal_draw"
    # code = lambda: {fractal_draw(1, 1, 0)}

    # time = timeit.timeit(code, setup=setup, number=26215)*10
    # # time_aiming = 1/get_time()
    # time_aiming = 12

    # print(f"time:{time:.4f}\tratio:{time_aiming/(1/time):.4f}")


def update():
    global last_frame_time
    # delta_time = (pygame.time.get_ticks() - last_frame_time)/1000
    # print(f"Time: {last_frame_time},\tDelta Time: {delta_time:.4f},\tFrame Rate: {1/delta_time:.4f}")
    # last_frame_time = pygame.time.get_ticks()
    
    renderer.update((pygame.time.get_ticks()/1000)%window_size)
    check_events()
    pygame.display.update()


def check_events():
    global run
    global points

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     mouse_position = pygame.mouse.get_pos()
        #     if event.button == 1:
        #         points = []
        #         for i in range(cell_count):
        #             row = []
        #             for j in range(cell_count):
        #                 # for k in range(cell_count):
        #                     row.append((
        #                         10000, 10000
        #                         # randomizer.random()*cell_size,
        #                         # randomizer.random()*cell_size
        #                     ))
        #             points.append(row)

        #         cell_in = ((mouse_position[0]//(cell_size*pixel_size))%cell_count, (mouse_position[1]//(cell_size*pixel_size))%cell_count)
        #         value = (mouse_position[0]/pixel_size-cell_in[0]*cell_size, mouse_position[1]/pixel_size-cell_in[1]*cell_size)
        #         print(mouse_position)
        #         print(value)
        #         points[cell_in[0]][cell_in[1]] = value


if __name__ == '__main__':
    window = pygame.display.set_mode((1000, 800), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    randomizer = random.Random(2)

    cell_size = 6
    cell_count = 4

    window_size = cell_size*cell_count
    pixel_size = 512//window_size

    renderer = PixelRenderer(window, window_size, window_size, fractal_draw, pixel_size=pixel_size)
    last_frame_time = 0

    points = []
    for i in range(cell_count):
        plane = []
        for j in range(cell_count):
            row = []
            for k in range(cell_count):
                row.append((
                    # 0, 0
                    randomizer.random()*cell_size,
                    randomizer.random()*cell_size,
                    randomizer.random()*cell_size
                ))
            plane.append(row)
        points.append(plane)

    # points[0][0][0] = (0, 0, 0)
                # print(points[(i, j, k)])


    pygame.init()
    pygame.display.set_caption("Pixel Fractal Simulation")

    start()
    # main loop
    run = True
    while run:
        clock.tick(12)
        update()

    pygame.quit()
