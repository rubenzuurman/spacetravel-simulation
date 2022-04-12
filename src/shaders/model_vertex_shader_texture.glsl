#version 330 core

layout(location=0) in vec3 a_position;
layout(location=1) in vec2 a_texture;
//layout(location=2) in vec3 a_normal;

uniform mat4 projection;
uniform mat4 translation;
uniform mat4 rotation;

out vec2 v_texture;

void main() {
    gl_Position = projection * translation * rotation * vec4(a_position, 1.0);
    v_texture = a_texture;
}