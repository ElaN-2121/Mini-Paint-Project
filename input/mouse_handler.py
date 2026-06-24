class MouseHandler:

  def __init__(self, shape_manager):
    self.shape_manager= shape_manager
    self.current_tool= "LINE"
    self.start_point= None
    self.current_polygon=None