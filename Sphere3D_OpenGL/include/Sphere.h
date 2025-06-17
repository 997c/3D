#ifndef SPHERE_H
#define SPHERE_H

#include <vector>
#include <glad/glad.h>
#include <glm/glm.hpp>

class Sphere {
public:
    Sphere(float radius = 1.0f, int sectors = 36, int stacks = 18);
    ~Sphere();
    
    void Draw();
    
private:
    void buildVertices();
    void setupMesh();
    
    float radius;
    int sectorCount;
    int stackCount;
    
    std::vector<float> vertices;
    std::vector<unsigned int> indices;
    
    unsigned int VAO, VBO, EBO;
};

#endif