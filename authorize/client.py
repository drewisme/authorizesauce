from uuid import uuid4

from authorize.apis.customer import CustomerAPI
from authorize.apis.recurring import RecurringAPI
from authorize.apis.transaction import TransactionAPI
from authorize.exceptions import AuthorizeInvalidError


class AuthorizeClient(object):
    def __init__(self, login_id, transaction_key, debug=True, test=False):
        self.login_id = login_id
        self.transaction_key = transaction_key
        self.debug = debug
        self.test = test
        self._transaction = TransactionAPI(login_id, transaction_key,
            debug, test)
        self._recurring = RecurringAPI(login_id, transaction_key, debug, test)
        self._customer = CustomerAPI(login_id, transaction_key, debug, test)

    def card(self, credit_card, address=None):
        return AuthorizeCreditCard(self, credit_card, address=address)

    def transaction(self, uid):
        return AuthorizeTransaction(self, uid)

    def saved_card(self, uid):
        return AuthorizeSavedCard(self, uid)

    def recurring(self, uid):
        return AuthorizeRecurring(self, uid)

class AuthorizeCreditCard(object):
    def __init__(self, client, credit_card, address=None):
        self._client = client
        self.credit_card = credit_card
        self.address = address

    def __repr__(self):
        return '<AuthorizeCreditCard {0.credit_card.card_type} ' \
            '{0.credit_card.safe_number}>'.format(self)

    def auth(self, amount):
        response = self._client._transaction.auth(
            amount, self.credit_card, self.address)
        transaction = self._client.transaction(response['transaction_id'])
        transaction.full_response = response
        return transaction

    def capture(self, amount):
        response = self._client._transaction.capture(
            amount, self.credit_card, self.address)
        transaction = self._client.transaction(response['transaction_id'])
        transaction.full_response = response
        return transaction

    def credit(self, amount):
        # Creates an "unlinked credit" (as opposed to refunding a previous transaction)
        response = self._client._transaction.credit(
            self.credit_card.card_number, amount=amount)
        transaction = self._client.transaction(response['transaction_id'])
        transaction.full_response = response
        return transaction

    def save(self):
        unique_id = uuid4().hex[:20]
        payment = self._client._customer.create_saved_payment(
            self.credit_card, address=self.address)
        profile_id, payment_ids = self._client._customer \
            .create_saved_profile(unique_id, [payment])
        uid = '{0}|{1}'.format(profile_id, payment_ids[0])
        return self._client.saved_card(uid)

    def recurring(self, amount, start, days=None, months=None,
            occurrences=None, trial_amount=None, trial_occurrences=None):
        uid = self._client._recurring.create_subscription(
            self.credit_card, amount, start, days=days, months=months,
            occurrences=occurrences, trial_amount=trial_amount,
            trial_occurrences=trial_occurrences)
        return self._client.recurring(uid)

class AuthorizeTransaction(object):
    def __init__(self, client, uid):
        self._client = client
        self.uid = uid

    def __repr__(self):
        return '<AuthorizeTransaction {0.uid}>'.format(self)

    def settle(self, amount=None):
        response = self._client._transaction.settle(self.uid, amount=amount)
        transaction = self._client.transaction(response['transaction_id'])
        transaction.full_response = response
        return transaction

    def credit(self, card_number, amount=None):
        # card_number is last four digits of card
        response = self._client._transaction.credit(
            card_number, transaction_id=self.uid, amount=amount)
        transaction = self._client.transaction(response['transaction_id'])
        transaction.full_response = response
        return transaction

    def void(self):
        response = self._client._transaction.void(self.uid)
        transaction = self._client.transaction(response['transaction_id'])
        transaction.full_response = response
        return transaction

class AuthorizeSavedCard(object):
    def __init__(self, client, uid):
        self._client = client
        self.uid = uid
        self._profile_id, self._payment_id = uid.split('|')

    def __repr__(self):
        return '<AuthorizeSavedCard {0.uid}>'.format(self)

    def auth(self, amount):
        response = self._client._customer.auth(
            self._profile_id, self._payment_id, amount)
        transaction = self._client.transaction(response['transaction_id'])
        transaction.full_response = response
        return transaction

    def capture(self, amount):
        response = self._client._customer.capture(
            self._profile_id, self._payment_id, amount)
        transaction = self._client.transaction(response['transaction_id'])
        transaction.full_response = response
        return transaction

    def credit(self, amount):
        # Creates an "unlinked credit" (as opposed to refunding a previous transaction)
        response = self._client._customer.credit(
            self._profile_id, self._payment_id, amount)
        transaction = self._client.transaction(response['transaction_id'])
        transaction.full_response = response
        return transaction

    def delete(self):
        self._client._customer.delete_saved_payment(
            self._profile_id, self._payment_id)

class AuthorizeRecurring(object):
    def __init__(self, client, uid):
        self._client = client
        self.uid = uid

    def __repr__(self):
        return '<AuthorizeRecurring {0.uid}>'.format(self)

    def update(self, amount=None, start=None, occurrences=None,
            trial_amount=None, trial_occurrences=None):
        self._client._recurring.update_subscription(self.uid,
            amount=amount, start=start, occurrences=occurrences,
            trial_amount=trial_amount, trial_occurrences=trial_occurrences)

    def delete(self):
        self._client._recurring.delete_subscription(self.uid)
