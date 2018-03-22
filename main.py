# Imports GLFW, OpenGL, and numpy
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
import pyrr

# List of cords for the vertices for drawing a triangle and the vertex colors for is as well (order of cords is "x, y, z, r, g, b")
tri_verts = [-0.5, -0.5, 0.0, 1.0, 1.0, 0.0,
             0.5, -0.5, 0.0,  0.0, 1.0, 1.0,
             0.0, 0.5, 0.0,   1.0, 0.0, 1.0]


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
    #////////////////////////////////////////////#
    # Some variables to change the view and such #
    #////////////////////////////////////////////#

    FOV = 35                    # Changes the field of view
    rotation_speed = 1          # Changes speed of the triangles rotation
    display_res = [1920, 1080]  # Window resolution

    # Initializing glfw
    if not glfw.init():
        print('Error when trying to initialize GLFW')
        return
    print('Initializing GLFW...')

    # Makes window
    window = glfw.create_window(display_res[0], display_res[1], "OpenGL Test", None, None)
    print('Creating window...')

    # Closes program when window is closed
    if not window:
        glfw.terminate()
        return

    # Start of OpenGL code
    glfw.make_context_current(window)

    # Compiles the vertex and fragment shader together
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vert_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(frag_shader, GL_FRAGMENT_SHADER))
    print('Compiling shaders...')

    # Sets background color
    glClearColor(1, 1, 1, 1)

    # Sends vertex data to VRAM
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, 72, tri_verts, GL_STATIC_DRAW)

    # Creates triangle
    position = glGetAttribLocation(shader, 'position')
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
    glEnableVertexAttribArray(position)

    # Colors the triangle
    color = glGetAttribLocation(shader, 'colors')
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    glEnableVertexAttribArray(color)

    # Enables shaders
    glUseProgram(shader)

    # Perspective matrix
    view_mat = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0., -3.0]))
    projection_mat = pyrr.matrix44.create_perspective_projection_matrix(FOV, display_res[0] / display_res[1], 0.1, 50)
    model_mat = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
    view_location = glGetUniformLocation(shader, 'view')
    proj_location = glGetUniformLocation(shader, 'projection')
    model_location = glGetUniformLocation(shader, 'model')

    glUniformMatrix4fv(view_location, 1, GL_FALSE, view_mat)
    glUniformMatrix4fv(proj_location, 1, GL_FALSE, projection_mat)
    glUniformMatrix4fv(model_location, 1, GL_FALSE, model_mat)

    print('Program started successfully!')

    # Main loop
    while not glfw.window_should_close(window):
        # Put opengl rendering code here...
        glClear(GL_COLOR_BUFFER_BIT)

        # Rotates the triangle
        transform = glGetUniformLocation(shader, 'transform')
        rotation_x = pyrr.Matrix44.from_x_rotation(rotation_speed * glfw.get_time())
        rotation_y = pyrr.Matrix44.from_y_rotation(rotation_speed * glfw.get_time())
        rotation_z = pyrr.Matrix44.from_x_rotation(rotation_speed * glfw.get_time())

        glUniformMatrix4fv(transform, 1, GL_FALSE, rotation_x * rotation_y * rotation_z)

        # Draws the triangle
        glDrawArrays(GL_TRIANGLES, 0, 3)

        # Swaps front and back buffers
        glfw.swap_buffers(window)
        # Detects any events that happen in GLFW (i.e the window closing)
        glfw.poll_events()

    print('Closing program...')
    glfw.terminate()

main()


