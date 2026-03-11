import random
import math
from Pygame.main import ImageRenderer
# import pixel_help
# from pixel_help import border


# def fractal_draw(x, y, time):
#     shade = randomizer.random()
#     distances = [1]
#     # divisions = window_size//cell_divisions
#     close_points = []

#     # for i in range(cell_count[0]):
#     #     for j in range(cell_count[1]):
#     #         for k in range(cell_count[2]):
#                 # cell_in = (int(i+x//cell_size[0]), int(j+y//cell_size[1]), int(k+time//(cell_size[2])))
                
#                 # point_in_box = points[cell_in[0]%cell_count[0]][cell_in[1]%cell_count[1]][cell_in[2]%cell_count[2]]
#                 # relative_position = (point_in_box[0]+cell_in[0]*cell_size[0], point_in_box[1]+cell_in[1]*cell_size[1], point_in_box[2]+cell_in[2]*cell_size[2])
#                 # close_points.append(relative_position)

#     for i in range(-1, 2):
#         for j in range(-1, 2):
#             for k in range(-1, 2):
#                 cell_in = (int(i+x//cell_size[0]), int(j+y//cell_size[1]), int(k+time//(cell_size[2])))
                
#                 point_in_box = points[cell_in[0]%cell_count[0]][cell_in[1]%cell_count[1]][cell_in[2]%cell_count[2]]
#                 relative_position = (point_in_box[0]+cell_in[0]*cell_size[0], point_in_box[1]+cell_in[1]*cell_size[1], point_in_box[2]+cell_in[2]*cell_size[2])
#                 close_points.append(relative_position)

#     # print(f"\t{(x//cell_count, y//cell_count)}\n{keys}")
#     for point in close_points:
#         # print((x, y, time), key, end=' ')
#         # print()
#         # print(point)
#         # distances.append(point.distance_to([x, y, time]))
#         # distances.append(math.sqrt((point[0] - x)**2 + (point[1] - y)**2)/window_size)
#         # print(math.sqrt(((point[0] - x))**2 + ((point[1] - y))**2 + ((point[2] - time))**2)/color_divider)
#         distances.append(math.sqrt(((point[0] - x))**2 + ((point[1] - y))**2 + ((point[2] - time))**2)/color_divider)

#     shade = min(distances)+0.1
#     # print(shade)
#     # shade = 1

#     # if (x, y) in points:
#     #     shade = 1
#     # else:
#     #     shade = 0

#     # return (255*int(points[keys[0]].x/window_size), 255*int(points[keys[0]].y/window_size), 255*int(points[keys[0]].z/window_size))
#     return shade*0.5, shade, 1


# def fractal_outline_draw(x, y, time):
#     return border(x, y, time, fractal_draw)


def points_in_adjacent_cells_2D(cell_list, x, y):
    cells = []
    width = cell_count[0]
    height = cell_count[1]

    for i in range(-1, 2):
        for j in range(-1, 2):
            cell_in = (x+i), (y+j)
            cells_origin = cell_in[0]*cell_size[0], cell_in[1]*cell_size[1]
            point_in_cell = cell_list[cell_in[0]%width][cell_in[1]%height]

            for point in point_in_cell:
                cells.append((cells_origin[0]+point[0], cells_origin[1]+point[1]))
    
    return cells

 
def points_in_adjacent_cells_3D(cell_list, x, y, z):
    cells = []
    width = cell_count[0]
    height = cell_count[1]
    depth = cell_count[2]

    for i in range(-1, 2):
        for j in range(-1, 2):
            for k in range(-1, 2):
                cell_in = (x+i), (y+j), (z+k)
                cells_origin = cell_in[0]*cell_size[0], cell_in[1]*cell_size[1], cell_in[2]*cell_size[2]
                point_in_cell = cell_list[cell_in[0]%width][cell_in[1]%height][cell_in[2]%depth]

                for point in point_in_cell:
                    cells.append((cells_origin[0]+point[0], cells_origin[1]+point[1], cells_origin[2]+point[2]))
    
    return cells


def distance_bettween_2D(vector_1, vector_2):
    return math.sqrt((vector_1[0]-vector_2[0])**2 + (vector_1[1]-vector_2[1])**2)


def distance_bettween_3D(vector_1, vector_2):
    return math.sqrt((vector_1[0]-vector_2[0])**2 + (vector_1[1]-vector_2[1])**2 + (vector_1[2]-vector_2[2])**2)


def distances_to_nearest_2_points_2D(points, x, y):
    closest_points = []

    for point in points:
        distance = distance_bettween_2D((x, y), point)
        
        if len(closest_points) < 1:
            closest_points.append({"dist": distance, "pos": point})
        elif len(closest_points) < 2:
            if distance <= closest_points[0]["dist"]:
                closest_points.insert(0, {"dist": distance, "pos": point})
            else:
                closest_points.append({"dist": distance, "pos": point})
        elif distance <= closest_points[1]["dist"]:
            if distance <= closest_points[0]["dist"]:
                closest_points.insert(0, {"dist": distance, "pos": point})
            else:
                closest_points.insert(1, {"dist": distance, "pos": point})
            del closest_points[-1]
    
    return closest_points[0]['dist'], closest_points[1]['dist']


def distances_to_nearest_2_points_3D(points, x, y, time):
    closest_points = []

    for point in points:
        distance = distance_bettween_3D((x, y, time), point)
        
        if len(closest_points) < 1:
            closest_points.append({"dist": distance, "pos": point})
        elif len(closest_points) < 2:
            if distance <= closest_points[0]["dist"]:
                closest_points.insert(0, {"dist": distance, "pos": point})
            else:
                closest_points.append({"dist": distance, "pos": point})
        elif distance <= closest_points[1]["dist"]:
            if distance <= closest_points[0]["dist"]:
                closest_points.insert(0, {"dist": distance, "pos": point})
            else:
                closest_points.insert(1, {"dist": distance, "pos": point})
            del closest_points[-1]
    
    return closest_points[0]['dist'], closest_points[1]['dist']


def border_2D(x, y, _):
    points = points_in_adjacent_cells_2D(point_list, x//cell_size[0], y//cell_size[1])

    if (x, y) in points:
        return 1, 0, 0
    
    # if x % cell_size[0] == 0 or y % cell_size[1] == 0:
    #     return 0, 1, 1
    
    distances = distances_to_nearest_2_points_2D(points, x, y)
    if abs(distances[0] - distances[1]) < 1:
        return 0, 0, 1
    return 1, 1, 1


def border_3D(x, y, time):
    points = points_in_adjacent_cells_3D(point_list, x//cell_size[0], y//cell_size[1], time//cell_size[2])

    # if (x, y, time) in points:
    #     return 1, 0, 0
    
    # if x % cell_size[0] == 0 or y % cell_size[1] == 0:
    #     return 0, 1, 1
    
    distances = distances_to_nearest_2_points_3D(points, x, y, time)
    if abs(distances[0] - distances[1]) < 1:
        return 0, 0, 1
    return 1, 1, 1


if __name__ == '__main__':
    cell_size = [32, 32, 32]
    cell_count = [16, 12, 8]
    points_in_box = 1

    window_size = [
        cell_size[0]*cell_count[0],
        cell_size[1]*cell_count[1],
        cell_size[2]*cell_count[2],
    ]

    randomizer = random.Random(1)
    point_list = []
    for i in range(cell_count[0]):
        rows = []
        for j in range(cell_count[1]):
            row = []
            for k in range(cell_count[2]):
                cell = []
                for _ in range(points_in_box):
                    cell.append((
                        randomizer.randint(0, cell_size[0]-1),
                        randomizer.randint(0, cell_size[1]-1),
                        randomizer.randint(0, cell_size[2]-1)
                    ))
                row.append(cell)
            rows.append(row)
        point_list.append(rows)

    # points.append((
    #     randomizer.randint(0, 31),
    #     randomizer.randint(0, 31)
    # ))
    # points.append((
    #     randomizer.randint(32, 63),
    #     randomizer.randint(0, 31)
    # ))
    # points.append((
    #     randomizer.randint(0, 31),
    #     randomizer.randint(32, 63)
    # ))
    # points.append((
    #     randomizer.randint(32, 63),
    #     randomizer.randint(32, 63)
    # ))

    # points = pixel_help.adjacent_cells_2D(point_rows, 0, 3)
    
    renderer = ImageRenderer(window_size[0], window_size[1], border_3D, window_size[2], 16)
    renderer.generate()
    # renderer.save_images('border_3D_3', 'gif_outputs/')
    renderer.images[0].show()

    # for i in range(cell_count[0]):
    #     plane = []
    #     for j in range(cell_count[1]):
    #         row = []
    #         for k in range(cell_count[2]):
    #             row.append((
    #                 # 0, 0, 0
    #                 i, j, k
    #                 # randomizer.random()*cell_size[0],
    #                 # randomizer.random()*cell_size[1],
    #                 # randomizer.random()*cell_size[2]
    #             ))
    #         plane.append(row)
    #     points.append(plane)

    # color_divider = (cell_size[0]+cell_size[1]+cell_size[2])/3

    # renderer = ImageRenderer(window_size[0], window_size[1], fractal_outline_draw, window_size[2], 16)
    # renderer.generate()
    # renderer.save_images('Fractal_17', 'gif_outputs/')
    # renderer.images[0].show()
