import moderngl
import numpy
from PIL import Image

# get compute shader code
compute_shader_source = ""
with open('compute_shader_main.glsl', 'r') as file:
    compute_shader_source = file.read()

# A grayscale 2D array (e.g., an image)
# Example input: a simple 4x4 array
input_data = numpy.array([
    [0.1, 0.2, 0.3, 0.4],
    [0.5, 0.6, 0.7, 0.8],
    [0.9, 0.8, 0.7, 0.6],
    [0.5, 0.4, 0.3, 0.2]
], dtype='f4') # 'f4' is for 32-bit float

width, height = input_data.shape

# 1. Initialize ModernGL context
# This example uses a headless context. For a windowed app,
# you would get the context from a library like moderngl-window.
context = moderngl.create_standalone_context(require=430)

# 2. Create the input texture from the numpy array
# The format 'r32f' is for a single 32-bit float channel, perfect for grayscale.
input_texture = context.texture(
    (width, height),
    components=1,
    data=input_data.tobytes(),
    dtype='f4',
)

# 3. Create the output texture
# The output texture should have the same dimensions and format.
output_texture = context.texture(
    (width, height),
    components=4,
    data=None, # No initial data
    dtype='f4',
)

# 5. Create a ComputeShader object and bind textures
compute_shader = context.compute_shader(compute_shader_source)

# Bind the textures to their respective image units
# Output image is write-only (read=False, write=True)
output_texture.bind_to_image(unit=0, read=False, write=True)
# # Input image is read-only (read=True, write=False)
input_texture.bind_to_image(unit=1, read=True, write=False)

# 6. Run the compute shader
# `group_x` and `group_y` are the number of workgroups to dispatch.
# We divide the total dimensions by the local workgroup size (4x4)
group_x = width // 4
group_y = height // 4
compute_shader.run(group_x=group_x, group_y=group_y)

# 7. Read the output texture data back to a numpy array
output_data = numpy.frombuffer(output_texture.read(), dtype='f4').reshape(height, width, 4)
output_data = numpy.delete(output_data, 3, axis=2)

# Print the results
# print("Input array:")
# print(input_data)
print("\nOutput array:")
print(output_data)

rgb_image_array = (output_data*255).astype(numpy.uint8)

# create image
image = Image.fromarray(rgb_image_array, "RGB")
# save image
image.save("compute_shader_main_output.png")
 
# Optional: Release resources
context.release()
output_texture.release()
input_texture.release()
