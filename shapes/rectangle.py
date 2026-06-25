from shapes.shape import Shape

class Rectangle(Shape):
  
  def __init__(self,start, end, color= (1,0,0)):
    super().__init__(color)
    x1,y1 = start
    x2,y2 = end

    self.vertices=[
      (x1,y1),
      (x2,y1),
      (x2,y2),
      (x1,y2)
    ]