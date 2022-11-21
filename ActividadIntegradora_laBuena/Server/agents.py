from mesa import Agent

class Robot(Agent):
  
  def __init__(self, unique_id, model):
    super().__init__(unique_id, model)
    self.empty = True
    self.move_w_box = False
    
