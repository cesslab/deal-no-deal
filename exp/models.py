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
                if self.session.config['random_envelopes_enabled']:
                    player.participant.vars["values"] = random.sample(range(1, 100), 10)
                else:
                    player.participant.vars["values"] = [self.session.config[f"envelope_{i}"] for i in range(1, 11)]
                player.participant.vars["leave"] = False
                random_round = random.randint(1, 9)
                player.participant.vars["random_round"] = random_round
                remaining = player.participant.vars['values'][random_round:]
                random_envelope_id = random.randint(0, len(remaining)-1)
                envelope_value = remaining[random_envelope_id]
                player.participant.vars["envelope_value"] = envelope_value

                player.participant.vars["random_envelope_id"] = random_envelope_id+1

                r = random.randint(0, 100)
                player.participant.vars['r'] = r
                if self.session.config['probability_treatment']:
                    if r <= envelope_value:
                        player.participant.vars['outcome_payoff'] = self.session.config['prize']
                    else:
                        player.participant.vars['outcome_payoff'] = 0
                else:
                    player.participant.vars['outcome_payoff'] = envelope_value





class Group(BaseGroup):
    pass


class Player(BasePlayer):
    buyout = models.IntegerField(blank=True)
    offer = models.IntegerField(default=0)
    envelope_value = models.IntegerField()
    leave = models.BooleanField(default=False)
    random_val = models.FloatField()
    rand_round = models.IntegerField()
