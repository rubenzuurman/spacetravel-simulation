import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

def main():
    # Initialize GLFW.
    if not glfw.init():
        raise Exception("GLFW could not be initialized.")
    
    # Create window.
    window = glfw.create_window(1920, 1080, "Window Title", None, None)
    
    # Check if the window was created.
    if not window:
        glfw.terminate()
        raise Exception("GLFW window could not be created.")
    
    # Make context current and set window position.
    glfw.make_context_current(window)
    glfw.set_window_pos(window, (3840 - 1920) // 2, (2160 - 1080) // 2)
    
    # Enable vsync.
    glfw.swap_interval(1)
    
    # Set anti-aliasing to 8.
    glfw.window_hint(glfw.SAMPLES, 0)
    
    # Set OpenGL version to 3.3 core.
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    
    # Here starts the opengl part.
    # Set vertex shader source and fragment shader source.
    vertex_shader_src = """
    #version 330 core
    layout (location = 0) in vec3 aPos;
    
    void main()
    {
        gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
    }
    """
    
    fragment_shader_src = """
    #version 330 core
    out vec4 FragColor;
    
    void main()
    {
        FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
    }
    """
    
    fragment_shader2_src = """
    #version 330 core
    out vec4 FragColor;
    
    void main()
    {
        FragColor = vec4(1.0f, 1.0f, 0.0f, 1.0f);
    }
    """
    
    # Compile shaders.
    vertex_shader = compileShader(vertex_shader_src, GL_VERTEX_SHADER)
    fragment_shader = compileShader(fragment_shader_src, GL_FRAGMENT_SHADER)
    fragment_shader2 = compileShader(fragment_shader2_src, GL_FRAGMENT_SHADER)
    
    # Compile shader program.
    shader = compileProgram(vertex_shader, fragment_shader)
    shader2 = compileProgram(vertex_shader, fragment_shader2)
    
    # Define vertices.
    """vertices = np.array([
         0.5,  0.5,  0.0,
         0.5, -0.5,  0.0,
        -0.5, -0.5,  0.0,
        -0.5,  0.5,  0.0,
    ], dtype=np.float32)"""
    vertices = np.array([
        -0.50, 0.00, 0.00,
        -0.25, 0.50, 0.00,
         0.00, 0.00, 0.00,
    ], dtype=np.float32)
    
    # Define indices.
    """indices = np.array([
        0, 1, 3,
        1, 2, 3,
    ], dtype=np.uint32)"""
    indices = np.array([
        0, 1, 2
    ], dtype=np.uint32)
    
    # Generate vertex array object.
    vao = glGenVertexArrays(1)
    # Bind vao.
    glBindVertexArray(vao)
    
    # Generate vertex buffer object.
    vbo = glGenBuffers(1)
    # Bind vbo.
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    # Send data to vbo.
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
    # Specify position using a vertex attribute pointer.
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))
    # Enable position vertex attribute array.
    glEnableVertexAttribArray(0)
    
    # Generate index buffer object.
    ibo = glGenBuffers(1)
    # Bind ibo.
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)
    # Send data to ibo.
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
    
    # Unbind vao.
    glBindVertexArray(0)
    
    # Unbind vbo.
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    # Unbind ibo.
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
    
    
    
    vertices2 = np.array([
         0.00, 0.00, 0.00,
         0.50, 0.00, 0.00,
         0.25, 0.50, 0.00,
    ], dtype=np.float32)
    
    indices2 = np.array([
        0, 1, 2
    ], dtype=np.uint32)
    
    vao2 = glGenVertexArrays(1)
    glBindVertexArray(vao2)
    
    vbo2 = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo2)
    glBufferData(GL_ARRAY_BUFFER, vertices2.nbytes, vertices2, GL_STATIC_DRAW)
    
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    ibo2 = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo2)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices2.nbytes, indices2, GL_STATIC_DRAW)
    
    glBindVertexArray(0)
    
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
    
    
    # OpenGL setup stuff.
    glClearColor(0, 0, 0, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    # Start application loop.
    while not glfw.window_should_close(window):
        # Poll events.
        glfw.poll_events()
        
        # Clear frame buffer and depth buffer.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Enable shader program.
        glUseProgram(shader)
        
        # Bind vao.
        glBindVertexArray(vao)
        
        # Render.
        glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, None)
        
        # Enable different shader program for vao2.
        glUseProgram(shader2)
        
        # Bind vao2.
        glBindVertexArray(vao2)
        
        # Render.
        glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, None)
        
        # Unbind vao.
        glBindVertexArray(0)
        
        # Disable shader program.
        glUseProgram(0)
        
        # Swap buffers.
        glfw.swap_buffers(window)
    
    # Terminate GLFW.
    glfw.terminate()

if __name__ == "__main__":
    main()