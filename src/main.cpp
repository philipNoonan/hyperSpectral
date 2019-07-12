#include "main.h"



static void error_callback(int error, const char* description)
{
	fprintf(stderr, "Error %d: %s\n", error, description);
}

void gRenderInit()
{
	grender.compileAndLinkShader();
	grender.setFrameSize(frameSize);

	grender.setLocations();
	grender.setVertPositions();

	grender.allocateBuffers();
	grender.allocateTextures();

//krender.genTexCoordOffsets(1, 1, 1.0f);
}


void searchForMedia()
{
	imagesFromFile.resize(0);

	cv::String pathImages("/home/mocat/data/images/*.png");

	std::cout << pathImages << std::endl;

	std::vector<cv::String> fnImages;
	cv::glob(pathImages, fnImages, false); // recurse
	for (size_t k = 0; k<fnImages.size(); ++k)
	{
		std::cout << fnImages[k] << std::endl;

		cv::Mat im = cv::imread(fnImages[k], cv::IMREAD_GRAYSCALE);
		if (im.empty())
		{
			std::cout << "empty image " << std::endl;
			continue; //only proceed if sucsessful
		}					  // you probably want to do some preprocessing
							  //if (k == 0)
							  //imagesFromFile.push_back(cv::Mat(im.rows, im.cols, CV_8UC3));
		imagesFromFile.push_back(im);
	}
	if (imagesFromFile.size() > 0)
	{
		frameSize = glm::vec3(imagesFromFile[0].cols, imagesFromFile[0].rows, imagesFromFile.size());
	}
	else
	{
		std::cout << "no images found" << std::endl;
	}
}



int main(int, char**)
{
	glEnable(GL_DEPTH_TEST);


	int display_w, display_h;
	// load openGL window
	window = grender.loadGLFWWindow();

	glfwGetFramebufferSize(window, &display_w, &display_h);
	// Setup ImGui binding
	ImGui::CreateContext();

	ImGui_ImplGlfwGL3_Init(window, true);
	ImVec4 clear_color = ImColor(114, 144, 154);



	searchForMedia();

	gRenderInit();


	grender.uploadImages(imagesFromFile);


	double lastTime = glfwGetTime();
	// Main loop
	while (!glfwWindowShouldClose(window))
	{
		glfwGetFramebufferSize(window, &display_w, &display_h);

		//// Rendering
		glViewport(0, 0, display_w, display_h);
		glClearColor(clear_color.x, clear_color.y, clear_color.z, clear_color.w);
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);



		glfwPollEvents();
		ImGui_ImplGlfwGL3_NewFrame();


		grender.render();

		if (grender.showImgui())
		{
			//ImGui::SetNextWindowPos(ImVec2(1600 - 32 - 528 - 150, 32));
			//ImGui::SetNextWindowSize(ImVec2(528 + 150, 424), ImGuiSetCond_Always);
			ImGuiWindowFlags window_flags = 0;

			float arr[] = { 0, 0, 0, 0, 0, 0, 0, 0, 0 };
			arr[8] = arr[0];// +arr[1] + arr[2] + arr[3] + arr[4] + arr[5] + arr[6] + arr[7];
			GLint total_mem_kb = 0;
			glGetIntegerv(GL_GPU_MEM_INFO_TOTAL_AVAILABLE_MEM_NVX,
				&total_mem_kb);

			GLint cur_avail_mem_kb = 0;
			glGetIntegerv(GL_GPU_MEM_INFO_CURRENT_AVAILABLE_MEM_NVX,
				&cur_avail_mem_kb);

			bool showGUI = grender.showImgui();
			ImGui::Begin("Menu", &showGUI, window_flags);
			ImGui::Text("Application average %.3f ms/frame (%.1f FPS)", arr[8], 1000.0f / arr[8]);
			ImGui::Text("GPU Memory Usage %d MB out of %d (%.1f %%)", (total_mem_kb - cur_avail_mem_kb) / 1024, total_mem_kb / 1024, 100.0f * (1.0f - (float)cur_avail_mem_kb / (float)total_mem_kb));
			ImGui::Separator();

			ImGui::Separator();
			ImGui::Text("View Options");
			ImGui::SliderInt("slice 0", &texLevelRed, 0, imagesFromFile.size());
			ImGui::SliderInt("slice 1", &texLevelGreen, 0, imagesFromFile.size());
			ImGui::SliderInt("slice 2", &texLevelBlue, 0, imagesFromFile.size());

			ImGui::SliderFloat("scale 0", &texScaleRed, 0.0f, 50.0f);
			ImGui::SliderFloat("scale 1", &texScaleGreen, 0.0f, 50.0f);
			ImGui::SliderFloat("scale 2", &texScaleBlue, 0.0f, 50.0f);

			grender.setLevel(texLevelRed, texLevelGreen, texLevelBlue);
			grender.setScale(texScaleRed, texScaleGreen, texScaleBlue);

			ImGui::End();

		}

		ImGui::Render();
		ImGui_ImplGlfwGL3_RenderDrawData(ImGui::GetDrawData());


		glfwSwapBuffers(window);

	}

	

	// Cleanup DO SOME CLEANING!!!
	ImGui_ImplGlfwGL3_Shutdown();
	ImGui::DestroyContext();
	glfwTerminate();


	//krender.cleanUp();

	return 0;
}