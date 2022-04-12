#version 330 core

layout(location=0) in vec3 a_position;
layout(location=1) in vec3 a_color;
//layout(location=2) in vec3 a_normal;

uniform mat4 projection;
uniform mat4 translation;
uniform mat4 rotation;

out vec3 v_color;

void main() {
    gl_Position = projection * translation * rotation * vec4(a_position, 1.0);
    v_color = a_color;
}