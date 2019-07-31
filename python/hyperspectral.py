import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
from glob import glob
import cv2
import natsort
import re
import os
import imgui
from imgui.integrations.glfw import GlfwRenderer

def get_data(dir_input):

    # Get data filenames of images without filename extension
    pattern = "([A-Za-z0-9+-_.]+)" + "[.]" + "(png)"
    p = re.compile(pattern)

    filenames = [
        p.match(f).group(0)
        for f in os.listdir(dir_input) if p.match(f)
    ]
    filenames = list(set(filenames))

    filenames = natsort.natsorted(filenames, key=lambda y: y.lower())

    lambdas = [
        re.sub("nm.png", "", re.sub("cube_irradiance_", "", f))
        for f in filenames
    ]
    lambdas = [float(l) for l in lambdas]
    images = [
        cv2.imread(os.path.join(dir_input, f), 0)
        for f in filenames
    ]

    return images, lambdas

def main():

    # initialize glfw
    if not glfw.init():
        return
    
    #creating the window
    window = glfw.create_window(800, 600, "My OpenGL window", None, None)


    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
	
	
	
    imgui.create_context()
    impl = GlfwRenderer(window)


	
    #           positions        colors          texture coords
    quad = [   -1.0, -1.0, 0.0,  1.0, 0.0, 0.0,  0.0, 0.0,
                1.0, -1.0, 0.0,  0.0, 1.0, 0.0,  1.0, 0.0,
                1.0,  1.0, 0.0,  0.0, 0.0, 1.0,  1.0, 1.0,
               -1.0,  1.0, 0.0,  1.0, 1.0, 1.0,  0.0, 1.0]

    quad = numpy.array(quad, dtype = numpy.float32)

    indices = [0, 1, 2,
               2, 3, 0]

    indices = numpy.array(indices, dtype= numpy.uint32)

    vertex_shader = """
    #version 430
    in layout(location = 0) vec3 position;
    in layout(location = 1) vec3 color;
    in layout(location = 2) vec2 inTexCoords;
    out vec3 newColor;
    out vec2 outTexCoords;
    void main()
    {
        gl_Position = vec4(position, 1.0f);
        newColor = color;
        outTexCoords = vec2(inTexCoords.x, 1.0f - inTexCoords.y);
    }
    """

    fragment_shader = """
    #version 430
    in vec3 newColor;
    in vec2 outTexCoords;
    out vec4 outColor;
	
    uniform sampler2DArray samplerTex;

	uniform int sliderR;
	uniform int sliderG;
	uniform int sliderB;

    void main()
    {
		// newcolor just shows you how to pass values through the shader stages
		//outColor = vec4(newColor, 1.0f);
        float texDataR = texture(samplerTex, vec3(outTexCoords, float(sliderR))).x;
		float texDataG = texture(samplerTex, vec3(outTexCoords, float(sliderG))).x;
        float texDataB = texture(samplerTex, vec3(outTexCoords, float(sliderB))).x;

		outColor = vec4(texDataR * 100.0f, texDataG * 100.0f, texDataB * 100.0f, 1.0f);
    }
    """
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, 128, quad, GL_STATIC_DRAW)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, 24, indices, GL_STATIC_DRAW)

    #position = glGetAttribLocation(shader, "position")
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    #color = glGetAttribLocation(shader, "color")
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    #texCoords = glGetAttribLocation(shader, "inTexCoords")
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))
    glEnableVertexAttribArray(2)

    sliderR_loc = glGetUniformLocation(shader, "sliderR")
    sliderG_loc = glGetUniformLocation(shader, "sliderG")
    sliderB_loc = glGetUniformLocation(shader, "sliderB")

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D_ARRAY, texture)
    #texture wrapping params
    glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_R, GL_REPEAT)

    #texture filtering params
    glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MAG_FILTER, GL_LINEAR)


    images, lambdas = get_data("D:\data\hysperspectral\snapscan_data_png")
    #image = Image.open("./maybotDance.JPG")
    #for index, image in enumerate(images):
        	
    numberOfImages = len(images)
    #print(numberOfImages)	
    height, width = images[0].shape[0:2]
    #img_data = numpy.array(list(image.getdata()), numpy.uint8)
    #print(xsize)
    #print(ysize)	
    glTexStorage3D(GL_TEXTURE_2D_ARRAY, 1, GL_R8, width, height, numberOfImages)
	# Allocate the immutable GPU memory storage -more efficient than mutable memory if you are not going to change image size after creation
    #glPixelStorei(GL_UNPACK_ALIGNMENT, 4);	
    #glPixelStorei(GL_UNPACK_ROW_LENGTH, xsize);
	# fill each image in the array with the same img_data
    for i in range(numberOfImages):
        #cv2.imshow('image', image*100.0)
        #cv2.waitKey(1)	
        #print(i)
        img_data = numpy.array(images[i].data, numpy.uint8)		
        glTexSubImage3D(GL_TEXTURE_2D_ARRAY, 0, 0, 0, i, width, height, 1, GL_RED, GL_UNSIGNED_BYTE, img_data)		
    #cv2.destroyAllWindows()
    #print("reached here")
    glUseProgram(shader)

    glClearColor(0.2, 0.3, 0.2, 1.0)
    
    sliderRValue = 0		
    sliderGValue = 0		
    sliderBValue = 0		

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()
        imgui.new_frame()

        w, h = glfw.get_framebuffer_size(window)
        glViewport(0,0,w,h)		
        glClear(GL_COLOR_BUFFER_BIT)

        glUniform1i(sliderR_loc, sliderRValue)
        glUniform1i(sliderG_loc, sliderGValue)
        glUniform1i(sliderB_loc, sliderBValue)
		
        #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE );		
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
		
        imgui.begin("My first imgui success!", True)
        changedR, sliderRValue = imgui.slider_int("sliceR", sliderRValue, min_value=0, max_value=numberOfImages)
        changedG, sliderGValue = imgui.slider_int("sliceG", sliderGValue, min_value=0, max_value=numberOfImages)
        changedB, sliderBValue = imgui.slider_int("sliceB", sliderBValue, min_value=0, max_value=numberOfImages)

        imgui.end()		

        imgui.render()		
        impl.render(imgui.get_draw_data())

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()