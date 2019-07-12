#define GLUT_NO_LIB_PRAGMA
//##### OpenGL ######
#include <GL/glew.h>
#define GLFW_INCLUDE_GLU
#include <GLFW/glfw3.h>

#include <glm/glm.hpp>
#include <glm/gtc/type_ptr.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtx/euler_angles.hpp>
#include <glm/gtx/transform.hpp>



#include "opencv2/core/utility.hpp"
#include "opencv2/opencv.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"

#include "glhelper.h"


#include <iostream>
#include <fstream>

#include <vector>
#include <valarray>
#include <list>
#include <numeric>
#include <algorithm>

#include "glutils.h"
#include "glslprogram.h"

#define _USE_MATH_DEFINES
#include <math.h>

class gRender
{
public:
	gRender(){}
	~gRender(){};

	GLFWwindow * window()
	{
		return m_window;
	}

	bool showImgui()
	{
		return m_show_imgui;
	}
	void setLevel(int level)
	{
		m_texLevel = level;
	}
	GLFWwindow * loadGLFWWindow();

	void compileAndLinkShader();
	void requestShaderInfo();
	void setLocations();
	void setVertPositions();
	void allocateBuffers();
	void allocateTextures();
	void setBuffers(GLuint quadlist, GLuint quadlistMeanTemp);
	void setFrameSize(glm::vec3 frameSize);
	void uploadImages(std::vector<cv::Mat> images);


	void render();


private:

	GLSLProgram renderProg;

	GLFWwindow * m_window;
	bool m_show_imgui = true;

	std::vector<float> m_vertices;
	std::vector<unsigned int> m_indices;
	int m_texLevel = 0;
	glm::vec3 m_frameSize;

	// programs
	GLuint m_programID;

	// objects 
	GLuint m_VAO;
	GLuint m_EBO;
	GLuint m_VBO;

	// textures
	GLuint m_textureHyperSpectral;
	// buffers

	// uniforms
	GLuint m_texLevelID;
};