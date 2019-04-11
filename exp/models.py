from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'exp'
    players_per_group = None
    num_rounds = 10
    num_envelopes = 2


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for player in self.get_players():
                player.participant.vars["values"] = random.sample(range(1, 100), int(self.session.config['envelopes']))


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    buyout = models.IntegerField(blank=False)
