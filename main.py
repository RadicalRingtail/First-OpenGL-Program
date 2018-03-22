# Imports GLFW, OpenGL, and numpy
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy

# List of cords for the vertices for drawing a triangle (order of cords is "x, y, z")
tri_verts = [-0.5, -0.5, 0.0,
             0.5, -0.5, 0.0,
             0.0, 0.5, 0.0]

# Converts list to numpy array
tri_verts = numpy.array(tri_verts, dtype = numpy.float32)

# Imports vertex shader
import_vs = open('shaders/vertex_shader.txt', 'r')
vert_shader = import_vs.read()
import_vs.close()

# Imports fragment shader
import_fs = open('shaders/fragment_shader.txt', 'r')
frag_shader = import_fs.read()
import_fs.close()

# Main window
def main():
    # Initializing glfw
    if not glfw.init():
        print('Error when trying to initialize GLFW')
        return
    display_res = [1920, 1080]

    # Makes window
    window = glfw.create_window(display_res[0], display_res[1], "OpenGL Test", None, None)

    # Closes program when window is closed
    if not window:
        glfw.terminate()
        return

    # Start of OpenGL code
    glfw.make_context_current(window)

    # Sets background color
    glClearColor(0.7, 0.5, 0.2, 1.0)

    # Compiles the vertex and fragment shader together
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vert_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(frag_shader, GL_FRAGMENT_SHADER))

    # Sends vertex data to VRAM
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, 36, tri_verts, GL_STATIC_DRAW)

    # Creates triangle
    position = glGetAttribLocation(shader, 'position')
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(position)

    # Enables shaders
    glUseProgram(shader)

    # Main loop
    while not glfw.window_should_close(window):

        # Put opengl rendering code here...
        glClear(GL_COLOR_BUFFER_BIT)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        # Swaps front and back buffers
        glfw.swap_buffers(window)
        # Detects any events that happen in GLFW (i.e the window closing)
        glfw.poll_events()

    glfw.terminate()

main()


