#version 430

// Set local workgroup size. The total number of workgroups will be calculated
// from the image size and these values.
layout (local_size_x = 4, local_size_y = 4, local_size_z = 1) in;

// `layout (binding = 0)` corresponds to `unit=0` in `texture.bind_to_image()`
layout (binding = 0, rgba32f) writeonly uniform image2D OutputImage;
layout (binding = 1, r32f) readonly uniform image2D InputImage;

void main() {
    // `gl_GlobalInvocationID` gives the unique ID of the current thread (pixel)
    ivec2 global_id = ivec2(gl_GlobalInvocationID.xy);

    // Read the value from the input image
    float pixel_value = imageLoad(InputImage, global_id).r;

    // Write the result to the output image
    imageStore(OutputImage, global_id, vec4(pixel_value, 0.0, 0.0, 1.0));
}