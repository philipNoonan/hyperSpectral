#include <imgui.h>
#include "imgui_impl_glfw_gl3.h"
#define IM_ARRAYSIZE(_ARR)  ((int)(sizeof(_ARR)/sizeof(*_ARR)))

#define GL_GPU_MEM_INFO_TOTAL_AVAILABLE_MEM_NVX 0x9048
#define GL_GPU_MEM_INFO_CURRENT_AVAILABLE_MEM_NVX 0x9049

#include <stdio.h>
#include <iostream>
#define GLUT_NO_LIB_PRAGMA
//##### OpenGL ######
#include <GL/glew.h>
#define GLFW_INCLUDE_GLU
#include <GLFW/glfw3.h>
#include <deque>
#include <valarray>
#include <map>

//#include "openCVStuff.h"

#include "render.h"

#include "opencv2/core/utility.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/optflow.hpp"

#include <thread>
#include <mutex>
#include <sstream>


GLFWwindow *window;

gRender grender;

int texLevelRed = 0;
int texLevelGreen = 0;
int texLevelBlue = 0;

float texScaleRed = 25.0f;
float texScaleGreen = 25.0f;
float texScaleBlue = 25.0f;

glm::vec3 frameSize;

std::vector<cv::Mat> imagesFromFile;


