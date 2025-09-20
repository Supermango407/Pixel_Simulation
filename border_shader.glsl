#version 430

// Set local workgroup size. The total number of workgroups will be calculated
// from the image size and these values.
layout (local_size_x = 32, local_size_y = 32, local_size_z = 1) in;

// `layout (binding = 0)` corresponds to `unit=0` in `texture.bind_to_image()`
layout (binding = 0, rgba32f) writeonly uniform image2D OutputImage;
layout (binding = 1, rg32f) readonly uniform image2D PointsTexture;

void main() {
    // `gl_GlobalInvocationID` gives the unique ID of the current thread (pixel)
    ivec2 global_id = ivec2(gl_GlobalInvocationID.xy);
    vec2 coords = vec2(global_id)/vec2(255,255);
    
    bool near_point = false;
    for(int i = 0; i < imageSize(PointsTexture).x; i++) {
        vec2 point = vec2(imageLoad(PointsTexture, ivec2(i, 0)).xy);
        if (length(coords-point) < 0.01) {
            near_point = true;
            break;
        }
    }

    // Read the value from the input image
    // float pixel_value = imageLoad(InputImage, global_id).r;


    // Write the result to the output image
    if (near_point) {
        imageStore(OutputImage, global_id, vec4(1.0, 0.0, 0.0, 1.0));
    } else {
        imageStore(OutputImage, global_id, vec4(1.0, 1.0, 1.0, 1.0));
    }
}