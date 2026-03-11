from __future__ import annotations
import pygame
from pygame import Vector2
import random
import moderngl
import numpy


pygame.init()
point_size = 4
width, height = (512, 512)
image = None

window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

compute_shader_source = ""
with open('border_shader.glsl', 'r') as file:
    compute_shader_source = file.read()

context = moderngl.create_standalone_context(require=430)
compute_shader = context.compute_shader(compute_shader_source)
compute_shader['width'] = width
compute_shader['height'] = height
# compute_shader['background_color'] = (1, 0, 0)

output_texture = context.texture(
    (width, height),
    components=4,
    data=None, # No initial data
    dtype='f4',
)
output_texture.bind_to_image(unit=0, read=False, write=True)
group_x = width // 32
group_y = height // 32


class Point():
    points:list[Point] = []
    point_selected:Point = None
    point_dragging:Point = None

    [staticmethod]
    def mouse_down():
        if Point.point_selected:
            Point.point_dragging = Point.point_selected

    [staticmethod]
    def mouse_up():
        if Point.point_selected:
            Point.point_dragging = None

    [staticmethod]
    def get_nearest_points(position:Vector2, amount:int) -> list[Point]:
        if amount <= 0:
            return []
        
        # points and distances from farthest to closest
        points_near = []
        distances = []
        
        for i, point in enumerate(Point.points):
            dist = (point.position-position).length()
            # if the first point add it and continue
            if i == 0:
                points_near.append(point)
                distances.append(dist)
                continue
            
            index = 0
            for point_dist in distances:
                if dist < point_dist:
                    index += 1
                else:
                    break

            points_near.insert(index, point)
            distances.insert(index, dist)
            if len(distances) > amount:
                points_near.pop(0)
                distances.pop(0)

        return points_near

    def __init__(self, position:Vector2):
        self.position:Vector2 = position
        Point.points.append(self)
    
    def update(self):
        if Point.point_dragging is self:
            self.position = mouse_pos
        # color should be green if mouse is over, blue if touching point_selected, and red otherwise.
        if Point.point_selected is self:
            color = (0, 255, 0) 
        elif self.touching_point():
            color = (0, 0, 255)
        else:
            color = (255, 0, 0)
        pygame.draw.circle(window, color, self.position, point_size)

    def touching_point(self) -> bool:
        if Point.point_selected == None:
            return False
        
        if self in Point.get_nearest_points((Point.point_selected.position+self.position)/2, 2):
            return True
        else:
            return False


def create_default_points():
    rng = random.Random(0)
    for i in range(32):
        Point(Vector2(rng.random()*width, rng.random()*height))


def draw_border():
    global image

    points_list = [[]]
    for point in Point.points:
        points_list[0].append([point.position.y/height, -point.position.x/width])

    points_data = numpy.concatenate((numpy.array(points_list), numpy.ones((1, len(Point.points), 2))), axis=2)
    points_texture = context.texture(
        (len(Point.points), 1),
        components=4,
        data=points_data.astype('f4').tobytes(),
        dtype='f4',
    )
    points_texture.bind_to_image(unit=1, read=True, write=False)
    compute_shader.run(group_x=group_x, group_y=group_y)
    
    output_data = numpy.frombuffer(output_texture.read(), dtype='f4').reshape(height, width, 4)
    output_data = numpy.delete(output_data, 3, axis=2)
    output_data = numpy.flip(output_data, axis=0)
    rgb_image_array = (output_data*255).astype(numpy.uint8)
    image = pygame.surfarray.make_surface(rgb_image_array)
    # image = pygame.surfarray.make_surface(numpy.tile(numpy.array([255, 255, 255]), (768, 768, 1)))


create_default_points()
# near_points = Point.get_nearest_points(Vector2(100, 150), 2)
# for point in near_points:
#     print((point.position-Vector2(100, 150)).length())

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Pygame Renderer")

    frame_on = 0
    running = True
    while running:
        if frame_on % 2 == 0:
            window.fill((255, 0, 255))
            draw_border()
        window.blit(image, (0, 0))

        mouse_pos = Vector2(pygame.mouse.get_pos())
        
        # set `Point` hover_point
        for point in Point.points:
            Point.point_selected = None
            if (point.position-mouse_pos).length()<point_size:
                Point.point_selected = point
                break

        for point in Point.points:
            point.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Point.mouse_down()
            elif event.type == pygame.MOUSEBUTTONUP:
                Point.mouse_up()
        
        frame_on += 1
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
