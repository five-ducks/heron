from dataclasses import dataclass

@dataclass
class Paddle:
    x: int
    y: int = 250
    width: int = 10
    height: int = 100