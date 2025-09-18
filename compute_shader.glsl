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

uniform int width;
uniform int height;

void main() {
    uint index = gl_GlobalInvocationID.x;
    // coordanates of the pixel
    vec2 uv = vec2(float(index % width), float(floor(index / width)));
    // coordanates of the pixel from 0 to 1
    vec2 dec_uv = uv/vec2(width, height);
    // coordanates of the pixel from -1 to 1
    vec2 coords = (dec_uv-0.5)*2;

    float val = length(coords);
    val = sin(val*8.)/8.;
    val = abs(val);
    val = 0.02/val;

    val = min(max(val, 0), 1);
    dataOutR[index] = val;
    dataOutG[index] = val;
    dataOutB[index] = val;
}