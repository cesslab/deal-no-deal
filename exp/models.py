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
    num_envelopes = 10


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for player in self.get_players():

                if self.session.config['random_envelopes_enabled']:
                    player.participant.vars["values"] = random.sample(range(1, 100), Constants.num_envelopes)
                else:
                    player.participant.vars["values"] = [self.session.config[f"envelope_{i}"] for i in range(1, Constants.num_envelopes + 1)]

                player.participant.vars["envelope_labels"] = list(range(1, Constants.num_envelopes + 1))
                random.shuffle(player.participant.vars['envelope_labels'])
                # Set the player leave state
                player.participant.vars["leave"] = False

                # Generate the random round in which to play out the game, if the player never enters their min buyout
                random_round = random.randint(1, 9)
                random_envelope_index = random.randint(random_round-1, Constants.num_envelopes-1)
                payoff_envelope = {
                    'round': random_round,
                    'index': random_envelope_index,
                    'value': player.participant.vars['values'][random_envelope_index],
                    'label': player.participant.vars['envelope_labels'][random_envelope_index]
                }
                player.participant.vars['payoff_envelope'] = payoff_envelope

                r = random.randint(0, 100)
                player.participant.vars['r'] = r
                if self.session.config['probability_treatment']:
                    if r <= payoff_envelope['value']:
                        player.participant.vars['outcome_payoff'] = self.session.config['prize']
                    else:
                        player.participant.vars['outcome_payoff'] = 0
                else:
                    player.participant.vars['outcome_payoff'] = payoff_envelope['value']





class Group(BaseGroup):
    pass


class Player(BasePlayer):
    buyout = models.IntegerField(blank=True)
    offer = models.IntegerField(default=0)
    envelope_value = models.IntegerField()
    leave = models.BooleanField(default=False)
    random_val = models.FloatField()
    rand_round = models.IntegerField()
