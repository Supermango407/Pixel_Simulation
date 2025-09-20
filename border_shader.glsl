#version 430

// Set local workgroup size. The total number of workgroups will be calculated
// from the image size and these values.
layout (local_size_x = 32, local_size_y = 32, local_size_z = 1) in;

// `layout (binding = 0)` corresponds to `unit=0` in `texture.bind_to_image()`
layout (binding = 0, rgba32f) writeonly uniform image2D OutputImage;
layout (binding = 1, rg32f) readonly uniform image2D PointsTexture;

void swap_vec3(inout vec3 a, inout vec3 b) {
    vec3 temp = a;
    a = b;
    b = temp;
}

vec2 get_point_number(int i) {
    return vec2(imageLoad(PointsTexture, ivec2(i, 0)).xy);
}

// first two values for point1 next two for point2
vec4 get_two_nearsest_points(vec2 pos) {
    // first two values for position 3rd value for distance
    // set two be the first two points by default.
    vec3 point1 = vec3(get_point_number(0).xy, 0.0);
    vec3 point2 = vec3(get_point_number(1).xy, 0.0);
    // set distances
    point1 = vec3(point1.xy, length(pos-vec2(point1.xy)));
    point2 = vec3(point2.xy, length(pos-vec2(point2.xy)));
    
    // checking wheter to swap point1 and point2
    if (point1.z > point2.z) {
        swap_vec3(point1, point2);
    }

    for(int i = 2; i < imageSize(PointsTexture).x; i++) { 
        vec3 point_checking = vec3(get_point_number(i), 0.0);
        point_checking = vec3(point_checking.xy, length(pos-vec2(point_checking.xy)));
        // if point_checking is closer than point2
        if (point_checking.z < point2.z) {
            // if point_checking is closer than both points
            // replace point2 with point1 and make point_checking, point1
            if (point_checking.z < point1.z) {
                point2 = point1;
                point1 = point_checking;
            // if point_checking is bigger than point2 but smaller than point1
            // make point_checking, point2 
            } else {
                point2 = point_checking;
            }
        }
    }
    
    return vec4(point1.xy, point2.xy);
}

void main() {
    // `gl_GlobalInvocationID` gives the unique ID of the current thread (pixel)
    ivec2 global_id = ivec2(gl_GlobalInvocationID.xy);
    vec2 coords = vec2(global_id)/vec2(1024,1024);
    
    bool near_point = false;
    for(int i = 0; i < imageSize(PointsTexture).x; i++) {
        vec2 point = get_point_number(i);
        if (length(coords-point) < 0.01) {
            near_point = true;
            break;
        }
    }

    // Read the value from the input image
    // float pixel_value = imageLoad(InputImage, global_id).r;


    // Write the result to the output image
    // vec2 point_checking = vec2(0.51, 0.31);
    vec4 nearest_points = get_two_nearsest_points(coords);
    vec2 point1 = nearest_points.xy;
    vec2 point2 = nearest_points.zw;
    if (near_point) {
        imageStore(OutputImage, global_id, vec4(1.0, 0.0, 0.0, 1.0));
    // } else if (length(point_checking-coords) < 0.01) {
    //     imageStore(OutputImage, global_id, vec4(0.0, 1.0, 0.0, 1.0));
    } else if (abs(length(point1-coords)-length(point2-coords))<0.004) {
        imageStore(OutputImage, global_id, vec4(0.0, 0.0, 0.0, 1.0));
    } else {
        imageStore(OutputImage, global_id, vec4(1.0, 1.0, 1.0, 1.0));
        // imageStore(OutputImage, global_id, vec4(length(point1-coords)-length(point2-coords), length(point1-coords), length(point2-coords), 1.0));
        // imageStore(OutputImage, global_id, nearest_points);
    }
}