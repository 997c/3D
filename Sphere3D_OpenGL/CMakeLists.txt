cmake_minimum_required(VERSION 3.10)
project(Sphere3D)

set(CMAKE_CXX_STANDARD 17)

# Point to vcpkg toolchain
set(CMAKE_TOOLCHAIN_FILE "C:/vcpkg/scripts/buildsystems/vcpkg.cmake")

# Set default build type to Release if none specified
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Release")
endif()

# Find packages
find_package(glfw3 CONFIG REQUIRED)
find_package(glad CONFIG REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(glm REQUIRED)

# Include directories
include_directories(
    ${OPENGL_INCLUDE_DIR}
    ${GLEW_INCLUDE_DIRS}
    ${GLM_INCLUDE_DIRS}
    include/
)

# Source files
set(SOURCES
    src/main.cpp
    src/Shader.cpp
    src/Sphere.cpp
    src/Camera.cpp
)

add_executable(Sphere3D ${SOURCES})

# Copy shaders to build directory
file(COPY shaders/ DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/shaders)

target_link_libraries(Sphere3D PRIVATE
    OpenGL::GL
    GLEW::GLEW
    glfw
    glm::glm
    glad::glad
)

# For Windows, link against the Win32 libraries
if(WIN32)
    target_link_libraries(Sphere3D PRIVATE
        opengl32.lib
        gdi32.lib
    )
endif()