class Environment:
    def __init__(self, (width, height)):
        self.width = width
        self.height = height
        self.particles = []

        self.colour = (255,255,255)
        self.mass_of_air = 0.2
        self.elasticity = 0.75