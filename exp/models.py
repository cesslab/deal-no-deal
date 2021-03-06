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
    num_rounds = 11
    num_envelopes = 11


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for player in self.get_players():
                player.participant.vars['values'] = [self.session.config[f"envelope_{i}"] for i in range(Constants.num_envelopes)]
                player.participant.vars['random_round'] = random.randint(1, 10)

                player.participant.vars['random_offer'] = random.randint(0, 100)
                unopened_values = player.participant.vars['values'][player.participant.vars['random_round'] - 1:]
                player.participant.vars['unopened_values'] = unopened_values
                player.participant.vars['random_envelope_value'] = random.choice(unopened_values)
                player.participant.vars['random_number'] = random.randint(0, 100)





class Group(BaseGroup):
    pass


class Player(BasePlayer):
    buyout = models.FloatField(blank=False, label='Enter your minimum value')
    random_offer = models.FloatField()
    random_round = models.FloatField()
    random_envelope_value = models.FloatField()
    random_number = models.FloatField()
    buyout_accepted = models.BooleanField()
    won_prize = models.BooleanField()
