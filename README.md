# Image Classifier

A utility to allow members of the VT Autonomous Aerial Vehicles team to quickly classify
images taken from their drone.

# Building and Running

This project depends on CMake and Qt being installed on your system. Both of these can be found at <https://cmake.org/download/> and <https://www.qt.io/download-qt-installer>.

The app also looks for some assets that are located in the project folder, so make sure to start the
executable from the `classifier` directory.

## Building from the Command Line

1. Enter the directory the `classifier` project was cloned into.

    ```
    cd <classifier directory>
    ```

2. Create and enter a build directory, for storing the compilation results.

    ```
    mkdir build
    cd build
    ```

3. Run the cmake command, passing in the location of the `classifier` directory. This configures the project
and detects the location of any dependencies. Extra compilation options can be passed in during this step.

    ```
    cmake ..
    ```

4. Build the project. This is the command you'll run any time you want to test out new changes.

    ```
    make
    ```

5. Enter the `classifier` directory again to run the project. This allows the executable to find the local
files it needs.

    ```
    cd ..
    build/classifier
    ```

## Building from Visual Studio

1. When installing Visual Studio, be sure to install the C++ development kit, which includes CMake support.
2. Cloning the repository from Visual Studio automatically configures the CMake project
3. Make sure that the environment variable `Qt5_DIR` in the CMake Settings page is set to `C:/Qt/5.12.5/msvc2017_64/lib/cmake/Qt5`
