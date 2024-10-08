#version 300 es
precision highp float;
uniform mat4 p3d_ModelViewProjectionMatrix;

in vec4 p3d_Vertex;
in vec4 p3d_Normal;
in vec2 p3d_MultiTexCoord0;
in vec2 p3d_MultiTexCoord1;

out vec2 texcoord0;
out vec2 texcoord1;
out vec4 vertex;

void main() {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    texcoord0 = p3d_MultiTexCoord0;
    texcoord1 = p3d_MultiTexCoord1;
    vertex = p3d_Vertex;
}



