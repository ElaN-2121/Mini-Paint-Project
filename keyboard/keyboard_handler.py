# input/keyboard_handler.py

import pygame  
from core.constants import *  

class KeyboardHandler:
    def __init__(self, shape_manager, selection_manager, ui_manager, transform_manager):

        self.shape_manager = shape_manager
        self.selection_manager = selection_manager
        self.ui_manager = ui_manager
        self.transform_manager = transform_manager
        
        self.current_mode = "DRAW" 

    def handle_keypress(self, key):

        # --- Mode & Tool Switching ---
        if key == pygame.K_l:
            self.current_mode = "DRAW"
            self.shape_manager.set_current_tool("LINE")
            self.ui_manager.update_tool_display("Line Tool Active")
            
        elif key == pygame.K_r:
            self.current_mode = "DRAW"
            self.shape_manager.set_current_tool("RECTANGLE")
            self.ui_manager.update_tool_display("Rectangle Tool Active")
            
        elif key == pygame.K_p:
            self.current_mode = "DRAW"
            self.shape_manager.set_current_tool("POLYGON")
            self.ui_manager.update_tool_display("Polygon Tool Active")
            
        elif key == pygame.K_s:
            self.current_mode = "SELECT"
            self.ui_manager.update_tool_display("Selection Mode Active")

        # --- Canvas Utilities & Actions ---
        elif key == pygame.K_DELETE:
            # Grab selected item and cleanly dispatch to Mike's UI/Canvas system
            selected_shape = self.selection_manager.get_selected_shape()
            if selected_shape:
                self.ui_manager.delete_shape(selected_shape, self.shape_manager)
                self.selection_manager.clear_selection()
                
        elif key == pygame.K_c:
            self.ui_manager.clear_canvas(self.shape_manager)
            self.selection_manager.clear_selection()

        # --- Active Palette Color Selection ---
        elif key == pygame.K_1:
            self.ui_manager.set_current_color((1.0, 0.0, 0.0))  # Red
        elif key == pygame.K_2:
            self.ui_manager.set_current_color((0.0, 1.0, 0.0))  # Green
        elif key == pygame.K_3:
            self.ui_manager.set_current_color((0.0, 0.0, 1.0))  # Blue

        # --- Real-Time Transformation Shortcuts (Selection Mode Only) ---
        elif self.current_mode == "SELECT":
            selected_shape = self.selection_manager.get_selected_shape()
            if selected_shape:
                self._handle_transformations(key, selected_shape)

    def _handle_transformations(self, key, shape):

        MOVE_SPEED = 5.0
        ROTATION_SPEED = 5.0  # Degrees
        SCALE_SPEED = 0.1

        # Translation (Arrow Keys)
        if key == pygame.K_LEFT:
            shape.transform.tx -= MOVE_SPEED
        elif key == pygame.K_RIGHT:
            shape.transform.tx += MOVE_SPEED
        elif key == pygame.K_UP:
            shape.transform.ty += MOVE_SPEED
        elif key == pygame.K_DOWN:
            shape.transform.ty -= MOVE_SPEED

        # Rotation (Q / E keys)
        elif key == pygame.K_q:
            shape.transform.rotation += ROTATION_SPEED
        elif key == pygame.K_e:
            shape.transform.rotation -= ROTATION_SPEED

        # Scaling (Equals/Plus to scale up, Minus to scale down)
        elif key == pygame.K_EQUALS or key == pygame.K_KP_PLUS:
            shape.transform.sx += SCALE_SPEED
            shape.transform.sy += SCALE_SPEED
        elif key == pygame.K_MINUS or key == pygame.K_KP_MINUS:
            # Prevent invert scaling or division by zero errors
            shape.transform.sx = max(0.1, shape.transform.sx - SCALE_SPEED)
            shape.transform.sy = max(0.1, shape.transform.sy - SCALE_SPEED)
