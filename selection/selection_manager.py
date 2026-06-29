import math

class SelectionManager:
    def __init__(self, shape_manager):
        self.shape_manager = shape_manager
        self.selected_shape = None
        self.threshold = 10.0

    def select_at(self, mouse_x, mouse_y):
        shapes = self.shape_manager.shapes
        
        for shape in reversed(shapes):
            if self._hit_test(shape, mouse_x, mouse_y):
                self.selected_shape = shape
                return shape
        
        self.selected_shape = None
        return None

    def deselect(self):
        self.selected_shape = None

    def draw_highlight(self):
        if not self.selected_shape or not self.selected_shape.vertices:
            return
            
        from OpenGL.GL import glColor3f, glLineWidth, glBegin, glEnd, glVertex2f, GL_LINE_LOOP, GL_POINTS, glPointSize
        
        vertices = self.selected_shape.transform.apply_to(self.selected_shape.vertices)
        if not vertices:
            return
            
        xs = [v[0] for v in vertices]
        ys = [v[1] for v in vertices]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        padding = 6
        min_x -= padding
        max_x += padding
        min_y -= padding
        max_y += padding
        
        glColor3f(0.0, 0.7, 1.0)
        glLineWidth(2.0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(min_x, min_y)
        glVertex2f(max_x, min_y)
        glVertex2f(max_x, max_y)
        glVertex2f(min_x, max_y)
        glEnd()
        
        pivot = self.selected_shape.transform.pivot
        if pivot:
            px, py = pivot
            tx = self.selected_shape.transform.tx
            ty = self.selected_shape.transform.ty
            world_px = px + tx
            world_py = py + ty
            
            glPointSize(8.0)
            glBegin(GL_POINTS)
            glColor3f(1.0, 0.2, 0.2)
            glVertex2f(world_px, world_py)
            glEnd()

    def _hit_test(self, shape, mx, my):
        transformed_vertices = shape.transform.apply_to(shape.vertices)
        if not transformed_vertices:
            return False

        shape_type = shape.__class__.__name__.lower()

        if "line" in shape_type:
            for i in range(len(transformed_vertices) - 1):
                p1 = transformed_vertices[i]
                p2 = transformed_vertices[i+1]
                if self._point_to_segment_distance(mx, my, p1, p2) <= self.threshold:
                    return True
            return False
        else:
            return self._point_in_polygon(mx, my, transformed_vertices)

    def _point_to_segment_distance(self, px, py, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        
        if dx == 0 and dy == 0:
            return math.hypot(px - x1, py - y1)
            
        t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
        t = max(0.0, min(1.0, t))
        
        nx = x1 + t * dx
        ny = y1 + t * dy
        return math.hypot(px - nx, py - ny)

    def _point_in_polygon(self, px, py, vertices):
        inside = False
        n = len(vertices)
        if n < 3:
            for i in range(n):
                if self._point_to_segment_distance(px, py, vertices[i], vertices[(i + 1) % n]) <= self.threshold:
                    return True
            return False

        j = n - 1
        for i in range(n):
            xi, yi = vertices[i]
            xj, yj = vertices[j]
            
            if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi + 1e-9) + xi):
                inside = not inside
            j = i
            
        if not inside:
            for i in range(n):
                if self._point_to_segment_distance(px, py, vertices[i], vertices[(i + 1) % n]) <= self.threshold:
                    return True
                    
        return inside