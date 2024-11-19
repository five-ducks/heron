# games/consumers/__init__.py
from .onetoone_consumers import OneToOneGameConsumer
from .tournament_consumers import TournamentGameConsumer

__all__ = ['OneToOneGameConsumer', 'TournamentGameConsumer']