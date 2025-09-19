import pygame
from PIL import Image
import moderngl
import numpy


width = 1024
height = 768
point_count = 64
pixel_count = width*height

window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

    
compute_shader_source = ""
with open('pygame_renderer.glsl', 'r') as file:
    compute_shader_source = file.read()

# create content
context = moderngl.create_standalone_context()

# Create input data using NumPy
rng = numpy.random.default_rng()
points_x = rng.random(size=point_count).astype('f4')
points_y = rng.random(size=point_count).astype('f4')
points_z = rng.random(size=point_count).astype('f4')

# Create buffers on the GPU and fill them with the input data
buffer_a = context.buffer(points_x.tobytes())
buffer_b = context.buffer(points_y.tobytes())
buffer_c = context.buffer(points_z.tobytes())

# create ouput buffers with size times four since float take up 4 bytes
output_buffer_r = context.buffer(reserve=pixel_count*4)
output_buffer_g = context.buffer(reserve=pixel_count*4)
output_buffer_b = context.buffer(reserve=pixel_count*4)

# bind buffers to glsl buffer indecies
output_buffer_r.bind_to_storage_buffer(0)
output_buffer_g.bind_to_storage_buffer(1)
output_buffer_b.bind_to_storage_buffer(2)
buffer_a.bind_to_storage_buffer(3)
buffer_b.bind_to_storage_buffer(4)
buffer_c.bind_to_storage_buffer(5)

# create the compute shader
compute_shader = context.compute_shader(compute_shader_source)
# set the uniform values
compute_shader['width'] = width
compute_shader['height'] = height
compute_shader['mouse_x'] = 0.0
compute_shader['mouse_y'] = 0.0
compute_shader['frame'] = 0


def get_image_from_shader():
    # set vars
    mouse_pos = pygame.mouse.get_pos()
    compute_shader['mouse_x'] = mouse_pos[0]
    compute_shader['mouse_y'] = mouse_pos[1]
    compute_shader['frame'] = frame

    # run the shader
    group_x = pixel_count // 256
    compute_shader.run(group_x)

    # get data from buffers
    result_data_r = numpy.frombuffer(output_buffer_r.read(), dtype=numpy.float32)
    result_data_g = numpy.frombuffer(output_buffer_g.read(), dtype=numpy.float32)
    result_data_b = numpy.frombuffer(output_buffer_b.read(), dtype=numpy.float32)
    # formate data
    result_data_r = (result_data_r*255).astype(numpy.uint8).reshape(height, width)
    result_data_g = (result_data_g*255).astype(numpy.uint8).reshape(height, width)
    result_data_b = (result_data_b*255).astype(numpy.uint8).reshape(height, width)
    rgb_image_array = numpy.stack((result_data_r, result_data_g, result_data_b), axis=2)
    rgb_image_array = rgb_image_array.astype(numpy.uint8)

    # create image
    image = Image.fromarray(rgb_image_array, "RGB")
    return image


def blit_shader():
    image = get_image_from_shader()
    image_data = image.tobytes()
    image_dimensions = image.size
    image_surface = pygame.image.fromstring(image_data, image_dimensions, 'RGB')
    # (Optional) Convert the Surface for optimal blitting
    image_surface = image_surface.convert()

    window.blit(image_surface, (0, 0))


frame = 0
if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Pygame Renderer")
    
    running = True
    while running:
        window.fill((255, 0, 255))
        blit_shader()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()
        frame += 1
        frame %= 90
        clock.tick(30)

    pygame.quit()
