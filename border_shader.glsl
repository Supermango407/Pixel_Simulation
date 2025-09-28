#version 430

// Set local workgroup size. The total number of workgroups will be calculated
// from the image size and these values.
layout (local_size_x = 32, local_size_y = 32, local_size_z = 1) in;

// `layout (binding = 0)` corresponds to `unit=0` in `texture.bind_to_image()`
layout (binding = 0, rgba32f) writeonly uniform image2D OutputImage;
layout (binding = 1, rgba32f) readonly uniform image2D PointsTexture;

uniform float time = 1;
uniform bool draw_dots = false;
uniform uint width = 256;
uniform uint height = 256;
uniform uint thickness = 2;
uniform vec3 background_color = vec3(1, 1, 1);
uniform vec3 border_color = vec3(0, 0, 0);

void swap_vec4(inout vec4 a, inout vec4 b) {
    vec4 temp = a;
    a = b;
    b = temp;
}

vec3 get_point_number(int i) {
    return vec3(imageLoad(PointsTexture, ivec2(i, 0)).xyz);
}

vec3 get_point_after_flip(vec3 coords, vec3 point) {
    // point too far left
    if (coords.x-point.x > 0.5) {
        point.x += 1;
    }
    // point too far right
    else if (coords.x-point.x < -0.5) {
        point.x -= 1;
    }

    // point too far down
    if (coords.y-point.y > 0.5) {
        point.y += 1;
    }
    // point too far right
    else if (coords.y-point.y < -0.5) {
        point.y -= 1;
    }

    // point too far in
    if (coords.z-point.z > 0.5) {
        point.z += 1;
    }
    // point too far out
    else if (coords.z-point.z < -0.5) {
        point.z -= 1;
    }
    return point;
}

float distance_to_point(vec3 coords, vec3 point) {
    return length(coords.xyz-get_point_after_flip(coords, point));
}

// first two values for point1 next two for point2
void get_two_nearsest_points(vec3 pos, inout vec4 point1, inout vec4 point2) {
    // first two values for position 3rd value for distance
    // set two be the first two points by default.
    point1 = vec4(get_point_number(0).xyz, 0.0);
    point2 = vec4(get_point_number(1).xyz, 0.0);
    // set distances
    point1 = vec4(point1.xyz, distance_to_point(pos, vec3(point1.xyz)));
    point2 = vec4(point2.xyz, distance_to_point(pos, vec3(point2.xyz)));
    
    // checking wh   eter to swap point1 and point2
    if (point1.w > point2.w) {
        swap_vec4(point1, point2);
    }

    for(int i = 2; i < imageSize(PointsTexture).x; i++) { 
        vec4 point_checking = vec4(get_point_number(i).xyz, 0.0);
        point_checking = vec4(point_checking.xyz, distance_to_point(pos, vec3(point_checking.xyz)));
        // if point_checking is closer than point2
        if (point_checking.w < point2.w) {
            // if point_checking is closer than both points
            // replace point2 with point1 and make point_checking, point1
            if (point_checking.w < point1.w) {
                point2 = point1;
                point1 = point_checking;
            // if point_checking is bigger than point2 but smaller than point1
            // make point_checking, point2 
            } else {
                point2 = point_checking;
            }
        }
    }
}

void get_three_nearsest_points(vec3 pos, inout vec4 point1, inout vec4 point2, inout vec4 point3) {
    // first two values for position 3rd value for distance
    // set two be the first two points by default.
    point1 = vec4(get_point_number(0).xyz, 0.0);
    point2 = vec4(get_point_number(1).xyz, 0.0);
    point3 = vec4(get_point_number(2).xyz, 0.0);
    // set distances
    point1 = vec4(point1.xyz, distance_to_point(pos, vec3(point1.xyz)));
    point2 = vec4(point2.xyz, distance_to_point(pos, vec3(point2.xyz)));
    point3 = vec4(point3.xyz, distance_to_point(pos, vec3(point3.xyz)));
    
    // checking wheter to swap point1 and point2
    if (point1.w > point2.w) {
        swap_vec4(point1, point2);
    }
    if (point2.w > point3.w) {
        swap_vec4(point2, point3);
    }
    if (point1.w > point2.w) {
        swap_vec4(point1, point2);
    }

    for(int i = 3; i < imageSize(PointsTexture).x; i++) { 
        vec4 point_checking = vec4(get_point_number(i).xyz, 0.0);
        point_checking = vec4(point_checking.xyz, distance_to_point(pos, vec3(point_checking.xyz)));
        // if point_checking is closer than point3
        if (point_checking.w < point3.w) {
            // if point_checking is closer than first two points
            // replace point2 with point1 and make point_checking, point1
            if (point_checking.w < point2.w) {
                // closer than all points
                if (point_checking.w < point1.w) {
                    point3 = point2;
                    point2 = point1;
                    point1 = point_checking;
                // closer the farthest two points but not the closest one
                } else {
                    point3 = point2;
                    point2 = point_checking;
                }
            // if point_checking is closer than point3 but smaller than point2
            // make point_checking, point2 
            } else {
                point3 = point_checking;
            }
        }
    }
}

void get_side_points(vec3 coords, vec3 point1, vec3 point2, inout vec3 side_point1, inout vec3 side_point2) {
    vec3 side_vec = normalize(get_point_after_flip(coords, point1)-get_point_after_flip(coords, point2))/width * thickness;
    // vec2 mid_point = (point1+point2)/2;
    
    // vec2 side_point1 = mid_point.xy + side_vec;
    // vec2 side_point2 = mid_point.xy - side_vec;
    
    side_point1 = side_vec+coords;
    side_point2 = -side_vec+coords;
}

bool is_border(vec3 coords) {
    vec4 point1 = vec4(0.0, 0.0, 0.0, 0.0);
    vec4 point2 = vec4(0.0, 0.0, 0.0, 0.0);
    vec4 point3 = vec4(0.0, 0.0, 0.0, 0.0);
    get_three_nearsest_points(coords, point1, point2, point3);

    vec3 side_point1 = vec3(0.0, 0.0, 0.0);
    vec3 side_point2 = vec3(0.0, 0.0, 0.0);
    get_side_points(coords, point1.xyz, point2.xyz, side_point1, side_point2);
    
    float diff = abs(distance_to_point(coords, point1.xyz)-distance_to_point(coords, point2.xyz));
    float side1_diff = abs(distance_to_point(side_point1, point1.xyz)-distance_to_point(side_point1, point2.xyz));
    float side2_diff = abs(distance_to_point(side_point2, point1.xyz)-distance_to_point(side_point2, point2.xyz));

    return diff<side1_diff && diff<side2_diff;
}

void main() {
    // `gl_GlobalInvocationID` gives the unique ID of the current thread (pixel)
    ivec2 global_id = ivec2(gl_GlobalInvocationID.xy);
    vec3 coords = vec3(global_id.xy, time)/vec3(width, height, 1);
    
    float dist_point = 1.0;
    for(int i = 0; i < imageSize(PointsTexture).x; i++) {
        vec3 point = get_point_number(i).xyz;
        if (length(vec2(coords).xy-vec2(point).xy) < 0.01) {
            float current_point_dist = 1-abs(abs(coords.z - point.z)-0.5)*2;
            dist_point = min(dist_point, current_point_dist);
        }
    }

    // vec3 point_checking = vec3(0.11, 0.61, 0.0);
    // vec4 point1_checking = vec4(0.0, 0.0, 0.0, 0.0);
    // vec4 point2_checking = vec4(0.0, 0.0, 0.0, 0.0);
    // vec4 point3_checking = vec4(0.0, 0.0, 0.0, 0.0);
    // get_three_nearsest_points(point_checking, point1_checking, point2_checking, point3_checking);
    
    // vec3 side_point1 = vec3(0.0, 0.0, 0.0);
    // vec3 side_point2 = vec3(0.0, 0.0, 0.0);
    // get_side_points(point_checking, point1_checking.xyz, point2_checking.xyz, side_point1, side_point2);

    // Write the result to the output image
    if (is_border(coords)) {
        imageStore(OutputImage, global_id, vec4(border_color.xyz, 1.0));
    // } else if (abs(point1.w-point2.w)<0.02 && abs(point1.w-point3.w)<0.02) {
    //     imageStore(OutputImage, global_id, vec4(0.0, 0.0, 1.0, 1.0));
    } else if (draw_dots && dist_point != 1) {
        imageStore(OutputImage, global_id, vec4(1.0, dist_point, dist_point, 1.0));
    // } else if (length(point_checking.xy-coords.xy) < 0.01) {
    //     imageStore(OutputImage, global_id, vec4(0.0, 1.0, 0.0, 1.0));
    // } else if (length(side_point1-coords) < 0.01 || length(side_point2-coords) < 0.01){
    //     imageStore(OutputImage, global_id, vec4(0.0, 1.0, 1.0, 1.0));
    } else {
        imageStore(OutputImage, global_id, vec4(background_color.xyz, 1.0));
        // imageStore(OutputImage, global_id, vec4(side_point2.xy, 1.0, 0.0));
        // imageStore(OutputImage, global_id, vec4(0.0353, 0.0196, 0.0392, 1.0));
        // imageStore(OutputImage, global_id, vec4(length(point1-coords)-length(point2-coords), length(point1-coords), length(point2-coords), 1.0));
        // imageStore(OutputImage, global_id, nearest_points);
    }
}