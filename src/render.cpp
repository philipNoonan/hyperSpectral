#include "render.h"



GLFWwindow * gRender::loadGLFWWindow()
{

	glfwInit();
	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
	glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
	//glfwWindowHint(GLFW_REFRESH_RATE, 5);
	glfwWindowHint(GLFW_RESIZABLE, GL_TRUE);
	glEnable(GL_DEPTH_TEST);

	m_window = glfwCreateWindow(1920, 1080, "hyperSpectralViewer", nullptr, nullptr);

	if (m_window == nullptr)
	{
		std::cout << "Failed to create GLFW window" << std::endl;
		glfwTerminate();
		//return -1;
	}

	glfwMakeContextCurrent(m_window);
	//glfwSwapInterval(1); // Enable vsync
	glewExperimental = GL_TRUE;

	if (glewInit() != GLEW_OK) 
	{
		std::cout << "Failed to initialize GLEW" << std::endl;
		//return -1;
	}


	return m_window;
}

void gRender::requestShaderInfo()
{
	renderProg.printActiveUniforms();
}

void gRender::compileAndLinkShader()
{
	try {
		renderProg.compileShader("shaders/vertShader.vs");
		renderProg.compileShader("shaders/fragShader.fs");
		renderProg.link();

	}
	catch (GLSLProgramException &e) {
		std::cerr << e.what() << std::endl;
		exit(EXIT_FAILURE);
	}
}

void gRender::setLocations()
{
	m_texLevelRID = glGetUniformLocation(renderProg.getHandle(), "texLevelR");
	m_texLevelGID = glGetUniformLocation(renderProg.getHandle(), "texLevelG");
	m_texLevelBID = glGetUniformLocation(renderProg.getHandle(), "texLevelB");

	m_texScaleID = glGetUniformLocation(renderProg.getHandle(), "scale");


}

void gRender::setFrameSize(glm::vec3 frameSize)
{
	m_frameSize = frameSize;
}

void gRender::setVertPositions()
{
	std::vector<float> vertices = {
		// Positions				// Texture coords
		1.0f,	1.0f,	0.0f,		1.0f, 1.0f, // top right
		1.0f,	-1.0f,	0.0f,		1.0f, 0.0f, // bottom right
		-1.0f,	-1.0f,	0.0f,		0.0f, 0.0f, // bottom left
		-1.0f,	1.0f,	0.0f,		0.0f, 1.0f  // Top left
	};

	m_vertices = vertices;

	std::vector<unsigned int>  indices = {  // Note that we start from 0!
		0, 1, 3, // First Triangle
		1, 2, 3  // Second Triangle
	};

	m_indices = indices;

}

void gRender::allocateTextures()
{

	m_textureHyperSpectral = GLHelper::createTexture(m_textureHyperSpectral, GL_TEXTURE_2D_ARRAY, 1, m_frameSize.x, m_frameSize.y, m_frameSize.z, GL_R8, GL_NEAREST, GL_NEAREST_MIPMAP_NEAREST);
}

void gRender::allocateBuffers()
{
	glGenVertexArrays(1, &m_VAO);
	glGenBuffers(1, &m_VBO);
	glGenBuffers(1, &m_EBO);
	glBindVertexArray(m_VAO);

	// standard verts
	glBindBuffer(GL_ARRAY_BUFFER, m_VBO);
	glBufferData(GL_ARRAY_BUFFER, m_vertices.size() * sizeof(float), &m_vertices[0], GL_DYNAMIC_DRAW);
	// EBO
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, m_EBO);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, m_indices.size() * sizeof(unsigned int), &m_indices[0], GL_DYNAMIC_DRAW);
	// Position attribute for Depth
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (GLvoid*)0);
	glEnableVertexAttribArray(0);
	//// TexCoord attribute for Depth
	glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (GLvoid*)(3 * sizeof(float)));
	glEnableVertexAttribArray(1);
	glBindVertexArray(0);
	glBindBuffer(GL_ARRAY_BUFFER, 0);

}

void gRender::setBuffers(GLuint quadList, GLuint quadlistMeanTemp) 
{
	
}

void gRender::uploadImages(std::vector<cv::Mat> images)
{



	glActiveTexture(GL_TEXTURE0);

	//use fast 4-byte alignment (default anyway) if possible
	glPixelStorei(GL_UNPACK_ALIGNMENT, (images[0].step & 3) ? 1 : 4);

	//set length of one complete row in data (doesn't need to equal image.cols)
	glPixelStorei(GL_UNPACK_ROW_LENGTH, images[0].step / images[0].elemSize());

	for (int i = 0; i < images.size(); i++)
	{
		glBindTexture(GL_TEXTURE_2D_ARRAY, m_textureHyperSpectral);
		glTexSubImage3D(GL_TEXTURE_2D_ARRAY, 0, 0, 0, i, m_frameSize.x, m_frameSize.y, 1, GL_RED, GL_UNSIGNED_BYTE, images[i].data);
	}
}





void gRender::render()
{


	int w, h;
	glfwGetFramebufferSize(m_window, &w, &h);
	glViewport(0, 0, w, h);


	//glBindFramebuffer(GL_FRAMEBUFFER, 0);
	renderProg.use();
	glBindFramebuffer(GL_FRAMEBUFFER, 0);

	glActiveTexture(GL_TEXTURE0);
	glBindTexture(GL_TEXTURE_2D_ARRAY, m_textureHyperSpectral);

	glBindVertexArray(m_VAO);

	//glUniformSubroutinesuiv(GL_VERTEX_SHADER, 1, &m_fromStandardTextureID);
	//glUniformSubroutinesuiv(GL_FRAGMENT_SHADER, 1, &m_fromDepthID);
	glUniform1i(m_texLevelRID, m_texLevelR);
	glUniform1i(m_texLevelGID, m_texLevelG);
	glUniform1i(m_texLevelBID, m_texLevelB);

	glUniform4fv(m_texScaleID, 1, glm::value_ptr(m_texScale));


	glDrawArrays(GL_TRIANGLES, 0, 6);







}


