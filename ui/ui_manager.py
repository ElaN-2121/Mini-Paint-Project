# ui/ui_manager.py

import os
from OpenGL.GL import *
from OpenGL.GLUT import *

class UIManager:
    def __init__(self, shape_manager, selection_manager):
        self.shape_manager = shape_manager
        self.selection_manager = selection_manager
        
      
        self.current_color = (1.0, 0.0, 0.0)
        
    def set_color(self, color_idx):
        """Sets the active drawing color based on user keyboard input (1, 2, 3)."""
        if color_idx == 1:
            self.current_color = (1.0, 0.0, 0.0)  # Red
        elif color_idx == 2:
            self.current_color = (0.0, 1.0, 0.0)  # Green
        elif color_idx == 3:
            self.current_color = (0.0, 0.0, 1.0)  # Blue
            
        
        selected_shape = self.selection_manager.get_selected_shape()
        if selected_shape:
            selected_shape.color = self.current_color

    def delete_selected(self):
        """Removes the currently selected shape from the application."""
        selected_shape = self.selection_manager.get_selected_shape()
        if selected_shape:
            self.shape_manager.remove_shape(selected_shape)
            self.selection_manager.clear_selection()

    def clear_canvas(self):
        """Wipes all shapes and clears selection."""
        self.shape_manager.clear_all()
        self.selection_manager.clear_selection()

    def draw_hud(self, current_tool_name, window_width, window_height):
        """
        Renders a simple on-screen text display showing the current tool, 
        selected color, and a quick help menu.
        """
        # Switch to orthographic projection for 2D UI overlay rendering
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, window_width, 0, window_height, -1, 1)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
       
        glDisable(GL_DEPTH_TEST)
        
       
        color_name = "Red"
        if self.current_color == (0.0, 1.0, 0.0): color_name = "Green"
        elif self.current_color == (0.0, 0.0, 1.0): color_name = "Blue"

        ui_lines = [
            f"Active Tool: {current_tool_name}",
            f"Active Color: {color_name}",
            "-------------------------",
            "Controls:",
            "  L: Line | R: Rect | P: Poly | S: Select",
            "  1: Red  | 2: Green | 3: Blue",
            "  [Delete]: Remove Shape",
            "  [C]: Clear Canvas"
        ]
        
       
        glColor3f(1.0, 1.0, 1.0) # White text
        y_offset = window_height - 30
        for line in ui_lines:
            glRasterPos2i(20, y_offset)
            for char in line:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))
            y_offset -= 20
            
       
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()