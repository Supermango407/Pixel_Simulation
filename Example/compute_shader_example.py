import moderngl
import numpy as np

# --- Shader source code ---
# The GLSL compute shader will add corresponding elements from 'InputBufferA' and 'InputBufferB'
# and store the result in 'OutputBuffer'.
compute_shader_source = """
#version 430

// The local_size_x directive specifies the number of work items in a local work group.
layout(local_size_x = 256) in;

// Use a Shader Storage Buffer Object (SSBO) for the input and output buffers.
// The binding number links the buffer in the shader to the one in Python.
layout(std430, binding = 0) buffer InputBufferA {
    float dataA[];
};

layout(std430, binding = 1) buffer InputBufferB {
    float dataB[];
};

layout(std430, binding = 2) buffer OutputBuffer {
    float dataOut[];
};

void main() {
    // The gl_GlobalInvocationID is a unique ID for the current work item across the entire
    // compute shader execution.
    uint index = gl_GlobalInvocationID.x;
    dataOut[index] = dataA[index] + dataB[index];
}
"""

def run_compute_shader_example():
    # --- ModernGL setup ---
    # Create a headless context, which doesn't require a window.
    ctx = moderngl.create_standalone_context()

    # --- Data and buffer setup ---
    size = 1024  # Total number of floats to process
    
    # Create input data using NumPy
    input_data_a = np.random.rand(size).astype('f4')
    input_data_b = np.random.rand(size).astype('f4')
    
    # Create buffers on the GPU and fill them with the input data
    buffer_a = ctx.buffer(input_data_a.tobytes())
    buffer_b = ctx.buffer(input_data_b.tobytes())
    
    # Create an empty output buffer to receive the result from the shader
    output_buffer = ctx.buffer(reserve=size * 4) # 4 bytes per float

    # --- Bind buffers to the shader storage blocks ---
    buffer_a.bind_to_storage_buffer(0) # Binding point 0
    buffer_b.bind_to_storage_buffer(1) # Binding point 1
    output_buffer.bind_to_storage_buffer(2) # Binding point 2

    # --- Create and run the compute shader ---
    compute_shader = ctx.compute_shader(compute_shader_source)
    
    # Run the shader, specifying the number of work groups.
    # The total number of work items launched is `group_x * local_size_x`.
    # `size // 256` gives us the number of groups needed to process all elements.
    group_x = size // 256
    compute_shader.run(group_x)

    # --- Read the results ---
    # Read the data from the output buffer back into a NumPy array.
    result_data = np.frombuffer(output_buffer.read(), dtype='f4')

    # --- Verification ---
    # Compare the GPU result with a CPU-calculated result.
    expected_result = input_data_a + input_data_b
    if np.allclose(result_data, expected_result):
        print("Compute shader execution successful! Results match CPU calculation.")
        print(result_data[:5])
    else:
        print("Error: Compute shader results do not match CPU calculation.")
        print("Expected:", expected_result[:5])
        print("Got:", result_data[:5])

if __name__ == '__main__':
    run_compute_shader_example()
