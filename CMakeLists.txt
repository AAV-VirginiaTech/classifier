cmake_minimum_required(VERSION 3.5)
project(classifier CXX)

# require a C++11 compiler
# use it for all targets
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# configure Qt
set(CMAKE_AUTOMOC ON)
set(CMAKE_INCLUDE_CURRENT_DIR ON)
find_package(Qt5 COMPONENTS Widgets Core Test REQUIRED)

# list any cpp files here
# don't include header or template files
set(src_files
    src/classifier/main.cpp
    src/classifier/window.cpp
    src/classifier/filepath_button.cpp
)

# some editors use this for intellisense support
set(CMAKE_EXPORT_COMPILE_COMMANDS 1)

include_directories(src)
add_executable(classifier ${src_files})
target_link_libraries(classifier Qt5::Widgets)
