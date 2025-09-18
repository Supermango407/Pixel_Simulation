import moderngl
import numpy
from PIL import Image


# set dementions of picture
width = 128
height = 96
size = width*height

# get compute shader code
compute_shader_source = ""
with open('compute_shader_main.glsl', 'r') as file:
    compute_shader_source = file.read()

# create content
context = moderngl.create_standalone_context()

# create ouput buffers with size times four since float take up 4 bytes
output_buffer_r = context.buffer(reserve=size*4)
output_buffer_g = context.buffer(reserve=size*4)
output_buffer_b = context.buffer(reserve=size*4)

# bind buffers to glsl buffer indecies
output_buffer_r.bind_to_storage_buffer(0)
output_buffer_g.bind_to_storage_buffer(1)
output_buffer_b.bind_to_storage_buffer(2)

# create the compute shader
compute_shader = context.compute_shader(compute_shader_source)
# set the uniform values
compute_shader['width'] = width
compute_shader['height'] = height

# run the shader
group_x = size // 256
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
# save image
image.save("compute_shader_main_output.png")
 