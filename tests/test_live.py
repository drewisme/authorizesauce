"""
Tests against the sandbox Authorize.net API. Slow, requires internet.

Authorize.net developer login for test
user: authorizepy0
pass: ny2qgWTw
gateway id: 355553
"""

from datetime import date, timedelta
import os

from unittest2 import skipUnless, TestCase

from authorize import Address, AuthorizeClient, CreditCard
from authorize.exceptions import AuthorizeResponseError


SKIP_MESSAGE = 'Live tests only run if the AUTHORIZE_LIVE_TESTS ' \
    'environment variable is true.'
TEST_LOGIN_ID = '285tUPuS'
TEST_TRANSACTION_KEY = '58JKJ4T95uee75wd'

@skipUnless(os.environ.get('AUTHORIZE_LIVE_TESTS'), SKIP_MESSAGE)
class AuthorizeLiveTests(TestCase):
    def setUp(self):
        self.client = AuthorizeClient(TEST_LOGIN_ID, TEST_TRANSACTION_KEY)
        self.year = date.today().year + 10
        self.credit_card = CreditCard('4111111111111111', self.year, 1, '911',
            'Jeff', 'Schenck')
        self.address = Address('45 Rose Ave', 'Venice', 'CA', '90291')

    def test_credit_card(self):
        card = self.client.card(self.credit_card, self.address)
        transaction = card.auth(10)
        transaction.void()
        self.assertRaises(AuthorizeResponseError, transaction.settle)

    def test_saved_card(self):
        card = self.client.card(self.credit_card, self.address)
        saved = card.save()
        saved.auth(10).settle()
        saved.capture(10)
        saved.credit(10)
        saved_from_id = self.client.saved_card(saved.uid)
        saved_from_id.delete()

    def test_recurring(self):
        card = self.client.card(self.credit_card, self.address)
        start = date.today() + timedelta(days=7)
        recurring = card.recurring(10, start, months=1, occurrences=10)
        recurring.update(amount=20, trial_amount=10, trial_occurrences=3)
        recurring_from_id = self.client.recurring(recurring.uid)
        recurring_from_id.delete()
