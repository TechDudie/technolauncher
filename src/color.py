def _limit(x):
    if x > 255:
        return 255
    return x

class AnimatedTheme:
    def __init__(self):
        self.x = 0
        self.multiplier = 0.4

    def color(self):
        return (_limit(51 + 51 ** self.x), _limit(102 + -51 * self.x), 238)
    
    def update(self, delta):
        self.x += delta * self.multiplier / (self.x + 3)
        if self.x > 1 or self.x < 0:
            self.multiplier *= -1