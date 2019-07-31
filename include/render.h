#define GLUT_NO_LIB_PRAGMA
//##### OpenGL ######
#include <GL/glew.h>
#define GLFW_INCLUDE_GLU
#include <GLFW/glfw3.h>
#define GLM_ENABLE_EXPERIMENTAL
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
	void setLevel(int red, int green, int blue)
	{
		m_texLevelR = red;
		m_texLevelG = green;
		m_texLevelB = blue;
	}

	void setScale(float redScale, float greenScale, float blueScale)
	{
		m_texScale = glm::vec4(redScale, greenScale, blueScale, 1.0f);
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
	void getMeanOfFrame(std::vector<float> &fMeans);

	void render();


private:

	GLSLProgram renderProg;
	GLSLProgram sumProg;

	GLFWwindow * m_window;
	bool m_show_imgui = true;

	std::vector<float> m_vertices;
	std::vector<unsigned int> m_indices;
	int m_texLevelR = 0;
	int m_texLevelG = 0;
	int m_texLevelB = 0;
	glm::vec4 m_texScale = glm::vec4(1.0f);

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
	GLuint m_texLevelRID;
	GLuint m_texLevelGID;
	GLuint m_texLevelBID;

	GLuint m_texScaleID;

};