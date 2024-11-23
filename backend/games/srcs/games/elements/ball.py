from dataclasses import dataclass

@dataclass
class Ball:
    x: int = 400
    y: int = 300
    dx: int = 5
    dy: int = 5
    radius: int = 10

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def reset(self):
        self.x = 400
        self.y = 300
        self.dx = -self.dx
        self.dy = 5 if self.dy > 0 else -5