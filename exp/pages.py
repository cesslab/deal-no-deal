from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1


class FirstRoundEntry(Page):
    def is_displayed(self):
        return self.round_number == 1

    form_model = 'player'
    form_fields = ['buyout']

    def vars_for_template(self):
        values = self.participant.vars['values'][:]

        values.sort()

        return {
            'round': self.round_number,
            'unopened': values,
            'value_type': '%' if (self.session.config['probability_treatment']) else 'Points'
        }

    def buyout_min(self):
        if 'buyout_min' in self.session.config:
            buyout_min = self.session.config['buyout_min']
        else:
            buyout_min = 0

        return buyout_min

    def buyout_max(self):
        if 'buyout_max' in self.session.config:
            buyout_max = self.session.config['buyout_max']
        else:
            buyout_max = 0

        return buyout_max

    def before_next_page(self):
        if self.round_number == self.player.participant.vars['random_round']:
            self.player.participant.vars['buyout'] = self.player.buyout


class RoundEntry(Page):
    def is_displayed(self):
        return self.round_number > 1

    form_model = 'player'
    form_fields = ['buyout']

    def vars_for_template(self):
        values = self.participant.vars['values']

        envelope = {
            'index': self.round_number - 2,
            'value': values[self.round_number - 2]
        }

        opened_values = values[:self.round_number - 2]
        unopened_values = values[self.round_number - 2:]
        unopened_values.sort()

        return {
            'round': self.round_number,
            'unopened': unopened_values,
            'opened': opened_values,
            'envelope': envelope,
            'value_type': '%' if (self.session.config['probability_treatment']) else 'Points'
        }

    def buyout_min(self):
        if 'buyout_min' in self.session.config:
            buyout_min = self.session.config['buyout_min']
        else:
            buyout_min = 0

        return buyout_min

    def buyout_max(self):
        if 'buyout_max' in self.session.config:
            buyout_max = self.session.config['buyout_max']
        else:
            buyout_max = 0

        return buyout_max

    def before_next_page(self):
        if self.round_number == self.player.participant.vars['random_round']:
            self.player.participant.vars['buyout'] = self.player.buyout


class Outcome(Page):
    def is_displayed(self):
        return not self.participant.vars["leave"] and self.round_number == Constants.num_rounds

    def vars_for_template(self):
        offer = self.participant.vars['random_offer']
        random_round = self.participant.vars['random_round']
        random_number = self.participant.vars['random_number']
        random_envelope_value = self.participant.vars['random_envelope_value']
        unopened_values = self.participant.vars['unopened_values']
        buyout = self.participant.vars['buyout']

        accept_offer = buyout < offer
        won_prize = random_number <= random_envelope_value

        return {
            'random_round': random_round,
            'unopened': unopened_values,
            'envelope': random_envelope_value,
            'prob_treatment': self.session.config['probability_treatment'],
            'accept_offer': accept_offer,
            'won_prize': won_prize,
            'buyout': buyout,
            'offer': offer,
            'random_number': random_number,
            'prize': self.session.config['prize'],
        }
    
    def before_next_page(self):
        self.player.buyout = self.participant.vars['buyout']
        self.player.random_offer = self.participant.vars['random_offer']
        self.player.random_round = self.participant.vars['random_round']
        self.player.random_envelope_value = self.participant.vars['random_envelope_value']
        self.player.random_number = self.participant.vars['random_number']


page_sequence = [
    Instructions,
    FirstRoundEntry,
    RoundEntry,
    Outcome,
]
