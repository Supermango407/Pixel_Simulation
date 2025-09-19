#version 430

// The local_size_x directive specifies the number of work items in a local work group.
layout(local_size_x = 256) in;

layout(std430, binding = 0) buffer OutputBufferA {
    float dataOutR[];
};

layout(std430, binding = 1) buffer OutputBufferB {
    float dataOutG[];
};

layout(std430, binding = 2) buffer OutputBufferC {
    float dataOutB[];
};

layout(std430, binding = 3) buffer InputBufferA {
    float points_x[];
};

layout(std430, binding = 4) buffer InputBufferB {
    float points_y[];
};

layout(std430, binding = 5) buffer InputBufferC {
    float points_z[];
};

uniform int width;
uniform int height;
uniform float mouse_x;
uniform float mouse_y;
uniform uint frame;

void main() {
    uint index = gl_GlobalInvocationID.x;
    // coordanates of the pixel
    vec2 uv = vec2(float(index % width), float(floor(index / width)));
    // coordanates of the pixel from 0 to )1
    vec3 coords = vec3(uv/vec2(width, height), float(frame)/90);
    vec2 mouse = vec2(mouse_x/width, mouse_y/height);
    
    bool is_point = false;
    float point_z = 0.0;
    // the longest length in sqrt of 2 or 3 depending
    float shortest_length = 2;
    
    for (int i = 0; i < points_x.length(); ++i) {
        if (!is_point && abs(points_x[i]-coords.x) < 1/float(width) && abs(points_y[i]-coords.y) < 1/float(height) && abs(points_z[i]-coords.z) < 1) {
            is_point = true;
            point_z = points_z[i];
        }
        vec3 point = vec3(points_x[i], points_y[i], points_z[i]);
        float dist = abs(length(point-coords));
        if (dist < shortest_length) {
            shortest_length = dist;
        }
    }
    frame;
    shortest_length = clamp(0, 1, shortest_length*2);
    float val = pow(shortest_length, 0.5);
    if (is_point) {
        float fade = 
        dataOutR[index] = 1;
        dataOutG[index] = 0;
        dataOutB[index] = 0;
    } else {
        dataOutR[index] = val;
        dataOutG[index] = 1;
        dataOutB[index] = 1;
    }
}