


class Stencil():
  '''
  Collection of points for drawing on a canvas,
  Differnet than a font. A font will have more crushed in, spacing
  ajusted. But several stencils will be stretched, barlines and the like.
  
  We do nothing, give it a name.
  '''
  # Lets just see...
  def __init__(self, name, style):
    self.name = name
    self.style = style
