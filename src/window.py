import glfw
import numpy as np
import pyrr
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

import logger as lg

def get_shaders(logger):
    # Load shaders.
    with open("src/shaders/vertex_shader.glsl", "r") as file:
        vertex_src = file.read()
    logger.log("Loaded vertex shader source.")
    
    with open("src/shaders/fragment_shader.glsl", "r") as file:
        fragment_src = file.read()
    logger.log("Loaded fragment shader source.")
    
    # Return source.
    return vertex_src, fragment_src

def main():
    # Initialize logger.
    logger = lg.Logger()
    
    # Initialize glfw.
    if not glfw.init():
        raise Exception("GLFW could not be initialized.")
    
    # Create window.
    window = glfw.create_window(1920, 1080, "Window Title", None, None)
    
    # Check if the window was created.
    if not window:
        glfw.terminate()
        raise Exception("GLFW window could not be created.")
    
    # Load shaders.
    vertex_src, fragment_src = get_shaders(logger)
    
    # Make context current.
    glfw.make_context_current(window)
    
    # Enable vsync.
    glfw.swap_interval(1)
    logger.log("Enabled vsync.")
    
    # Set window position.
    glfw.set_window_pos(window, (3840 - 1920) // 2, (2160 - 1080) // 2)
    
    # Triangle
    """# Vertex data.
    vertex_data = np.array([
        -0.5, -0.5, 0.0,
         0.5, -0.5, 0.0,
         0.0,  0.5, 0.0,
         1.0,  0.0, 0.0,
         0.0,  1.0, 0.0,
         0.0,  0.0, 1.0,
    ], dtype=np.float32)
    
    # Index data.
    index_data = np.array([
        0, 1, 2
    ], dtype=np.uint32)"""
    
    # Quad
    """vertex_data = np.array([
        -0.5,  0.5, 0.0,
        -0.5, -0.5, 0.0,
         0.5, -0.5, 0.0,
         0.5,  0.5, 0.0,
         0.0,  0.0, 1.0,
         1.0,  0.0, 0.0,
         0.0,  1.0, 0.0,
         1.0,  1.0, 1.0
    ], dtype=np.float32)
    
    index_data = np.array([
        0, 1, 2,
        2, 3, 0
    ], dtype=np.uint32)"""
    
    # Cube
    vertex_data = np.array([
        -0.5, -0.5,  0.5,
         0.5, -0.5,  0.5,
         0.5,  0.5,  0.5,
        -0.5,  0.5,  0.5,
        -0.5, -0.5, -0.5,
         0.5, -0.5, -0.5,
         0.5,  0.5, -0.5,
        -0.5,  0.5, -0.5,
         1.0,  0.0,  0.0,
         0.0,  1.0,  0.0,
         0.0,  0.0,  1.0,
         1.0,  1.0,  1.0,
         1.0,  0.0,  0.0,
         0.0,  1.0,  0.0,
         0.0,  0.0,  1.0,
         1.0,  1.0,  1.0,
    ], dtype=np.float32)

    index_data = np.array([
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7
    ], dtype=np.uint32)
    
    # Compile shaders.
    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), \
                            compileShader(fragment_src, GL_FRAGMENT_SHADER))
    
    # Important stuff.
    # Create and bind vertex buffer, and store data.
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)
    
    # Create and bind index buffer, and store data.
    ibo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)
    
    # Get position of a_position in shader and specify data structure.
    position = glGetAttribLocation(shader, "a_position")
    glEnableVertexAttribArray(position)
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    
    color = glGetAttribLocation(shader, "a_color")
    glEnableVertexAttribArray(color)
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(48))
    
    # OpenGL initializing stuff.
    glClearColor(0, 0, 0, 1)
    glEnable(GL_DEPTH_TEST)
    glUseProgram(shader)
    
    rotation_location = glGetUniformLocation(shader, "rotation")
    
    ct = 0
    
    # Main application loop.
    while not glfw.window_should_close(window):
        ct = glfw.get_time()
        
        glfw.poll_events()
        
        rotation = pyrr.matrix44.create_from_eulers([.1 * ct, .4 * ct, .7 * ct])
        glUniformMatrix4fv(rotation_location, 1, GL_FALSE, rotation)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDrawElements(GL_TRIANGLES, len(index_data), GL_UNSIGNED_INT, None)
        
        glfw.swap_buffers(window)
    
    # Terminate GLFW.
    glfw.terminate()

if __name__ == "__main__":
    main()