from transform.transform import Transform

class Shape:
  def __init__(self, color=(1,0,0)):
    self.vertices =[] #contains original vertices only
    self.color = color
    self.transform = Transform()
  
  def draw (self):
    raise NotImplementedError()
  
  def add_vertex(self,x,y):
    self.vertices.append((x,y))
