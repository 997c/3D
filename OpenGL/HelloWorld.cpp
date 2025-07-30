#include <GL/glut.h>
#include <GL/gl.h>

void renderScene() {
    glClear(GL_COLOR_BUFFER_BIT);  // Clear color buffer
    
    // Set text color (white)
    glColor3f(1.0, 1.0, 1.0);
    
    // Set position for text
    glRasterPos2f(-0.2, 0.0);  // Position in normalized coordinates
    
    // Text to display
    const char* text = "Hello, OpenGL World!";
    
    // Render each character
    for (const char* c = text; *c != '\0'; c++) {
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, *c);
    }
    
    glFlush();  // Render now
}

int main(int argc, char** argv) {
    // Initialize GLUT
    glutInit(&argc, argv);
    
    // Create window with single buffer and RGB mode
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowSize(500, 200);  // Window size
    glutCreateWindow("OpenGL Hello World");
    
    // Set background color (black)
    glClearColor(0.0, 0.0, 0.0, 1.0);
    
    // Register display callback
    glutDisplayFunc(renderScene);
    
    // Enter main event loop
    glutMainLoop();
    
    return 0;
}