from dataclasses import dataclass, field
from typing import Optional
from .ball import Ball
from .paddle import Paddle
from .score import Score

@dataclass
class GameState:
    ball: Ball = field(default_factory=Ball)
    paddle1: Paddle = field(default_factory=lambda: Paddle(x=10))
    paddle2: Paddle = field(default_factory=lambda: Paddle(x=780))
    score: Score = field(default_factory=Score)

    def to_dict(self) -> dict:
        return {
            'ball': vars(self.ball),
            'paddle1': vars(self.paddle1),
            'paddle2': vars(self.paddle2),
            'score': vars(self.score)
        }

    def update(self):
        self.ball.move()
        
        if self.ball.y - self.ball.radius <= 0 or self.ball.y + self.ball.radius >= 600:
            self.ball.dy = -self.ball.dy

        if (self.ball.x - self.ball.radius <= self.paddle1.x + self.paddle1.width and
            self.paddle1.y <= self.ball.y <= self.paddle1.y + self.paddle1.height) or \
           (self.ball.x + self.ball.radius >= self.paddle2.x and
            self.paddle2.y <= self.ball.y <= self.paddle2.y + self.paddle2.height):
            self.ball.dx = -self.ball.dx

        if self.ball.x - self.ball.radius <= 0:
            self.score.player2 += 1
            self.ball.reset()
        elif self.ball.x + self.ball.radius >= 800:
            self.score.player1 += 1
            self.ball.reset()

    def is_game_over(self) -> bool:
        return self.score.player1 >= 5 or self.score.player2 >= 5

    def get_winner(self) -> Optional[int]:
        if self.score.player1 >= 5:
            return 1
        elif self.score.player2 >= 5:
            return 2
        return None