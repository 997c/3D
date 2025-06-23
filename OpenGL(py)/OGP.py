import sys
import time
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QSurfaceFormat
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(OpenGLWidget, self).__init__(parent)
        self.setMinimumSize(800, 600)
        
        # Camera parameters
        self.zoom = -15.0
        self.rotation_x = 30.0
        self.rotation_y = -45.0
        self.translation_x = 0.0
        self.translation_y = 0.0
        
        # Mouse interaction
        self.last_pos = None
        
        # FPS calculation
        self.frame_count = 0
        self.fps = 0
        self.last_fps_time = time.time()
        
        # Start update timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # ~60 FPS

    def initializeGL(self):
        glClearColor(0.1, 0.1, 0.15, 1.0)  # Dark background
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, (5.0, 5.0, 10.0, 1.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
        
        # Initialize GLUT for text rendering
        glutInit(sys.argv)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / h if h > 0 else 1.0
        gluPerspective(45, aspect, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        # Clear buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Set up modelview matrix
        glLoadIdentity()
        glTranslatef(0, 0, self.zoom)
        glTranslatef(self.translation_x, self.translation_y, 0)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        
        # Draw coordinate axes
        self.draw_coordinate_axes()
        
        # Draw the 3D HelloWorld text
        self.draw_3d_text()
        
        # Draw FPS counter
        self.draw_fps()
        
        # Update FPS counter
        self.update_fps()

    def draw_coordinate_axes(self):
        glDisable(GL_LIGHTING)
        glLineWidth(2.0)
        glBegin(GL_LINES)
        # X axis (red)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(5.0, 0.0, 0.0)
        # Y axis (green)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 5.0, 0.0)
        # Z axis (blue)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 5.0)
        glEnd()
        glEnable(GL_LIGHTING)

    def draw_3d_text(self):
        glPushMatrix()
        glColor3f(0.4, 0.8, 1.0)  # Light blue color
        glTranslatef(0.0, 0.0, 0.0)
        glScalef(0.15, 0.15, 0.15)
        glRotatef(90, 1, 0, 0)
        glRotatef(180, 0, 1, 0)
        
        # Render "HelloWorld" in 3D
        for char in "HelloWorld":
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))
        glPopMatrix()

    def draw_fps(self):
        # Switch to 2D projection
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, self.width(), 0, self.height())
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glDisable(GL_LIGHTING)
        
        # Draw FPS text in green
        glColor3f(0.0, 1.0, 0.0)
        glRasterPos2f(10, self.height() - 30)
        
        fps_text = f"FPS: {self.fps:.1f}"
        for char in fps_text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
        
        # Restore state
        glEnable(GL_LIGHTING)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    def update_fps(self):
        self.frame_count += 1
        current_time = time.time()
        elapsed = current_time - self.last_fps_time
        
        if elapsed >= 1.0:  # Update every second
            self.fps = self.frame_count / elapsed
            self.frame_count = 0
            self.last_fps_time = current_time

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_pos = event.pos()
        elif event.button() == Qt.RightButton:
            self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.last_pos is None:
            return
            
        dx = event.x() - self.last_pos.x()
        dy = event.y() - self.last_pos.y()
        
        if event.buttons() & Qt.LeftButton:  # Pan
            self.translation_x += dx * 0.02
            self.translation_y -= dy * 0.02
        elif event.buttons() & Qt.RightButton:  # Rotate
            self.rotation_x += dy * 0.5
            self.rotation_y += dx * 0.5
            
        self.last_pos = event.pos()

    def wheelEvent(self, event):
        # Zoom with mouse wheel
        self.zoom += event.angleDelta().y() * 0.05
        self.zoom = max(-25.0, min(self.zoom, -5.0))  # Limit zoom range

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("3D HelloWorld OpenGL Application")
        self.setGeometry(100, 100, 800, 600)
        
        # Set OpenGL format
        fmt = QSurfaceFormat()
        fmt.setSamples(4)  # 4x multisampling
        fmt.setVersion(3, 3)
        QSurfaceFormat.setDefaultFormat(fmt)
        
        # Create OpenGL widget
        self.gl_widget = OpenGLWidget()
        self.setCentralWidget(self.gl_widget)
        
        # Add help label
        self.statusBar().showMessage("Left mouse: Pan | Right mouse: Rotate | Wheel: Zoom")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())