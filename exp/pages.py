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
        labels = self.participant.vars['envelope_labels']
        unopened_labels = sorted(labels[self.round_number:])
        opened_labels = labels[:self.round_number-1]
        opened_values = self.participant.vars['values'][:self.round_number-1]

        unopened_envelopes = []
        opened_envelopes = []
        for i in range(0, len(unopened_labels)):
            unopened_envelopes.append({
                'label': unopened_labels[i],
            })

        for i in range(0, len(opened_labels)):
            opened_envelopes.append({
                'label': opened_labels[i],
                'value': opened_values[i]
            })

        envelope = {
            'label': labels[self.round_number-1],
            'value': self.participant.vars['values'][self.round_number-1]
        }
        return {
            'unopened': unopened_envelopes,
            'opened': opened_envelopes,
            'envelope': envelope,
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
        self.player.envelope_value = self.participant.vars['values'][self.round_number-1]
        print(f"Player buyout {self.player.buyout}")
        if self.player.buyout is not None and self.player.buyout > 0:
            self.player.offer = random.randint(0, 100)
            print(f"Computer offer {self.player.offer}")
            if self.player.offer >= self.player.buyout:
                self.participant.vars["leave"] = True
                self.player.payoff = self.player.offer
        else:
            self.player.buyout = 0


class BuyoutOutcome(Page):
    def is_displayed(self):
        return self.player.buyout is not None and self.player.buyout > 0

    def vars_for_template(self):
        return {
            'payoff': self.player.payoff,
            'buyout': self.player.buyout,
            'offer': self.player.offer,
        }


class Outcome(Page):
    def is_displayed(self):
        return not self.participant.vars["leave"] and self.round_number == Constants.num_rounds

    def vars_for_template(self):
        payoff_envelope = self.participant.vars['payoff_envelope']
        labels = self.participant.vars['envelope_labels']
        unopened_labels = sorted(labels[payoff_envelope['round']:])

        unopened_envelopes = []
        for i in range(0, len(unopened_labels)):
            unopened_envelopes.append({
                'label': unopened_labels[i],
            })

        return {
            'unopened': unopened_envelopes,
            'envelope': payoff_envelope,
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
