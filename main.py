import pygame
from pygame.locals import *
from OpenGL.GL import *
import config
from shader import create_shader_program
from pixel import create_pixel
from texture_loader import load_pixel_art
import numpy as np

def create_pixel_grid():
    rows, cols = config.GRID_SIZE  # Unpack grid size
    pixel_width = 2.0 / cols   # Each pixel exactly fills a column space
    pixel_height = 2.0 / rows  # Each pixel exactly fills a row space
    half_width = pixel_width / 2.0
    half_height = pixel_height / 2.0

    pixel_positions = []
    for y in range(rows):
        for x in range(cols):
            px = (x * pixel_width) - 1.0 + half_width  # Center horizontally
            py = (rows - 1 - y) * pixel_height - 1.0 + half_height  # Flip vertically
            pixel_positions.append((px, py))

    return np.array(pixel_positions, dtype=np.float32)


def main():
    pygame.init()
    pygame.display.set_mode((config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT), DOUBLEBUF | OPENGL)
    glClearColor(*config.BACKGROUND_COLOR)
    shader_program = create_shader_program()
    glUseProgram(shader_program)

    VAO, EBO, index_count = create_pixel()
    pixel_positions = create_pixel_grid()
    pixel_colors = load_pixel_art("pixel_map.txt", config.GRID_SIZE)

    # Load instance buffers for positions & colors
    position_VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, position_VBO)
    glBufferData(GL_ARRAY_BUFFER, pixel_positions.nbytes, pixel_positions, GL_STATIC_DRAW)

    glBindVertexArray(VAO)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)
    glVertexAttribDivisor(1, 1)

    color_VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, color_VBO)
    glBufferData(GL_ARRAY_BUFFER, pixel_colors.nbytes, pixel_colors, GL_STATIC_DRAW)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    glEnableVertexAttribArray(2)
    glVertexAttribDivisor(2, 1)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    rows, cols = config.GRID_SIZE  # Unpack tuple
    pixel_size_location = glGetUniformLocation(shader_program, "pixelSize")
    glUniform2f(pixel_size_location, 2.0 / cols, 2.0 / rows)  


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(shader_program)
        glBindVertexArray(VAO)

        rows, cols = config.GRID_SIZE  
        total_pixels = rows * cols

        glDrawElementsInstanced(GL_TRIANGLES, index_count, GL_UNSIGNED_INT, None, total_pixels)

        pygame.display.flip()

    # Cleanup OpenGL resources
    glDeleteBuffers(1, [position_VBO])
    glDeleteBuffers(1, [color_VBO])
    glDeleteBuffers(1, [EBO])
    glDeleteVertexArrays(1, [VAO])
    glDeleteProgram(shader_program)  

    pygame.quit()

if __name__ == "__main__":
    main()
