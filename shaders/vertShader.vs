#version 430 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoord;

out vec2 TexCoord;

void main()
{
 // an approach that doesnt require CPU passed vertices, very nice
 // taken from demanze answer at https://stackoverflow.com/questions/2588875/whats-the-best-way-to-draw-a-fullscreen-quad-in-opengl-3-2
	float x = float(((uint(gl_VertexID) + 2u) / 3u)%2u); // u is just the type qualifer, like f, i think
    float y = float(((uint(gl_VertexID) + 1u) / 3u)%2u); 

	TexCoord = vec2(x, 1.0 - y);

	gl_Position = vec4(-1.0f + x*2.0f, -1.0f+y*2.0f, 0, 1.0f);
}