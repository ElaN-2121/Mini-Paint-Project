from shapes.shape import Shape

class Line (Shape):
  
  def __init__(self, start, end, color=(1,0,0)):
    super().__init__(color)

  def add_point(self, point):
    self.vertices.append(point)