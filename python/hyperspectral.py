import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
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

def do_some_compute(computeShader, imageTex, outImage, width, height):
    glUseProgram(computeShader)
    glBindImageTexture(0, imageTex, 0, GL_FALSE, 0, GL_READ_ONLY, GL_R8UI)    
    glBindImageTexture(1, outImage, 0, GL_FALSE, 0, GL_WRITE_ONLY, GL_RGBA32F)    

    glDispatchCompute(int((width/32.0)+0.5), int((height/32.0)+0.5), 1)
    glMemoryBarrier(GL_ALL_BARRIER_BITS)

def read_texture_memory(imageTex, width, height):

    newImages = np.empty([width*height*4], dtype=np.float)
    #glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, imageTex)
    newImages = glGetTexImageub(GL_TEXTURE_2D, 0, GL_RGBA, GL_FLOAT)
    glBindTexture(GL_TEXTURE_2D, 0)
    
    newImages.reshape((width, height, 4))
    print(newImages)	

def createTexture(target, internalFormat, levels, width, height, depth, minFilter, magFilter):
    texName = glGenTextures(1)
    glBindTexture(target, texName)
    #texture wrapping params
    glTexParameteri(target, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
    glTexParameteri(target, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
    #texture filtering params
    glTexParameteri(target, GL_TEXTURE_MIN_FILTER, minFilter)
    glTexParameteri(target, GL_TEXTURE_MAG_FILTER, magFilter)
    
    if target == GL_TEXTURE_1D:
        glTexStorage1D(target, levels, internalFormat, width)
    elif target == GL_TEXTURE_2D:
        glTexStorage2D(target, levels, internalFormat, width, height)
    elif target == GL_TEXTURE_3D or depth > 1:
        glTexParameteri(target, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_BORDER)	
        glTexStorage3D(target, levels, internalFormat, width, height, depth)

    return texName	

def main():

    # initialize glfw
    if not glfw.init():
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
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

    quad = np.array(quad, dtype = np.float32)

    indices = [0, 1, 2,
               2, 3, 0]

    indices = np.array(indices, dtype= np.uint32)

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

    compute_shader = """
    #version 430

    layout(local_size_x = 32, local_size_y = 32) in;

    layout(binding= 0, r8ui) uniform uimage2DArray imageArray;
    layout(binding= 1, rgba32f) uniform image2D outputImage;

    void main()
    {
        uvec2 pix = gl_GlobalInvocationID.xy;
        ivec3 imSize = imageSize(imageArray);
		
		float sumPixel = 0.0f;

        if (pix.x < imSize.x && pix.y < imSize.y)
        {
            for (int z = 0; z < imSize.z; z++)
            {
                sumPixel += float(imageLoad(imageArray, ivec3(pix, z)).z);
            }


        }
		
		imageStore(outputImage, ivec2(pix), vec4(sumPixel, sumPixel / float(imSize.z), 69.0f, 8008135.0f));
		
    }

    """

    computeShader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(compute_shader, GL_COMPUTE_SHADER))

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)
	
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, 128, quad, GL_STATIC_DRAW)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, 24, indices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))
    glEnableVertexAttribArray(2)

    sliderR_loc = glGetUniformLocation(shader, "sliderR")
    sliderG_loc = glGetUniformLocation(shader, "sliderG")
    sliderB_loc = glGetUniformLocation(shader, "sliderB")

    images, lambdas = get_data("D:\data\hysperspectral\snapscan_data_png")
    #image = Image.open("./maybotDance.JPG")
    #for index, image in enumerate(images):
        	
    numberOfImages = len(images)
    #print(numberOfImages)	
    height, width = images[0].shape[0:2]
	
	    # GENERATE TEXTURES
    hyperspectralDataTexture = createTexture(GL_TEXTURE_2D_ARRAY, GL_R8, 1, width, height, numberOfImages, GL_LINEAR, GL_LINEAR)
    outputTexture = createTexture(GL_TEXTURE_2D, GL_RGBA32F, 1, width, height, 1, GL_LINEAR, GL_LINEAR)
	
    #img_data = numpy.array(list(image.getdata()), numpy.uint8)
    #print(width)
    #print(height)
    #print(images[0])
	# Allocate the immutable GPU memory storage -more efficient than mutable memory if you are not going to change image size after creation
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1);	
    glPixelStorei(GL_UNPACK_ROW_LENGTH, width);
	# fill each image in the array with the same img_data
    for i in range(numberOfImages):
        #cv2.imshow('image', images[i]*1000.0)
        #cv2.waitKey(0)	
        #print(images[i].strides)
        img_data = np.array(images[i].data, np.uint8)		
        #print(img_data.shape[0:2])
        glTexSubImage3D(GL_TEXTURE_2D_ARRAY, 0, 0, 0, i, width, height, 1, GL_RED, GL_UNSIGNED_BYTE, img_data)		
    #cv2.destroyAllWindows()
    #print("reached here")

    glClearColor(0.2, 0.3, 0.2, 1.0)
    
    sliderRValue = 0		
    sliderGValue = 0		
    sliderBValue = 0		

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()
        imgui.new_frame()
        glUseProgram(shader)

        w, h = glfw.get_framebuffer_size(window)
        glViewport(0,0,int(w/2),h)		
        glClear(GL_COLOR_BUFFER_BIT)

        glUniform1i(sliderR_loc, sliderRValue)
        glUniform1i(sliderG_loc, sliderGValue)
        glUniform1i(sliderB_loc, 50)


        #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE );		
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        glUniform1i(sliderB_loc, sliderBValue)
        glViewport(int(w/2),0,int(w/2),h)		
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        imgui.begin("My first imgui success!", True)
        changedR, sliderRValue = imgui.slider_int("sliceR", sliderRValue, min_value=0, max_value=numberOfImages)
        changedG, sliderGValue = imgui.slider_int("sliceG", sliderGValue, min_value=0, max_value=numberOfImages)
        changedB, sliderBValue = imgui.slider_int("sliceB", sliderBValue, min_value=0, max_value=numberOfImages)

        if imgui.button("do some compute"):
            do_some_compute(computeShader, hyperspectralDataTexture, outputTexture, width, height)

        if imgui.button("get memory back"):
            read_texture_memory(outputTexture, width, height)

        imgui.end()		

        imgui.render()		
        impl.render(imgui.get_draw_data())

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()