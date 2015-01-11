from django.utils.translation import ugettext_lazy as _
import random
import datetime
from server.bom.draw_base import *


class CardDraw(DrawBase):
    """
    Stores the content of a draw of CardsDraw
    """

    def __init__(self, type_of_deck=1, **kwargs):

        '''This may be interesting for the API'''
        self.decks = {'french': ["h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "h10", "hj", "hq", "hk",
                                "t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9", "t10", "tj", "tq", "tk",
                                "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "cj", "cq", "ck",
                                "p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10", "pj", "pq", "pk"],
                     'spanish': [],
                     }

        self.type_of_deck = type_of_deck
        """Type of deck to be used"""

    def is_feasible(self):
        return self.type_of_deck in self.decks and self.number_of_results > 0

    def generate_result(self):
        return [random.randint(1, len(self.decks[self.type_of_deck])) for x in range(0, self.number_of_results)]
