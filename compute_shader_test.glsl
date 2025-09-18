#version 430

// The local_size_x directive specifies the number of work items in a local work group.
layout(local_size_x = 256) in;

// Use a Shader Storage Buffer Object (SSBO) for the input and output buffers.
// The binding number links the buffer in the shader to the one in Python.
// layout(std430, binding = 0) buffer InputBufferA {
//     float dataA[];
// };

// layout(std430, binding = 1) buffer InputBufferB {
//     float dataB[];
// };

// layout(std430, binding = 2) buffer InputBufferC {
//     float dataC[];
// };


layout(std430, binding = 0) buffer OutputBufferA {
    float dataOutR[];
};

layout(std430, binding = 1) buffer OutputBufferB {
    float dataOutG[];
};

layout(std430, binding = 2) buffer OutputBufferC {
    float dataOutB[];
};

uniform float val;

void main() {
    // The gl_GlobalInvocationID is a unique ID for the current work item across the entire
    // compute shader execution.
    uint index = gl_GlobalInvocationID.x;
    vec2 coord = vec2(float(index % 32), float(floor(index / 32)));
    dataOutR[index] = val;
    dataOutG[index] = val;
    dataOutB[index] = val;
}