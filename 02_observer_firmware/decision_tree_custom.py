
class DecisionTreeCustom:
  
  def predict(self, x):
    
    y = [0, 0, 0]
    
    if not x <= 0.111:
      y = [255, 225, 195]
    
    elif x <= 0.076:
      y = [0, 0, 0]
      
    elif not x <= 0.103:
      y = [255, 225, 0]
      
    elif x <= 0.084:
      y = [0, 0, 195]
      
    elif not x <= 0.093:
      if not x <= 0.100:
        y = [255, 0, 0]
      else:
        y = [255, 0, 195]
        
    else:
      if x <= 0.087:
        y = [0, 225, 0]
      else:
        y = [0, 225, 195]
        
    return y[0], y[1], y[2]