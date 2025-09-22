import moderngl
import numpy
from PIL import Image
import math

def get_clostest_dist(points:numpy.array) -> float:
    nearest = math.inf
    for i, point1 in enumerate(points):
        for j, point2 in enumerate(points):
            if j == i:
                continue
            dist = numpy.linalg.norm(point1-point2)
            if dist < nearest:
                nearest = dist
    return nearest

# get compute shader code
compute_shader_source = ""
with open('border_shader.glsl', 'r') as file:
    compute_shader_source = file.read()


point_number = 32
width, height = 1024, 1024
thickness = 2
frames_per_second = 30
total_seconds = 5

# total_frames = 1
total_frames = frames_per_second*total_seconds

# seed = 0
# farthest_dist = 0
# for i in range(1000):
#     rng = numpy.random.default_rng(i)
#     points_data = rng.random((1, point_number, 2))
#     dist = get_clostest_dist(points_data[0])
#     if dist > farthest_dist:
#         farthest_dist = dist
#         seed = i

if total_frames > 1:
    rng = numpy.random.default_rng(91)
    points_data = rng.random((1, point_number, 3))
    points_data = numpy.concatenate((points_data, numpy.zeros((1, point_number, 1))), axis=2)
else:
    # rng = numpy.random.default_rng(87) # for 8 points
    # rng = numpy.random.default_rng(372) # for 16 points
    rng = numpy.random.default_rng(679) # for 32 points
    # rng = numpy.random.default_rng(0)
    points_data = rng.random((1, point_number, 2))
    points_data = numpy.concatenate((points_data, numpy.zeros((1, point_number, 2))), axis=2)

# with open('border_pygame.py', 'w') as file:
#     for point in points_data[0].tolist():
#         print(point[:2], file=file)

# points_data = numpy.array([[
#     [0.5, 0.8, 0.0, 0.0],
#     [0.6, 0.3, 0.0, 0.0],
#     [0.2, 0.9, 0.0, 0.0],
#     [0.4, 0.2, 0.0, 0.0],
#     [0.1, 0.4, 0.0, 0.0],
#     [0.9, 0.1, 0.0, 0.0],
#     [0.8, 0.8, 0.0, 0.0],
#     [0.4, 0.5, 0.0, 0.0]
# ]], dtype='f4') # 'f4' is for 32-bit float

# points_data = numpy.array([[
#     [0.5, 0.8, 0.4, 0.0],
#     [0.6, 0.3, 0.8, 0.0],
#     [0.2, 0.9, 0.1, 0.0],
#     [0.4, 0.2, 0.3, 0.0],
#     [0.1, 0.4, 0.7, 0.0],
#     [0.9, 0.1, 0.2, 0.0],
#     [0.8, 0.8, 0.6, 0.0],
#     [0.4, 0.5, 0.0, 0.0]
# ]], dtype='f4') # 'f4' is for 32-bit float

# 1. Initialize ModernGL context
# This example uses a headless context. For a windowed app,
# you would get the context from a library like moderngl-window.
context = moderngl.create_standalone_context(require=430)

# 2. Create the input texture from the numpy array
# The format 'r32f' is for a single 32-bit float channel, perfect for grayscale.
points_texture = context.texture(
    (point_number, 1),
    components=4,
    data=points_data.astype('f4').tobytes(),
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
compute_shader['width'] = width
compute_shader['height'] = height
compute_shader['thickness'] = thickness

# Bind the textures to their respective image units
# Output image is write-only (read=False, write=True)
output_texture.bind_to_image(unit=0, read=False, write=True)
# # Input image is read-only (read=True, write=False)
points_texture.bind_to_image(unit=1, read=True, write=False)

# 6. Run the compute shader
# `group_x` and `group_y` are the number of workgroups to dispatch.
# We divide the total dimensions by the local workgroup size (4x4)
group_x = width // 32
group_y = height // 32

frames:list[Image.Image] = []
for i in range(total_frames):
    print(i/total_frames)
    compute_shader['time'] = i/total_frames
    compute_shader.run(group_x=group_x, group_y=group_y)

    # 7. Read the output texture data back to a numpy array
    output_data = numpy.frombuffer(output_texture.read(), dtype='f4').reshape(height, width, 4)
    print(output_data[0][0])
    print()
    output_data = numpy.delete(output_data, 3, axis=2)
    output_data = numpy.flip(output_data, axis=0)

    # Print the results
    # print("Input array:")
    # print(input_data)
    # print("\nOutput array:")
    # print(output_data)

    rgb_image_array = (output_data*255).astype(numpy.uint8)
    # print(rgb_image_array)

    # create image
    image = Image.fromarray(rgb_image_array, "RGB")
    frames.append(image)

# save image
if total_frames > 1:
    frames[0].save("border.gif", save_all=True, append_images=frames[1:], optimize=False, duration=1000/frames_per_second,loop=0)
else:
    frames[0].save("border.png")
 
# Optional: Release resources
context.release()
output_texture.release()
points_texture.release()
