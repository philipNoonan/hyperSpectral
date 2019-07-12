#version 430 core
const float PI = 3.1415926535897932384626433832795f;

layout (binding=0) uniform sampler2DArray textureHyperSpectral;


in vec2 TexCoord;

layout(location = 0) out vec4 color;

uniform int texLevel;


void main()
{
	ivec3 texSize = textureSize(textureHyperSpectral, 0).xyz;
	float data = texelFetch(textureHyperSpectral, ivec3(TexCoord.x * texSize.x, TexCoord.y * texSize.y, texLevel), 0).x;
	color = vec4(data.xxx * 10.0f, 1);
}