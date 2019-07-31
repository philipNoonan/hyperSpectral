# hsviewer

<h2>Installation</h2>

<h3>Dependencies</h3>

We can use vcpkg to install dependencies. Get vcpkg from the link and follow its installation instructions.

<a href="https://github.com/Microsoft/vcpkg">VCPKG</a> 

<h4>Windows</h4>

To make vcpkg use a little cleaner we set two environment variables, defining the tpe of system (x64 / x86) and the location of vcpkg.exe. Open a command promt with administrator privilages (hit windows key, type "cmd", right click "Command Prompt" and choose "Run as Administrator") .
These commands may take a few seconds to execute.

```
setx VCPKG_DEFAULT_TRIPLET "x64-windows" /m
setx VCPKG_ROOT "C:\vcpkg" /m
```
Close the Admin Command Prompt window to flush the newly set variables.

Go to your vcpkg.exe installed location and open another command prompt.

Then we install the various libraries needed for this project.
```
vcpkg install glew glfw3 glm imgui opencv
```
This should take 3-4 minutes. imgui may or may not work, you may just use the files located in this repo.

<h4>Ubuntu</h4>

sudo apt install libopencv-dev libglew-dev libglfw3-dev libglm-dev
