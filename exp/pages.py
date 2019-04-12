from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1


class EnvelopeSelection(Page):
    def is_displayed(self):
        return not self.participant.vars["leave"]

    def vars_for_template(self):
        return {
            'unopened': self.participant.vars['values'][self.round_number:],
            'envelope': self.participant.vars['values'][self.round_number-1],
            'opened': self.participant.vars['values'][:self.round_number-1]
        }


class EnterMinimumBuyout(Page):
    form_model = 'player'
    form_fields = ['buyout']

    def is_displayed(self):
        return not self.round_number == Constants.num_rounds and not self.participant.vars["leave"]

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
        print("Envelope value = {}".format(self.participant.vars['values'][self.round_number-1]))
        self.player.envelope_value = self.participant.vars['values'][self.round_number-1]
        if self.player.buyout is not None and self.player.buyout > 0:
            self.player.leave = True
            self.player.offer = random.randint(0, 100)
            if self.player.offer >= self.player.buyout:
                self.participant.vars["leave"] = True
                self.player.payoff = self.player.offer
        else:
            self.player.buyout = 0


class BuyoutOutcome(Page):
    def is_displayed(self):
        return self.player.buyout is not None and self.player.buyout > 0 and self.player.offer < self.player.buyout

    def vars_for_template(self):
        return {
            'buyout': self.player.buyout,
            'offer': self.player.offer,
        }


class Outcome(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        random_round = self.participant.vars['random_round']
        return {
            'unopened': self.participant.vars['values'][random_round:],
            'remaining': len(self.participant.vars['values'][random_round:]),
            'random_round': random_round,
            'random_envelope_id': self.participant.vars['random_envelope_id'],
            'envelope_value': self.participant.vars['envelope_value'],
            'probability_treatment': self.session.config['probability_treatment'],
            'r': self.participant.vars['r'],
            'outcome_payoff': self.participant.vars['outcome_payoff']

        }


page_sequence = [
    Instructions,
    EnvelopeSelection,
    EnterMinimumBuyout,
    BuyoutOutcome,
    Outcome,
]
