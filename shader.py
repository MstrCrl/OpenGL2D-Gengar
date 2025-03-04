from OpenGL.GL import *

vertex_shader_src = """
#version 330 core
layout (location=0) in vec2 aPos;
layout (location=1) in vec2 instancePos;
layout (location=2) in vec3 instanceColor;

out vec3 PixelColor;

uniform vec2 pixelSize;  // Change to vec2

void main()
{
    vec2 finalPos = aPos * pixelSize + instancePos;
    gl_Position = vec4(finalPos, 0.0, 1.0);
    PixelColor = instanceColor;
}
"""

fragment_shader_src = """
#version 330 core
in vec3 PixelColor;
out vec4 FragColor;

void main()
{
    FragColor = vec4(PixelColor, 1.0);
}
"""

def compile_shader(shader_type, source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(shader).decode())
    return shader

def create_shader_program():
    vertex_shader = compile_shader(GL_VERTEX_SHADER, vertex_shader_src)
    fragment_shader = compile_shader(GL_FRAGMENT_SHADER, fragment_shader_src)

    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)

    if glGetProgramiv(shader_program, GL_LINK_STATUS) != GL_TRUE:
        raise RuntimeError(glGetProgramInfoLog(shader_program).decode())

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return shader_program
