from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1


class EnvelopeSelection(Page):
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
        return not self.round_number == Constants.num_rounds


class Outcome(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [
    Instructions,
    EnvelopeSelection,
    EnterMinimumBuyout,
    Outcome,
]
