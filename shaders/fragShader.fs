#version 430 core
const float PI = 3.1415926535897932384626433832795f;

layout (binding=0) uniform sampler2DArray textureHyperSpectral;


in vec2 TexCoord;

layout(location = 0) out vec4 color;

uniform int texLevelR;
uniform int texLevelG;
uniform int texLevelB;

uniform vec4 scale;


void main()
{
	ivec3 texSize = textureSize(textureHyperSpectral, 0).xyz;
	float dataRed = texelFetch(textureHyperSpectral, ivec3(TexCoord.x * texSize.x, TexCoord.y * texSize.y, texLevelR), 0).x;
	float dataGreen = texelFetch(textureHyperSpectral, ivec3(TexCoord.x * texSize.x, TexCoord.y * texSize.y, texLevelG), 0).x;
	float dataBlue = texelFetch(textureHyperSpectral, ivec3(TexCoord.x * texSize.x, TexCoord.y * texSize.y, texLevelB), 0).x;

	
	color = vec4(dataRed * scale.x, dataGreen * scale.y, dataBlue * scale.z, 1);
}